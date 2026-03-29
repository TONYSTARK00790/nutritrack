import os
import requests
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from meals.models import Food
import time


class Command(BaseCommand):
    help = 'Download food images from Wikipedia and upload them to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-download',
            action='store_true',
            help='Skip download and only upload existing images from folder'
        )
        parser.add_argument(
            '--folder',
            type=str,
            default='downloaded_food_images',
            help='Folder to save images (default: downloaded_food_images)'
        )

    def handle(self, *args, **options):
        skip_download = options.get('skip_download')
        folder_name = options.get('folder')
        folder_path = Path(folder_name)

        # Create folder if it doesn't exist
        folder_path.mkdir(exist_ok=True)

        if not skip_download:
            self.stdout.write(self.style.SUCCESS('\n🔽 DOWNLOADING FOOD IMAGES...\n'))
            self.download_images(folder_path)

        self.stdout.write(self.style.SUCCESS('\n⬆️  UPLOADING IMAGES TO DATABASE...\n'))
        self.upload_images(folder_path)

    def download_images(self, folder_path):
        """Download images from Wikipedia for each food"""
        foods = Food.objects.all().order_by('name')
        total = foods.count()
        downloaded = 0
        failed = 0

        for idx, food in enumerate(foods, 1):
            # Skip if already downloaded
            image_path = folder_path / f"{food.name}.jpg"
            if image_path.exists():
                self.stdout.write(f'  ⏭️  SKIP ({idx}/{total}): {food.name} - already exists')
                continue

            # Try to download from Wikipedia
            try:
                image_url = self.get_food_image_url(food.name)
                if image_url:
                    self.download_image(image_url, image_path)
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ DOWNLOAD ({idx}/{total}): {food.name}')
                    )
                    downloaded += 1
                    time.sleep(0.5)  # Be nice to servers
                else:
                    self.stdout.write(
                        self.style.WARNING(f'  ✗ NOT FOUND ({idx}/{total}): {food.name} - no image found')
                    )
                    failed += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ ERROR ({idx}/{total}): {food.name} - {str(e)[:50]}')
                )
                failed += 1

        self.stdout.write(f'\n{self.style.SUCCESS("=" * 60)}')
        self.stdout.write(self.style.SUCCESS(f'Summary:'))
        self.stdout.write(f'  📁 Total foods: {total}')
        self.stdout.write(self.style.SUCCESS(f'  ✓ Downloaded: {downloaded}'))
        self.stdout.write(self.style.WARNING(f'  ✗ Failed: {failed}'))
        self.stdout.write(f'  ⏭️  Skipped: {total - downloaded - failed}')
        self.stdout.write(f'  📂 Saved to: {folder_path.absolute()}\n')

    def get_food_image_url(self, food_name):
        """Get image URL from Wikipedia for a food"""
        search_url = f'https://en.wikipedia.org/w/api.php'
        
        params = {
            'action': 'query',
            'titles': food_name,
            'prop': 'pageimages',
            'pithumbsize': 500,
            'format': 'json'
        }

        try:
            response = requests.get(search_url, params=params, timeout=5)
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if 'thumbnail' in page_data:
                    return page_data['thumbnail']['source']
                if 'pageimage' in page_data:
                    return page_data['pageimage']
            
            return None
        except Exception as e:
            return None

    def download_image(self, url, save_path):
        """Download image from URL and save to file"""
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)

    def upload_images(self, folder_path):
        """Upload images from folder to database"""
        foods = Food.objects.all()
        uploaded = 0
        skipped = 0
        not_found = 0
        total_foods = foods.count()

        for idx, food in enumerate(foods, 1):
            # Find image file
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            image_file = None
            
            for ext in image_extensions:
                potential_path = folder_path / f"{food.name}{ext}"
                if potential_path.exists():
                    image_file = potential_path
                    break

            if not image_file:
                self.stdout.write(
                    self.style.WARNING(f'  ✗ NOT FOUND ({idx}/{total_foods}): {food.name}')
                )
                not_found += 1
                continue

            if food.image:
                self.stdout.write(
                    self.style.WARNING(f'  ⏭️  SKIP ({idx}/{total_foods}): {food.name} - already has image')
                )
                skipped += 1
                continue

            try:
                # Read and save image
                with open(image_file, 'rb') as f:
                    file_content = ContentFile(f.read(), name=image_file.name)
                    food.image = file_content
                    food.save()

                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ UPLOAD ({idx}/{total_foods}): {food.name}')
                )
                uploaded += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ ERROR ({idx}/{total_foods}): {food.name} - {str(e)[:50]}')
                )

        self.stdout.write(f'\n{self.style.SUCCESS("=" * 60)}')
        self.stdout.write(self.style.SUCCESS(f'Upload Summary:'))
        self.stdout.write(f'  📁 Total foods: {total_foods}')
        self.stdout.write(self.style.SUCCESS(f'  ✓ Uploaded: {uploaded}'))
        self.stdout.write(self.style.WARNING(f'  ✗ Failed: {not_found}'))
        self.stdout.write(f'  ⏭️  Skipped: {skipped}\n')

        if uploaded > 0:
            self.stdout.write(self.style.SUCCESS(f'✅ Upload complete!'))
            self.stdout.write(f'Visit: http://localhost:8000/meals/foods/ to see images!\n')

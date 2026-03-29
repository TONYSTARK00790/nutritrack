import os
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from meals.models import Food


class Command(BaseCommand):
    help = 'Batch upload food images from a folder. Image filenames should match food names (case-insensitive)'

    def add_arguments(self, parser):
        parser.add_argument(
            'image_folder',
            type=str,
            help='Path to folder containing food images'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be uploaded without making changes'
        )

    def handle(self, *args, **options):
        folder_path = Path(options['image_folder'])
        dry_run = options['dry_run']

        # Validate folder exists
        if not folder_path.exists() or not folder_path.is_dir():
            raise CommandError(f'Folder not found: {folder_path}')

        # Supported image extensions
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        
        # Get all image files
        image_files = [f for f in folder_path.iterdir() 
                      if f.is_file() and f.suffix.lower() in image_extensions]

        if not image_files:
            self.stdout.write(self.style.WARNING(f'No image files found in {folder_path}'))
            return

        self.stdout.write(f'Found {len(image_files)} image files')
        
        matched = 0
        skipped = 0
        uploaded = 0

        for image_file in sorted(image_files):
            # Extract food name from filename (remove extension)
            food_name = image_file.stem.strip()
            
            # Try to find matching food (case-insensitive)
            try:
                food = Food.objects.get(name__iexact=food_name)
                
                if food.image:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠ SKIP: {food_name} - already has image')
                    )
                    skipped += 1
                    continue
                
                matched += 1
                
                if dry_run:
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ WOULD UPLOAD: {food_name} ({image_file.name})')
                    )
                else:
                    # Read file and save to model
                    with open(image_file, 'rb') as f:
                        file_content = ContentFile(f.read(), name=image_file.name)
                        food.image = file_content
                        food.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ UPLOADED: {food_name} ({image_file.name})')
                    )
                    uploaded += 1
            
            except Food.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'  ✗ NOT FOUND: {food_name} - no matching food in database')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ ERROR: {food_name} - {str(e)}')
                )

        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'Summary:'))
        self.stdout.write(f'  📁 Total image files: {len(image_files)}')
        self.stdout.write(f'  ✓ Matched foods: {matched}')
        if dry_run:
            self.stdout.write(self.style.WARNING(f'  [DRY RUN] Would upload: {matched}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'  ✓ Successfully uploaded: {uploaded}'))
        self.stdout.write(f'  ⚠ Skipped (already have image): {skipped}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\n⚠️  DRY RUN MODE - No changes made. Run without --dry-run to upload.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✅ Upload complete!'))

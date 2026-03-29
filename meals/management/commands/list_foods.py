from django.core.management.base import BaseCommand
from meals.models import Food


class Command(BaseCommand):
    help = 'List all food names to help with image file naming'

    def add_arguments(self, parser):
        parser.add_argument(
            '--category',
            type=str,
            help='Filter by category (veg, non_veg, grain, snack, fruit, beverage, dairy)'
        )
        parser.add_argument(
            '--cuisine',
            type=str,
            help='Filter by cuisine (indian, chinese, continental)'
        )
        parser.add_argument(
            '--export',
            type=str,
            help='Export to CSV file (provide filename, e.g., food_names.csv)'
        )

    def handle(self, *args, **options):
        foods = Food.objects.all()

        # Apply filters
        if options.get('category'):
            foods = foods.filter(category=options['category'])
        if options.get('cuisine'):
            foods = foods.filter(cuisine=options['cuisine'])

        # Sort by name
        foods = foods.order_by('name')

        # Export to CSV if requested
        if options.get('export'):
            import csv
            from pathlib import Path
            
            filename = options['export']
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Food Name', 'Category', 'Cuisine', 'Calories', 'Protein', 'Carbs', 'Fat'])
                
                for food in foods:
                    writer.writerow([
                        food.name,
                        food.get_category_display(),
                        food.get_cuisine_display(),
                        food.calories_per_100g,
                        food.protein,
                        food.carbs,
                        food.fat
                    ])
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Exported {foods.count()} foods to {filename}')
            )
            return

        # Display foods
        if not foods.exists():
            self.stdout.write(self.style.WARNING('No foods found matching filters'))
            return

        self.stdout.write(f'\n📋 {foods.count()} Food(s) Found:\n')
        self.stdout.write('─' * 80)

        for idx, food in enumerate(foods, 1):
            has_image = '✓' if food.image else '✗'
            self.stdout.write(
                f'{idx:3}. [{has_image}] {food.name:<40} | {food.get_category_display():<10} | {food.get_cuisine_display():<12}'
            )

        self.stdout.write('─' * 80)
        
        # Count by image status
        with_image = foods.filter(image__isnull=False).count()
        without_image = foods.exclude(image__isnull=False).count()
        
        self.stdout.write(f'\n📊 Summary:')
        self.stdout.write(f'  Total: {foods.count()}')
        self.stdout.write(self.style.SUCCESS(f'  ✓ With images: {with_image}'))
        self.stdout.write(self.style.WARNING(f'  ✗ Without images: {without_image}'))

        # Filename suggestions for first 5 foods (for reference)
        self.stdout.write(f'\n💡 Filename Examples (use these as naming templates):')
        for food in foods[:5]:
            self.stdout.write(f'  {food.name}.jpg')
        if foods.count() > 5:
            self.stdout.write(f'  ... and {foods.count() - 5} more')

        self.stdout.write(f'\nTo export all food names to CSV:')
        self.stdout.write(f'  python manage.py list_foods --export food_list.csv\n')

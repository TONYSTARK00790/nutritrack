"""
Custom management command to set up initial data.
Usage: python manage.py setup_nutritrack
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from meals.models import Food


SAMPLE_FOODS = [
    {"name": "Idli", "calories_per_100g": 58, "protein": 1.9, "carbs": 11.4, "fat": 0.3, "fiber": 0.1, "category": "grain"},
    {"name": "Dosa (Plain)", "calories_per_100g": 168, "protein": 3.4, "carbs": 25.5, "fat": 5.8, "fiber": 0.5, "category": "grain"},
    {"name": "Chapati / Roti", "calories_per_100g": 297, "protein": 7.7, "carbs": 52.9, "fat": 3.7, "fiber": 1.9, "category": "grain"},
    {"name": "Paneer", "calories_per_100g": 265, "protein": 18.3, "carbs": 1.2, "fat": 20.8, "fiber": 0.0, "category": "dairy"},
    {"name": "Boiled Egg (Whole)", "calories_per_100g": 155, "protein": 13.0, "carbs": 1.1, "fat": 11.0, "fiber": 0.0, "category": "non_veg"},
    {"name": "Cooked White Rice", "calories_per_100g": 130, "protein": 2.7, "carbs": 28.6, "fat": 0.3, "fiber": 0.4, "category": "grain"},
    {"name": "Chicken Breast (Cooked)", "calories_per_100g": 165, "protein": 31.0, "carbs": 0.0, "fat": 3.6, "fiber": 0.0, "category": "non_veg"},
    {"name": "Banana", "calories_per_100g": 89, "protein": 1.1, "carbs": 22.8, "fat": 0.3, "fiber": 2.6, "category": "fruit"},
    {"name": "Whole Milk", "calories_per_100g": 61, "protein": 3.2, "carbs": 4.8, "fat": 3.3, "fiber": 0.0, "category": "beverage"},
    {"name": "Dal (Cooked Lentils)", "calories_per_100g": 116, "protein": 9.0, "carbs": 20.0, "fat": 0.4, "fiber": 7.9, "category": "veg"},
    {"name": "Oats (Cooked)", "calories_per_100g": 71, "protein": 2.5, "carbs": 12.0, "fat": 1.5, "fiber": 1.7, "category": "grain"},
    {"name": "Greek Yogurt", "calories_per_100g": 59, "protein": 10.0, "carbs": 3.6, "fat": 0.4, "fiber": 0.0, "category": "dairy"},
    {"name": "Almonds", "calories_per_100g": 579, "protein": 21.2, "carbs": 21.6, "fat": 49.9, "fiber": 12.5, "category": "snack"},
    {"name": "Brown Rice (Cooked)", "calories_per_100g": 112, "protein": 2.6, "carbs": 23.5, "fat": 0.9, "fiber": 1.8, "category": "grain"},
    {"name": "Apple", "calories_per_100g": 52, "protein": 0.3, "carbs": 13.8, "fat": 0.2, "fiber": 2.4, "category": "fruit"},
]


class Command(BaseCommand):
    help = 'Set up NutriTrack with sample foods and optional demo user'

    def add_arguments(self, parser):
        parser.add_argument('--demo', action='store_true', help='Create demo user')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🥗 Setting up NutriTrack...'))

        # Load foods
        created = 0
        for food_data in SAMPLE_FOODS:
            _, was_created = Food.objects.get_or_create(
                name=food_data['name'],
                defaults=food_data
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Loaded {created} new foods ({Food.objects.count()} total)'))

        if options['demo']:
            user, was_created = User.objects.get_or_create(
                username='demo',
                defaults={
                    'email': 'demo@nutritrack.app',
                    'first_name': 'Demo',
                    'last_name': 'User',
                }
            )
            if was_created:
                user.set_password('demo1234')
                user.save()
                profile = user.profile
                profile.age = 25
                profile.gender = 'M'
                profile.height = 175
                profile.weight = 70
                profile.activity_level = 'moderate'
                profile.goal = 'maintain'
                profile.save()
                self.stdout.write(self.style.SUCCESS('✅ Demo user created (username: demo, password: demo1234)'))
            else:
                self.stdout.write('ℹ️  Demo user already exists')

        self.stdout.write(self.style.SUCCESS('\n🚀 Ready! Run: python manage.py runserver'))

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

from meals.models import Food

print(f'Total foods: {Food.objects.count()}')
print(f'Indian: {Food.objects.filter(cuisine="indian").count()}')
print(f'Chinese: {Food.objects.filter(cuisine="chinese").count()}')
print(f'Continental: {Food.objects.filter(cuisine="continental").count()}')
print(f'\nCategories:')
for cat, cat_name in Food.CATEGORY_CHOICES:
    count = Food.objects.filter(category=cat).count()
    print(f'  {cat_name}: {count}')

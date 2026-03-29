import os
import django
import json
from datetime import datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

# Read the existing fixture
with open('meals/fixtures/foods_comprehensive.json', 'r') as f:
    foods = json.load(f)

# Add created_at to each food
now = timezone.now().isoformat()
for food in foods:
    food['fields']['created_at'] = now

# Write back
with open('meals/fixtures/foods_comprehensive.json', 'w') as f:
    json.dump(foods, f, indent=2)

print(f"Updated {len(foods)} food items with timestamp")

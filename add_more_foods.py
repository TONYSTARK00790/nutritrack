#!/usr/bin/env python
"""
Script to add more comprehensive food data to the database
"""
import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

from meals.models import Food

# Additional foods to add
additional_foods = [
    {
        "name": "Quinoa (cooked)",
        "calories_per_100g": 120,
        "protein": 4.4,
        "carbs": 21.3,
        "fat": 1.9,
        "fiber": 2.6,
        "category": "grain",
        "cuisine": "general"
    },
    {
        "name": "Brown Rice (cooked)",
        "calories_per_100g": 111,
        "protein": 2.6,
        "carbs": 23.0,
        "fat": 0.9,
        "fiber": 1.8,
        "category": "grain",
        "cuisine": "general"
    },
    {
        "name": "Sweet Potato (baked)",
        "calories_per_100g": 90,
        "protein": 2.0,
        "carbs": 20.7,
        "fat": 0.1,
        "fiber": 3.8,
        "category": "vegetable",
        "cuisine": "general"
    },
    {
        "name": "Broccoli (steamed)",
        "calories_per_100g": 34,
        "protein": 2.8,
        "carbs": 7.2,
        "fat": 0.4,
        "fiber": 2.6,
        "category": "vegetable",
        "cuisine": "general"
    },
    {
        "name": "Spinach (raw)",
        "calories_per_100g": 23,
        "protein": 2.9,
        "carbs": 3.6,
        "fat": 0.4,
        "fiber": 2.2,
        "category": "vegetable",
        "cuisine": "general"
    },
    {
        "name": "Almonds",
        "calories_per_100g": 579,
        "protein": 21.2,
        "carbs": 21.6,
        "fat": 49.9,
        "fiber": 12.5,
        "category": "nut",
        "cuisine": "general"
    },
    {
        "name": "Greek Yogurt (plain, non-fat)",
        "calories_per_100g": 59,
        "protein": 10.3,
        "carbs": 3.6,
        "fat": 0.4,
        "fiber": 0.0,
        "category": "dairy",
        "cuisine": "general"
    },
    {
        "name": "Egg Whites",
        "calories_per_100g": 52,
        "protein": 11.1,
        "carbs": 0.7,
        "fat": 0.2,
        "fiber": 0.0,
        "category": "protein",
        "cuisine": "general"
    },
    {
        "name": "Turkey Breast (grilled)",
        "calories_per_100g": 135,
        "protein": 30.1,
        "carbs": 0.0,
        "fat": 1.0,
        "fiber": 0.0,
        "category": "protein",
        "cuisine": "general"
    },
    {
        "name": "Salmon (grilled)",
        "calories_per_100g": 206,
        "protein": 22.1,
        "carbs": 0.0,
        "fat": 12.4,
        "fiber": 0.0,
        "category": "protein",
        "cuisine": "general"
    },
    {
        "name": "Oatmeal (cooked)",
        "calories_per_100g": 68,
        "protein": 2.4,
        "carbs": 11.7,
        "fat": 1.4,
        "fiber": 1.7,
        "category": "grain",
        "cuisine": "general"
    },
    {
        "name": "Banana",
        "calories_per_100g": 89,
        "protein": 1.1,
        "carbs": 22.8,
        "fat": 0.3,
        "fiber": 2.6,
        "category": "fruit",
        "cuisine": "general"
    },
    {
        "name": "Blueberries",
        "calories_per_100g": 57,
        "protein": 0.7,
        "carbs": 14.5,
        "fat": 0.3,
        "fiber": 2.4,
        "category": "fruit",
        "cuisine": "general"
    },
    {
        "name": "Avocado",
        "calories_per_100g": 160,
        "protein": 2.0,
        "carbs": 8.5,
        "fat": 14.7,
        "fiber": 6.7,
        "category": "fruit",
        "cuisine": "general"
    },
    {
        "name": "Cottage Cheese (low-fat)",
        "calories_per_100g": 85,
        "protein": 12.4,
        "carbs": 2.7,
        "fat": 2.3,
        "fiber": 0.0,
        "category": "dairy",
        "cuisine": "general"
    },
    {
        "name": "Tuna (canned in water)",
        "calories_per_100g": 86,
        "protein": 19.4,
        "carbs": 0.0,
        "fat": 0.6,
        "fiber": 0.0,
        "category": "protein",
        "cuisine": "general"
    },
    {
        "name": "Lentils (cooked)",
        "calories_per_100g": 116,
        "protein": 9.0,
        "carbs": 20.1,
        "fat": 0.4,
        "fiber": 7.9,
        "category": "legume",
        "cuisine": "general"
    },
    {
        "name": "Chickpeas (cooked)",
        "calories_per_100g": 164,
        "protein": 7.6,
        "carbs": 27.4,
        "fat": 2.6,
        "fiber": 7.6,
        "category": "legume",
        "cuisine": "general"
    },
    {
        "name": "Whey Protein Powder",
        "calories_per_100g": 380,
        "protein": 80.0,
        "carbs": 6.0,
        "fat": 3.0,
        "fiber": 0.0,
        "category": "supplement",
        "cuisine": "general"
    },
    {
        "name": "Creatine Monohydrate",
        "calories_per_100g": 0,
        "protein": 0.0,
        "carbs": 0.0,
        "fat": 0.0,
        "fiber": 0.0,
        "category": "supplement",
        "cuisine": "general"
    }
]

def add_foods():
    added_count = 0
    for food_data in additional_foods:
        # Check if food already exists
        if not Food.objects.filter(name=food_data['name']).exists():
            Food.objects.create(**food_data)
            added_count += 1
            print(f"Added: {food_data['name']}")
        else:
            print(f"Skipped (exists): {food_data['name']}")

    print(f"\nTotal foods added: {added_count}")
    print(f"Total foods in database: {Food.objects.count()}")

if __name__ == '__main__':
    add_foods()
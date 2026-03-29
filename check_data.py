import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

from meals.models import Food, Meal
from django.db.models import Q, Sum

# Check if any foods have missing nutritional data
foods_with_missing_data = Food.objects.filter(
    Q(protein__isnull=True) | Q(carbs__isnull=True) | Q(fat__isnull=True) | 
    Q(protein=0) | Q(carbs=0) | Q(fat=0)
)
print(f"Foods with missing/zero nutritional data: {foods_with_missing_data.count()}")
for food in foods_with_missing_data.values('name', 'calories_per_100g', 'protein', 'carbs', 'fat')[:10]:
    print(f"  {food}")

# Check recent meals
recent_meals = Meal.objects.order_by('-created_at')[:5]
print("\nRecent meals:")
for meal in recent_meals:
    print(f"  {meal.food.name}: {meal.quantity}g -> {meal.total_calories} kcal")
    print(f"    Food: {meal.food.calories_per_100g} cal/100g, Protein: {meal.food.protein}g, Carbs: {meal.food.carbs}g, Fat: {meal.food.fat}g")
    print(f"    Meal: {meal.total_protein}g protein, {meal.total_carbs}g carbs, {meal.total_fat}g fat\n")

# Check all foods
print(f"\nTotal foods in database: {Food.objects.count()}")
all_foods_summary = Food.objects.filter(protein=0).count()
print(f"Foods with protein=0: {all_foods_summary}")

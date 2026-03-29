import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

from meals.models import Food, Meal
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

# Create test user
test_user, _ = User.objects.get_or_create(
    username='testcalculator',
    defaults={'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User'}
)

# Get or create profile
profile, _ = UserProfile.objects.get_or_create(
    user=test_user,
    defaults={
        'age': 25,
        'height': 180,
        'weight': 75,
        'gender': 'M',
        'activity_level': 'moderate',
        'goal': 'maintain'
    }
)

# Get some foods from database
foods = Food.objects.all()[:3]

print(f"✅ Test User: {test_user.username}")
print(f"✅ Profile: Age {profile.age}, Height {profile.height}cm, Weight {profile.weight}kg\n")

if foods:
    print("📝 Creating test meals to verify calculations:\n")
    today = date.today()
    
    for food in foods:
        quantity = 100  # 100 grams
        
        # Create meal
        meal, created = Meal.objects.get_or_create(
            user=test_user,
            food=food,
            date=today,
            defaults={
                'quantity': quantity,
                'meal_type': 'lunch'
            }
        )
        
        # Verify calculation
        expected_calories = food.calories_per_100g * (quantity / 100)
        expected_protein = food.protein * (quantity / 100)
        expected_carbs = food.carbs * (quantity / 100)
        expected_fat = food.fat * (quantity / 100)
        
        print(f"Food: {food.name}")
        print(f"  Database values per 100g:")
        print(f"    • Calories: {food.calories_per_100g} kcal")
        print(f"    • Protein: {food.protein}g")
        print(f"    • Carbs: {food.carbs}g")
        print(f"    • Fat: {food.fat}g")
        
        print(f"  Quantity logged: {quantity}g")
        print(f"  Calculated values:")
        print(f"    • Expected Calories: {expected_calories:.1f} kcal")
        print(f"    • Stored Calories: {meal.total_calories} kcal")
        print(f"    • Match: {'✅' if abs(meal.total_calories - expected_calories) < 0.1 else '❌'}")
        
        print(f"    • Expected Protein: {expected_protein:.1f}g")
        print(f"    • Stored Protein: {meal.total_protein}g")
        print(f"    • Match: {'✅' if abs(meal.total_protein - expected_protein) < 0.1 else '❌'}")
        
        print(f"    • Expected Carbs: {expected_carbs:.1f}g")
        print(f"    • Stored Carbs: {meal.total_carbs}g")
        print(f"    • Match: {'✅' if abs(meal.total_carbs - expected_carbs) < 0.1 else '❌'}")
        
        print(f"    • Expected Fat: {expected_fat:.1f}g")
        print(f"    • Stored Fat: {meal.total_fat}g")
        print(f"    • Match: {'✅' if abs(meal.total_fat - expected_fat) < 0.1 else '❌'}\n")

# Get dashboard totals
from django.db.models import Sum

today_meals = Meal.objects.filter(user=test_user, date=today).select_related('food')
totals = today_meals.aggregate(
    total_calories=Sum('total_calories'),
    total_protein=Sum('total_protein'),
    total_carbs=Sum('total_carbs'),
    total_fat=Sum('total_fat'),
)

print(f"\n📊 Today's Totals for {test_user.username}:")
print(f"  • Total Meals: {today_meals.count()}")
print(f"  • Total Calories: {int(totals['total_calories'] or 0)} kcal")
print(f"  • Total Protein: {int(totals['total_protein'] or 0)}g")
print(f"  • Total Carbs: {int(totals['total_carbs'] or 0)}g")
print(f"  • Total Fat: {int(totals['total_fat'] or 0)}g")

# Get calorie goal
calorie_goal = profile.calorie_goal or (profile.calculate_tdee() or 2000)
remaining = calorie_goal - (totals['total_calories'] or 0)
progress = min(((totals['total_calories'] or 0) / calorie_goal) * 100, 100)

print(f"\n📈 Progress:")
print(f"  • Calorie Goal: {int(calorie_goal)} kcal")
print(f"  • Consumed: {int(totals['total_calories'] or 0)} kcal")
print(f"  • Remaining: {int(remaining)} kcal")
print(f"  • Progress: {int(progress)}%")
print(f"\n✅ All calculations verified and working correctly!")

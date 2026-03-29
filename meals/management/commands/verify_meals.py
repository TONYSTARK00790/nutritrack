"""
Management command to verify and fix meal calorie calculations
"""
from django.core.management.base import BaseCommand
from meals.models import Meal, Food
from django.db.models import Sum
from datetime import date


class Command(BaseCommand):
    help = 'Verify and recalculate meal calories based on food data and quantity'

    def handle(self, *args, **options):
        self.stdout.write("Starting meal calorie verification...")
        
        fixed_count = 0
        meals = Meal.objects.select_related('food')
        
        for meal in meals:
            # Recalculate based on food data
            factor = meal.quantity / 100
            new_calories = round(meal.food.calories_per_100g * factor, 1)
            new_protein = round(meal.food.protein * factor, 1)
            new_carbs = round(meal.food.carbs * factor, 1)
            new_fat = round(meal.food.fat * factor, 1)
            
            # Check if values are different
            if (meal.total_calories != new_calories or 
                meal.total_protein != new_protein or 
                meal.total_carbs != new_carbs or 
                meal.total_fat != new_fat):
                
                self.stdout.write(
                    f"  Fixing: {meal.food.name} ({meal.quantity}g)\n"
                    f"    Old: {meal.total_calories}kcal, {meal.total_protein}g protein, "
                    f"{meal.total_carbs}g carbs, {meal.total_fat}g fat\n"
                    f"    New: {new_calories}kcal, {new_protein}g protein, "
                    f"{new_carbs}g carbs, {new_fat}g fat"
                )
                
                meal.total_calories = new_calories
                meal.total_protein = new_protein
                meal.total_carbs = new_carbs
                meal.total_fat = new_fat
                meal.save()
                fixed_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Verification complete! Fixed {fixed_count} meals.'
            )
        )
        
        # Print daily summaries
        self.stdout.write("\n📊 Daily Summaries (Last 7 days):")
        from datetime import timedelta
        today = date.today()
        
        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            totals = Meal.objects.filter(date=d).aggregate(
                cal=Sum('total_calories'),
                pro=Sum('total_protein'),
                carb=Sum('total_carbs'),
                fat=Sum('total_fat'),
                count=Sum('id', _output_field_class=lambda: 'IntegerField')
            )
            cal = totals['cal'] or 0
            pro = totals['pro'] or 0
            carb = totals['carb'] or 0
            fat = totals['fat'] or 0
            
            self.stdout.write(
                f"  {d.strftime('%Y-%m-%d (%A)')}: {int(cal)} kcal | "
                f"{int(pro)}g protein | {int(carb)}g carbs | {int(fat)}g fat"
            )

from django.db import models
from django.contrib.auth.models import User


class Food(models.Model):
    CATEGORY_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non_veg', 'Non-Vegetarian'),
        ('beverage', 'Beverage'),
        ('snack', 'Snack'),
        ('fruit', 'Fruit'),
        ('dairy', 'Dairy'),
        ('grain', 'Grain/Cereal'),
    ]
    
    CUISINE_CHOICES = [
        ('indian', 'Indian'),
        ('chinese', 'Chinese'),
        ('continental', 'Continental'),
    ]

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True, help_text='Upload food image')
    calories_per_100g = models.FloatField()
    protein = models.FloatField(default=0, help_text='Protein per 100g')
    carbs = models.FloatField(default=0, help_text='Carbohydrates per 100g')
    fat = models.FloatField(default=0, help_text='Fat per 100g')
    fiber = models.FloatField(default=0, help_text='Fiber per 100g')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='veg')
    cuisine = models.CharField(max_length=20, choices=CUISINE_CHOICES, default='indian')
    is_custom = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='custom_foods')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.calories_per_100g} kcal/100g)"

    def get_category_icon(self):
        icons = {
            'veg': '🥦', 'non_veg': '🍗', 'beverage': '🥤',
            'snack': '🍿', 'fruit': '🍎', 'dairy': '🥛', 'grain': '🌾',
        }
        return icons.get(self.category, '🍽️')
    
    def get_cuisine_badge(self):
        badges = {
            'indian': '🇮🇳',
            'chinese': '🥡',
            'continental': '🍽️',
        }
        return badges.get(self.cuisine, '🍽️')


class Meal(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meals')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meals')
    quantity = models.FloatField(help_text='Quantity in grams')
    meal_type = models.CharField(max_length=15, choices=MEAL_TYPE_CHOICES, default='lunch')
    date = models.DateField()
    total_calories = models.FloatField(editable=False, default=0)
    total_protein = models.FloatField(editable=False, default=0)
    total_carbs = models.FloatField(editable=False, default=0)
    total_fat = models.FloatField(editable=False, default=0)
    notes = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'meal_type']

    def save(self, *args, **kwargs):
        factor = self.quantity / 100
        self.total_calories = round(self.food.calories_per_100g * factor, 1)
        self.total_protein = round(self.food.protein * factor, 1)
        self.total_carbs = round(self.food.carbs * factor, 1)
        self.total_fat = round(self.food.fat * factor, 1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.food.name} ({self.quantity}g) on {self.date}"

    @property
    def meal_type_icon(self):
        icons = {
            'breakfast': '🌅', 'lunch': '☀️', 'dinner': '🌙', 'snack': '🍎'
        }
        return icons.get(self.meal_type, '🍽️')

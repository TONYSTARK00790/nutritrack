from django.contrib import admin
from .models import Food, Meal


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'calories_per_100g', 'protein', 'carbs', 'fat', 'category', 'cuisine', 'has_image', 'is_custom']
    list_filter = ['category', 'cuisine', 'is_custom']
    search_fields = ['name']
    ordering = ['name']
    fieldsets = (
        ('Food Information', {
            'fields': ('name', 'category', 'cuisine', 'is_custom')
        }),
        ('Nutritional Data (per 100g)', {
            'fields': ('calories_per_100g', 'protein', 'carbs', 'fat', 'fiber')
        }),
    )
    
    def has_image(self, obj):
        return obj.image and obj.image.url
    has_image.short_description = 'Has Image'
    has_image.boolean = True


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['user', 'food', 'quantity', 'meal_type', 'date', 'total_calories']
    list_filter = ['meal_type', 'date']
    search_fields = ['user__username', 'food__name']
    date_hierarchy = 'date'

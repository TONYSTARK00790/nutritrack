from django import forms
from .models import Meal, Food


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['food', 'quantity', 'meal_type', 'date', 'notes']
        widgets = {
            'food': forms.Select(attrs={'class': 'hidden', 'id': 'id_food'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'nt-input', 'placeholder': 'Grams (e.g. 150)',
                'min': '1', 'max': '2000', 'step': '0.5'
            }),
            'meal_type': forms.Select(attrs={'class': 'nt-input'}),
            'date': forms.DateInput(attrs={'class': 'nt-input', 'type': 'date'}),
            'notes': forms.TextInput(attrs={'class': 'nt-input', 'placeholder': 'Optional note...'}),
        }


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'calories_per_100g', 'protein', 'carbs', 'fat', 'fiber', 'category', 'cuisine']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'nt-input', 'placeholder': 'Food name'}),
            'calories_per_100g': forms.NumberInput(attrs={
                'class': 'nt-input', 'placeholder': 'kcal per 100g', 'step': '0.1'
            }),
            'protein': forms.NumberInput(attrs={'class': 'nt-input', 'placeholder': 'g', 'step': '0.1'}),
            'carbs': forms.NumberInput(attrs={'class': 'nt-input', 'placeholder': 'g', 'step': '0.1'}),
            'fat': forms.NumberInput(attrs={'class': 'nt-input', 'placeholder': 'g', 'step': '0.1'}),
            'fiber': forms.NumberInput(attrs={'class': 'nt-input', 'placeholder': 'g', 'step': '0.1'}),
            'category': forms.Select(attrs={'class': 'nt-input'}),
            'cuisine': forms.Select(attrs={'class': 'nt-input'}),
        }

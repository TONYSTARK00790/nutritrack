from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum
from datetime import date, timedelta
import json

from .models import Food, Meal
from .forms import MealForm, FoodForm


@login_required
def meal_list(request):
    selected_date_str = request.GET.get('date', date.today().isoformat())
    try:
        selected_date = date.fromisoformat(selected_date_str)
    except ValueError:
        selected_date = date.today()

    meals = Meal.objects.filter(user=request.user, date=selected_date).select_related('food')
    totals = meals.aggregate(
        cal=Sum('total_calories'), pro=Sum('total_protein'),
        carb=Sum('total_carbs'), fat=Sum('total_fat')
    )

    # Group by meal type
    grouped = {}
    for mt_code, mt_label in Meal.MEAL_TYPE_CHOICES:
        mt_meals = meals.filter(meal_type=mt_code)
        grouped[mt_code] = {
            'label': mt_label,
            'icon': {'breakfast': '🌅', 'lunch': '☀️', 'dinner': '🌙', 'snack': '🍎'}.get(mt_code),
            'meals': mt_meals,
            'total_cal': round(mt_meals.aggregate(t=Sum('total_calories'))['t'] or 0),
        }

    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)

    return render(request, 'meals/meal_list.html', {
        'selected_date': selected_date,
        'grouped': grouped,
        'totals': {k: round(v or 0) for k, v in totals.items()},
        'prev_date': prev_date,
        'next_date': next_date,
        'is_today': selected_date == date.today(),
    })


@login_required
def nutrition_unified(request):
    """Unified nutrition dashboard combining meals, norms, and food library"""
    selected_date_str = request.GET.get('date', date.today().isoformat())
    try:
        selected_date = date.fromisoformat(selected_date_str)
    except ValueError:
        selected_date = date.today()

    meals = Meal.objects.filter(user=request.user, date=selected_date).select_related('food')
    totals = meals.aggregate(
        cal=Sum('total_calories'), pro=Sum('total_protein'),
        carb=Sum('total_carbs'), fat=Sum('total_fat')
    )

    # Group by meal type
    grouped = {}
    for mt_code, mt_label in Meal.MEAL_TYPE_CHOICES:
        mt_meals = meals.filter(meal_type=mt_code)
        grouped[mt_code] = {
            'label': mt_label,
            'icon': {'breakfast': '🌅', 'lunch': '☀️', 'dinner': '🌙', 'snack': '🍎'}.get(mt_code),
            'meals': mt_meals,
            'total_cal': round(mt_meals.aggregate(t=Sum('total_calories'))['t'] or 0),
        }

    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)

    return render(request, 'meals/nutrition_unified.html', {
        'selected_date': selected_date,
        'grouped': grouped,
        'totals': {k: round(v or 0) for k, v in totals.items()},
        'prev_date': prev_date,
        'next_date': next_date,
        'is_today': selected_date == date.today(),
    })


@login_required
def add_meal(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            messages.success(request, f'✅ {meal.food.name} added to your {meal.get_meal_type_display()}!')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Meal added!'})
            return redirect('meal_list')
    else:
        initial = {
            'date': request.GET.get('date', date.today()),
            'meal_type': request.GET.get('meal_type', 'lunch'),
        }
        food_id = request.GET.get('food')
        if food_id:
            try:
                initial['food'] = int(food_id)
            except (ValueError, TypeError):
                pass

        form = MealForm(initial=initial)
    
    foods = Food.objects.all()
    
    # Get suggested foods for each meal type
    suggestions = {
        'breakfast': Food.objects.filter(Q(category__in=['fruit', 'dairy', 'grain']) | Q(name__icontains='cereal')).order_by('?')[:5],
        'lunch': Food.objects.filter(Q(category__in=['veg', 'non_veg', 'grain'])).order_by('?')[:5],
        'dinner': Food.objects.filter(Q(category__in=['veg', 'non_veg', 'grain'])).order_by('?')[:5],
        'snack': Food.objects.filter(category__in=['fruit', 'snack', 'dairy']).order_by('?')[:5],
        'evening_snack': Food.objects.filter(category__in=['fruit', 'snack', 'beverage']).order_by('?')[:5],
    }
    
    return render(request, 'meals/add_meal.html', {
        'form': form,
        'foods': foods,
        'suggestions': suggestions,
    })


@login_required
def edit_meal(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meal updated!')
            return redirect('meal_list')
    else:
        form = MealForm(instance=meal)
    return render(request, 'meals/add_meal.html', {'form': form, 'meal': meal, 'edit': True})


@login_required
def adjust_quantity(request, pk):
    """AJAX endpoint to quickly adjust meal quantity"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        meal = get_object_or_404(Meal, pk=pk, user=request.user)
        adjustment = int(request.POST.get('adjustment', 0))
        
        new_quantity = max(1, meal.quantity + adjustment)  # Minimum 1g
        meal.quantity = new_quantity
        meal.save()
        
        return JsonResponse({
            'success': True,
            'quantity': meal.quantity,
            'calories': round(meal.total_calories, 1),
            'protein': round(meal.total_protein, 1),
            'carbs': round(meal.total_carbs, 1),
            'fat': round(meal.total_fat, 1),
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def delete_meal(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == 'POST':
        food_name = meal.food.name
        meal.delete()
        messages.success(request, f'{food_name} removed from your log.')
    return redirect(f'/meals/?date={meal.date}')


@login_required
def food_database(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    cuisine = request.GET.get('cuisine', '')
    foods = Food.objects.all()
    if query:
        foods = foods.filter(Q(name__icontains=query) | Q(category__icontains=query))
    if category:
        foods = foods.filter(category=category)
    if cuisine:
        foods = foods.filter(cuisine=cuisine)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = [{
            'id': f.id, 'name': f.name,
            'calories': f.calories_per_100g,
            'protein': f.protein, 'carbs': f.carbs,
            'fat': f.fat, 'category': f.get_category_display(),
            'cuisine': f.get_cuisine_badge(),
            'icon': f.get_category_icon(),
        } for f in foods]
        return JsonResponse({'foods': data})
    return render(request, 'meals/food_database.html', {
        'foods': foods, 'query': query, 'category': category, 'cuisine': cuisine,
        'categories': Food.CATEGORY_CHOICES,
        'cuisines': Food.CUISINE_CHOICES,
    })


@login_required
def add_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            food.is_custom = True
            food.created_by = request.user
            food.save()
            messages.success(request, f'✅ {food.name} added to the database!')
            return redirect('food_database')
    else:
        form = FoodForm()
    return render(request, 'meals/add_food.html', {'form': form})


@login_required
def food_detail_api(request, pk):
    food = get_object_or_404(Food, pk=pk)
    return JsonResponse({
        'id': food.id, 'name': food.name,
        'calories_per_100g': food.calories_per_100g,
        'protein': food.protein, 'carbs': food.carbs,
        'fat': food.fat, 'category': food.get_category_display(),
    })

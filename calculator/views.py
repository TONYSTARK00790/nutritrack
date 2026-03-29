from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json


@login_required
def calculator_view(request):
    result = None
    if request.method == 'POST':
        try:
            age = int(request.POST.get('age', 0))
            gender = request.POST.get('gender', 'M')
            height = float(request.POST.get('height', 0))
            weight = float(request.POST.get('weight', 0))
            activity = request.POST.get('activity_level', 'moderate')

            if gender == 'M':
                bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
            else:
                bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

            multipliers = {
                'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55,
                'active': 1.725, 'very_active': 1.9,
            }
            tdee = bmr * multipliers.get(activity, 1.55)

            result = {
                'bmr': round(bmr),
                'maintenance': round(tdee),
                'fat_loss': round(tdee - 500),
                'muscle_gain': round(tdee + 500),
                'protein_g': round((tdee * 0.30) / 4),
                'carbs_g': round((tdee * 0.40) / 4),
                'fat_g': round((tdee * 0.30) / 9),
                # Aggressive fat loss
                'aggressive_loss': round(tdee - 1000),
                # Mild surplus
                'mild_gain': round(tdee + 250),
                'bmi': round(weight / ((height / 100) ** 2), 1),
                'weight': weight,
                'height': height,
                'age': age,
                'gender': gender,
                'activity': activity,
            }

            bmi = result['bmi']
            if bmi < 18.5:
                result['bmi_cat'] = 'Underweight'
                result['bmi_color'] = '#3b82f6'
            elif bmi < 25:
                result['bmi_cat'] = 'Normal Weight'
                result['bmi_color'] = '#22c55e'
            elif bmi < 30:
                result['bmi_cat'] = 'Overweight'
                result['bmi_color'] = '#f59e0b'
            else:
                result['bmi_cat'] = 'Obese'
                result['bmi_color'] = '#ef4444'

            if request.user.is_authenticated and request.POST.get('save_to_profile'):
                profile = request.user.profile
                profile.age = age
                profile.gender = gender
                profile.height = height
                profile.weight = weight
                profile.activity_level = activity
                profile.calorie_goal = result['maintenance']
                profile.save()

        except (ValueError, ZeroDivisionError) as e:
            result = {'error': str(e)}

    # Pre-fill with profile data
    profile_data = {}
    if request.user.is_authenticated:
        p = request.user.profile
        profile_data = {
            'age': p.age or '',
            'gender': p.gender or 'M',
            'height': p.height or '',
            'weight': p.weight or '',
            'activity_level': p.activity_level or 'moderate',
        }

    return render(request, 'calculator/calculator.html', {
        'result': result,
        'profile_data': profile_data,
    })

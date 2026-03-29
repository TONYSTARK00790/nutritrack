from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from datetime import timedelta, date
import json

from .models import UserProfile, ChatSession, ChatMessage
from .forms import RegisterForm, LoginForm, ProfileForm
from .enhanced_chatbot import SmartNutritionChatbot, get_initial_response as get_enhanced_initial, get_bot_response as get_enhanced_bot_response
from meals.models import Meal, Food


def get_workouts_for_goal(profile: UserProfile):
    # Detailed workout suggestions mapped by preferred workout type and goal
    level = profile.activity_level or 'moderate'
    wt = getattr(profile, 'preferred_workout_type', 'balanced') or 'balanced'

    # Example sets for each type. These lists can be expanded later or moved to DB.
    hypertrophy = [
        {'name': 'Push Hypertrophy', 'duration_min': 50, 'desc': 'Chest/Shoulders/Triceps, 8-12 reps, 3-4 sets.'},
        {'name': 'Pull Hypertrophy', 'duration_min': 50, 'desc': 'Back/Biceps, 8-12 reps, 3-4 sets.'},
        {'name': 'Leg Hypertrophy', 'duration_min': 60, 'desc': 'Quads/Hamstrings/Glutes, 8-12 reps, 3-4 sets.'},
        {'name': 'Upper/Lower Split', 'duration_min': 55, 'desc': 'Alternating upper and lower body hypertrophy sessions.'},
        {'name': 'Isolation Focus', 'duration_min': 35, 'desc': 'Target weak points with strict form.'},
    ]

    strength = [
        {'name': 'Strength Day: Squat Focus', 'duration_min': 60, 'desc': 'Heavy squats 3-6 reps, accessory work.'},
        {'name': 'Strength Day: Deadlift/Posterior', 'duration_min': 60, 'desc': 'Deadlifts, Romanian DLs, glute work.'},
        {'name': 'Strength Day: Press', 'duration_min': 55, 'desc': 'Bench/Overhead press heavy sets 3-6 reps.'},
        {'name': 'Power/Explosiveness', 'duration_min': 40, 'desc': 'Olympic lift variations, plyometrics.'},
        {'name': 'Compound Focus Circuit', 'duration_min': 50, 'desc': 'Low-rep compound superset training.'},
    ]

    endurance = [
        {'name': 'Long Run/Row', 'duration_min': 45, 'desc': 'Steady-state cardio 40–60 minutes.'},
        {'name': 'Fartlek Intervals', 'duration_min': 35, 'desc': 'Speed play intervals for endurance and speed.'},
        {'name': 'Tempo Ride', 'duration_min': 50, 'desc': 'Sustained moderate-hard effort on bike.'},
        {'name': 'Endurance Circuits', 'duration_min': 40, 'desc': 'Low-rest bodyweight circuits for stamina.'},
        {'name': 'Rowing Pyramid', 'duration_min': 30, 'desc': 'Interval pyramid sessions on rower.'},
    ]

    balanced = [
        {'name': 'Balanced Mix A', 'duration_min': 35, 'desc': '20 min cardio + 15 min full-body strength.'},
        {'name': 'Circuit Combo', 'duration_min': 30, 'desc': 'Circuit mixing strength and conditioning.'},
        {'name': 'Mobility + Core', 'duration_min': 25, 'desc': 'Recovery and stability work.'},
    ]

    # Select base list by workout type
    mapping = {
        'hypertrophy': hypertrophy,
        'strength': strength,
        'endurance': endurance,
        'balanced': balanced,
    }
    base = mapping.get(wt, balanced)

    # Tailor a bit by goal (e.g., if user wants to lose, give more cardio options)
    result = []
    if profile.goal == 'lose':
        # prioritize endurance + circuits
        result = endurance[:3] + balanced[:2] if wt != 'endurance' else endurance
    elif profile.goal == 'gain':
        # prioritize hypertrophy/strength
        if wt == 'strength':
            result = strength + hypertrophy[:2]
        elif wt == 'hypertrophy':
            result = hypertrophy + strength[:2]
        else:
            result = hypertrophy[:3] + strength[:2]
    else:
        # maintain -> balanced mix but include preferred
        result = base + balanced

    # Add intensity tag based on activity level
    intensity = 'Moderate'
    if level in ('sedentary', 'light'):
        intensity = 'Beginner'
    elif level in ('active', 'very_active'):
        intensity = 'Advanced'
    for w in result:
        w['intensity'] = intensity
    return result


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to NutriTrack, {user.first_name}! 🎉')
            return redirect('accounts:profile')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}! 💪')
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # auto-calc calorie goal if left blank or to align with chosen goal
            targets = profile.get_calorie_targets()
            if targets:
                if not profile.calorie_goal:
                    if profile.goal == 'lose':
                        profile.calorie_goal = targets.get('fat_loss')
                    elif profile.goal == 'gain':
                        profile.calorie_goal = targets.get('muscle_gain')
                    else:
                        profile.calorie_goal = targets.get('maintenance')
                profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)

    targets = profile.get_calorie_targets()
    workouts = get_workouts_for_goal(profile)
    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile,
        'targets': targets,
        'workouts': workouts,
    })




@login_required
def training_style_view(request):
    """Allow users to customize their preferred training style."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        training_style = request.POST.get('training_style')
        if training_style in dict(UserProfile.TRAINING_STYLE_CHOICES):
            profile.training_style = training_style
            profile.save()
            messages.success(request, f'Training style updated to {profile.get_training_style_display()}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid training style selected.')
    
    # Get workouts filtered by training style
    from workouts.models import Workout
    
    style_workouts = {}
    
    # Jeff Nippard workouts
    style_workouts['jeff_nippard'] = {
        'name': 'Jeff Nippard - Science-Based Training',
        'desc': 'Evidence-based, moderate intensity, technical proficiency focus',
        'icon': '🧬',
        'features': ['Moderate intensity', 'Controlled tempo', 'Technical proficiency', 'Balanced volume'],
        'workouts': Workout.objects.filter(name__icontains='Nippard')[:4],
    }
    
    # Arnold Golden Era workouts
    style_workouts['arnold_golden'] = {
        'name': 'Arnold Golden Era - High Volume Bodybuilding',
        'desc': 'Classic split routines with multiple angles and pump focus',
        'icon': '🏆',
        'features': ['High volume', 'Multiple angles', 'Pump focus', '60-80 min sessions'],
        'workouts': Workout.objects.filter(name__icontains='Arnold')[:4],
    }
    
    # Ronnie Coleman workouts
    style_workouts['ronnie_coleman'] = {
        'name': 'Ronnie Coleman - Hardcore High Volume',
        'desc': 'Extreme volume, minimal rest, massive intensity',
        'icon': '💪',
        'features': ['Extreme volume', 'Heavy compounds', 'Minimal rest', '75-90 min sessions'],
        'workouts': Workout.objects.filter(name__icontains='Ronnie')[:4],
    }
    
    # Mixed style
    style_workouts['mixed'] = {
        'name': 'Mixed - Variety of All Styles',
        'desc': 'Combine all training philosophies for complete development',
        'icon': '🔄',
        'features': ['Variety', 'All philosophies', 'Flexibility', 'Balanced approach'],
        'workouts': Workout.objects.all()[:4],
    }
    
    context = {
        'profile': profile,
        'style_workouts': style_workouts,
        'current_style': profile.training_style,
    }
    return render(request, 'accounts/training_style.html', context)


@login_required
def dashboard_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    today = date.today()

    # Profile form for onboarding modal
    profile_form = ProfileForm(instance=profile)

    # Today's meals
    today_meals = Meal.objects.filter(user=request.user, date=today).select_related('food')

    # Aggregated totals
    today_totals = today_meals.aggregate(
        total_calories=Sum('total_calories'),
        total_protein=Sum('total_protein'),
        total_carbs=Sum('total_carbs'),
        total_fat=Sum('total_fat'),
    )

    calories_consumed = round(today_totals['total_calories'] or 0)
    protein_consumed = round(today_totals['total_protein'] or 0)
    carbs_consumed = round(today_totals['total_carbs'] or 0)
    fat_consumed = round(today_totals['total_fat'] or 0)

    # Clean stats for dashboard display (divide by 1000 for display)
    today_nutrition = {
        'calories': round(calories_consumed / 1000, 1) if calories_consumed > 0 else 0,
        'protein': protein_consumed,
        'carbs': carbs_consumed,
    }

    context = {
        'profile': profile,
        'profile_form': profile_form,
        'today': today,
        'today_nutrition': today_nutrition,
    }
    return render(request, 'dashboard_clean.html', context)


@login_required
def toggle_dark_mode(request):
    profile = request.user.profile
    profile.dark_mode = not profile.dark_mode
    profile.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


@login_required
def create_chat_session(request):
    """Create a new chat session and return the initial bot response."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        reason = data.get('reason')
        
        if reason not in dict(ChatSession.REASON_CHOICES):
            return JsonResponse({'error': 'Invalid reason'}, status=400)
        
        session = ChatSession.objects.create(user=request.user, reason=reason)
        
        # Use enhanced chatbot with user data
        try:
            bot = SmartNutritionChatbot(request.user)
            initial_msg = bot.get_initial_response(reason)
        except Exception:
            # Fallback to basic response if enhanced fails
            initial_msg = get_initial_response(reason)
        
        bot_msg = ChatMessage.objects.create(session=session, role='bot', message=initial_msg)
        
        return JsonResponse({
            'status': 'ok',
            'session_id': session.pk,
            'initial_message': initial_msg,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def send_chat_message(request):
    """Send a user message and get a contextual bot response based on message content."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        user_message = data.get('message', '').strip()
        
        session = ChatSession.objects.get(pk=session_id, user=request.user)
        
        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)
        
        # Save user message
        ChatMessage.objects.create(session=session, role='user', message=user_message)
        
        # Get contextual bot response using enhanced chatbot with user data
        message_count = session.messages.filter(role='bot').count()
        try:
            bot = SmartNutritionChatbot(request.user)
            # PASS THE REASON so bot prioritizes the right topic!
            bot_response = bot.get_response(user_message, reason=session.reason)
        except Exception:
            # Fallback to basic response if enhanced fails
            bot_response = get_bot_response(session.reason, user_message, message_count)
        
        bot_msg = ChatMessage.objects.create(session=session, role='bot', message=bot_response)
        
        return JsonResponse({
            'status': 'ok',
            'bot_message': bot_response,
        })
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


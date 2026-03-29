from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q, Sum
from datetime import date, timedelta
import json

from .models import Workout, UserWorkoutSession, WorkoutLog, ExerciseSetLog, CustomWorkoutRoutine
from .forms import CustomWorkoutRoutineForm, AddWorkoutToRoutineForm


def workout_list(request):
    wtype = request.GET.get('type')
    if wtype:
        workouts = Workout.objects.filter(workout_type=wtype)
    else:
        workouts = Workout.objects.all()
    return render(request, 'workouts/list.html', {'workouts': workouts, 'selected_type': wtype})


def workout_detail(request, pk):
    w = get_object_or_404(Workout, pk=pk)
    return render(request, 'workouts/detail.html', {'workout': w})


@login_required
def start_workout(request, pk):
    w = get_object_or_404(Workout, pk=pk)
    if request.method == 'POST':
        session = UserWorkoutSession.objects.create(user=request.user, workout=w, scheduled_at=timezone.now())
        return redirect('workouts:detail', pk=pk)
    return redirect('workouts:detail', pk=pk)


@login_required
def sessions_list(request):
    sessions = request.user.workout_sessions.select_related('workout').all()
    return render(request, 'workouts/sessions_list.html', {'sessions': sessions})


@login_required
def mark_complete(request, pk):
    session = get_object_or_404(UserWorkoutSession, pk=pk, user=request.user)
    if request.method == 'POST':
        session.mark_complete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'ok',
                'pk': session.pk,
                'completed_at': session.completed_at.isoformat() if session.completed_at else None,
            })
    return redirect('workouts:sessions')


@login_required
def all_workouts(request):
    """Browse all workouts with filtering by type and search"""
    workout_type = request.GET.get('type', '')
    search_query = request.GET.get('q', '')
    
    # Start with all workouts
    if workout_type:
        workouts = Workout.objects.filter(workout_type=workout_type)
    else:
        workouts = Workout.objects.all()
    
    # Apply search filter if provided
    if search_query:
        workouts = workouts.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Group workouts by type for display
    grouped = {}
    for type_code, type_name in Workout.WORKOUT_TYPE_CHOICES:
        if workout_type:
            # If filtering by type, only show selected type
            grouped[type_code] = {
                'name': type_name,
                'icon': {'hypertrophy': '💪', 'strength': '🏋️', 'endurance': '🏃', 'balanced': '⚖️'}.get(type_code, '🏋️'),
                'workouts': workouts.filter(workout_type=type_code) if type_code == workout_type else Workout.objects.none()
            }
        else:
            # Show all types grouped
            filtered = Workout.objects.filter(workout_type=type_code)
            if search_query:
                filtered = filtered.filter(
                    Q(name__icontains=search_query) | 
                    Q(description__icontains=search_query)
                )
            grouped[type_code] = {
                'name': type_name,
                'icon': {'hypertrophy': '💪', 'strength': '🏋️', 'endurance': '🏃', 'balanced': '⚖️'}.get(type_code, '🏋️'),
                'workouts': filtered
            }
    
    return render(request, 'workouts/all_workouts.html', {
        'grouped': grouped,
        'selected_type': workout_type,
        'search_query': search_query,
    })


@login_required
def log_workout(request, pk):
    """Log a workout with exercise sets"""
    workout = get_object_or_404(Workout, pk=pk)
    
    if request.method == 'POST':
        # Create a new workout log
        workout_log = WorkoutLog.objects.create(
            user=request.user,
            workout=workout,
            date=date.today(),
            duration_minutes=request.POST.get('duration_minutes', workout.duration_min),
            notes=request.POST.get('notes', '')
        )
        
        # Process exercise sets from form
        exercise_data = request.POST.get('exercises_json')
        if exercise_data:
            try:
                exercises = json.loads(exercise_data)
                for exercise_name, sets_data in exercises.items():
                    for set_num, set_info in enumerate(sets_data, 1):
                        ExerciseSetLog.objects.create(
                            workout_log=workout_log,
                            exercise_name=exercise_name,
                            set_number=set_num,
                            weight_kg=float(set_info.get('weight', 0)) or None,
                            reps=int(set_info.get('reps', 0)),
                            notes=set_info.get('notes', '')
                        )
            except (json.JSONDecodeError, ValueError):
                pass
        
        return redirect('workouts:history')
    
    return render(request, 'workouts/log_workout.html', {'workout': workout})


@login_required
def workout_history(request):
    """View user's workout history"""
    selected_date_str = request.GET.get('date', date.today().isoformat())
    try:
        selected_date = date.fromisoformat(selected_date_str)
    except ValueError:
        selected_date = date.today()
    
    # Get workout logs for the selected date
    logs = WorkoutLog.objects.filter(user=request.user, date=selected_date).select_related('workout').prefetch_related('exercise_sets')
    
    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)
    
    return render(request, 'workouts/history.html', {
        'logs': logs,
        'selected_date': selected_date,
        'prev_date': prev_date,
        'next_date': next_date,
        'is_today': selected_date == date.today(),
    })


@login_required
def create_custom_routine(request):
    """Create a new custom workout routine (empty, no workouts yet)"""
    if request.method == 'POST':
        form = CustomWorkoutRoutineForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.user = request.user
            routine.save()
            from django.contrib import messages
            messages.success(request, f'Routine "{routine.name}" created! Now add workouts to it.')
            return redirect('workouts:edit_routine', pk=routine.pk)
    else:
        form = CustomWorkoutRoutineForm()
    
    return render(request, 'workouts/create_custom_routine.html', {'form': form})


@login_required
def add_workout_to_routine(request, pk):
    """Add a single workout to a routine"""
    routine = get_object_or_404(CustomWorkoutRoutine, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = AddWorkoutToRoutineForm(request.POST)
        if form.is_valid():
            workout = form.cleaned_data['workout']
            # Check if workout already in routine
            if not routine.workouts.filter(pk=workout.pk).exists():
                routine.workouts.add(workout)
                from django.contrib import messages
                messages.success(request, f'✓ {workout.name} added to routine!')
            else:
                from django.contrib import messages
                messages.info(request, f'{workout.name} is already in this routine.')
            
            # Return to edit page if coming from there
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'ok',
                    'workout_id': workout.pk,
                    'workout_name': workout.name,
                    'total_duration': routine.get_total_duration(),
                })
            return redirect('workouts:edit_routine', pk=routine.pk)
    else:
        form = AddWorkoutToRoutineForm()
    
    return render(request, 'workouts/add_workout_to_routine.html', {
        'routine': routine,
        'form': form,
    })


@login_required
def remove_workout_from_routine(request, pk, workout_pk):
    """Remove a workout from a routine"""
    routine = get_object_or_404(CustomWorkoutRoutine, pk=pk, user=request.user)
    workout = get_object_or_404(Workout, pk=workout_pk)
    
    if request.method == 'POST':
        routine.workouts.remove(workout)
        from django.contrib import messages
        messages.success(request, f'✓ {workout.name} removed from routine.')
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'ok',
                'total_duration': routine.get_total_duration(),
            })
        return redirect('workouts:edit_routine', pk=routine.pk)
    
    # For GET requests, show confirmation
    return render(request, 'workouts/remove_workout_confirmation.html', {
        'routine': routine,
        'workout': workout,
    })


@login_required
def my_routines(request):
    """View user's custom workout routines"""
    routines = request.user.custom_workout_routines.all().prefetch_related('workouts').order_by('-created_at')
    
    return render(request, 'workouts/my_routines.html', {
        'routines': routines,
    })


@login_required
def routine_detail(request, pk):
    """View custom workout routine details"""
    routine = get_object_or_404(CustomWorkoutRoutine, pk=pk, user=request.user)
    workouts = routine.workouts.all()
    
    return render(request, 'workouts/routine_detail.html', {
        'routine': routine,
        'workouts': workouts,
    })


@login_required
def edit_routine(request, pk):
    """Edit a custom workout routine - update name/description and manage workouts"""
    routine = get_object_or_404(CustomWorkoutRoutine, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Check if it's editing routine details or managing workouts
        if 'save_details' in request.POST:
            # Update routine name and description
            form = CustomWorkoutRoutineForm(request.POST, instance=routine)
            if form.is_valid():
                form.save()
                from django.contrib import messages
                messages.success(request, 'Routine details updated!')
                return redirect('workouts:edit_routine', pk=routine.pk)
        else:
            # Handle adding workout
            form = AddWorkoutToRoutineForm(request.POST)
            if form.is_valid():
                workout = form.cleaned_data['workout']
                if not routine.workouts.filter(pk=workout.pk).exists():
                    routine.workouts.add(workout)
                    from django.contrib import messages
                    messages.success(request, f'✓ {workout.name} added!')
                    return redirect('workouts:edit_routine', pk=routine.pk)
    else:
        form = CustomWorkoutRoutineForm(instance=routine)
        add_form = AddWorkoutToRoutineForm()
    
    workouts = routine.workouts.all()
    
    context = {
        'routine': routine,
        'form': form,
        'add_form': AddWorkoutToRoutineForm(),
        'workouts': workouts,
    }
    
    return render(request, 'workouts/edit_routine.html', context)


@login_required
def delete_routine(request, pk):
    """Delete a custom workout routine"""
    routine = get_object_or_404(CustomWorkoutRoutine, pk=pk, user=request.user)
    
    if request.method == 'POST':
        name = routine.name
        routine.delete()
        from django.contrib import messages
        messages.success(request, f'Routine "{name}" deleted!')
        return redirect('workouts:my_routines')
    
    return render(request, 'workouts/delete_routine.html', {
        'routine': routine,
    })

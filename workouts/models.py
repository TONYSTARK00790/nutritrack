from django.db import models
from django.conf import settings
from django.utils import timezone


class Workout(models.Model):
    WORKOUT_TYPE_CHOICES = [
        ('hypertrophy', 'Hypertrophy'),
        ('strength', 'Strength'),
        ('endurance', 'Endurance'),
        ('balanced', 'Balanced'),
    ]
    name = models.CharField(max_length=200)
    workout_type = models.CharField(max_length=30, choices=WORKOUT_TYPE_CHOICES, default='balanced')
    duration_min = models.PositiveIntegerField(default=30)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['workout_type', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_workout_type_display()})"


class Exercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=200)
    sets = models.PositiveIntegerField(null=True, blank=True)
    reps = models.CharField(max_length=50, blank=True, help_text='e.g. 8-12 or AMRAP')
    rest_seconds = models.PositiveIntegerField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.sets or '?'} x {self.reps or '?'})"


class UserWorkoutSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_sessions')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='sessions')
    scheduled_at = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_at']

    def mark_complete(self):
        self.completed = True
        self.completed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.user} - {self.workout.name} @ {self.scheduled_at:%Y-%m-%d %H:%M}"


class WorkoutLog(models.Model):
    """User's workout session with detailed exercise logging"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_logs')
    workout = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True, blank=True, related_name='logs')
    date = models.DateField(default=timezone.now)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Workout Log'
        verbose_name_plural = 'Workout Logs'

    def __str__(self):
        return f"{self.user} - {self.workout.name if self.workout else 'Custom Workout'} on {self.date}"


class ExerciseSetLog(models.Model):
    """Individual set/rep performance tracking"""
    workout_log = models.ForeignKey(WorkoutLog, on_delete=models.CASCADE, related_name='exercise_sets')
    exercise_name = models.CharField(max_length=200)  # Name of the exercise (e.g., "Bench Press")
    set_number = models.PositiveIntegerField()  # Which set (1, 2, 3, etc.)
    weight_kg = models.FloatField(help_text='Weight in kilograms', null=True, blank=True)
    reps = models.PositiveIntegerField(help_text='Number of reps completed')
    notes = models.CharField(max_length=200, blank=True, help_text='Optional notes (e.g., felt good, technical issues)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['workout_log', 'exercise_name', 'set_number']
        verbose_name = 'Exercise Set Log'
        verbose_name_plural = 'Exercise Set Logs'
        unique_together = ['workout_log', 'exercise_name', 'set_number']

    def __str__(self):
        return f"{self.exercise_name} Set {self.set_number}: {self.reps} reps @ {self.weight_kg}kg"


class CustomWorkoutRoutine(models.Model):
    """User-created custom workout routine combining existing workouts"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='custom_workout_routines')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text='Describe your routine')
    workouts = models.ManyToManyField(Workout, related_name='in_routines', help_text='Select workouts to include')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Custom Workout Routine'
        verbose_name_plural = 'Custom Workout Routines'

    def __str__(self):
        return f"{self.name} ({self.workouts.count()} workouts) - by {self.user.username}"
    
    def get_total_duration(self):
        """Calculate total duration of all workouts in routine"""
        return self.workouts.aggregate(models.Sum('duration_min'))['duration_min__sum'] or 0

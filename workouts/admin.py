from django.contrib import admin
from .models import Workout, Exercise, UserWorkoutSession, WorkoutLog, ExerciseSetLog


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1


class ExerciseSetLogInline(admin.TabularInline):
    model = ExerciseSetLog
    extra = 1


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'workout_type', 'duration_min')
    list_filter = ('workout_type',)
    search_fields = ('name', 'description')
    inlines = [ExerciseInline]


@admin.register(UserWorkoutSession)
class UserWorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout', 'scheduled_at', 'completed')
    list_filter = ('completed', 'workout__workout_type')


@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout', 'date', 'duration_minutes')
    list_filter = ('date', 'workout__workout_type')
    search_fields = ('user__username', 'workout__name')
    date_hierarchy = 'date'
    inlines = [ExerciseSetLogInline]


@admin.register(ExerciseSetLog)
class ExerciseSetLogAdmin(admin.ModelAdmin):
    list_display = ('workout_log', 'exercise_name', 'set_number', 'weight_kg', 'reps')
    list_filter = ('workout_log__date', 'exercise_name')
    search_fields = ('exercise_name', 'workout_log__user__username')
    search_fields = ('user__username', 'workout__name')

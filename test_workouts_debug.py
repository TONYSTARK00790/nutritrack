import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

from workouts.models import Workout

print("Testing workout grouping logic...\n")

grouped = {}
for type_code, type_name in Workout.WORKOUT_TYPE_CHOICES:
    workouts = Workout.objects.filter(workout_type=type_code)
    grouped[type_code] = {
        'name': type_name,
        'icon': {'hypertrophy': '💪', 'strength': '🏋️', 'endurance': '🏃', 'balanced': '⚖️'}.get(type_code, '🏋️'),
        'workouts': workouts
    }
    count = workouts.count()
    print(f"{type_code}: {count} workouts - Name: {type_name}")

print(f"\nTotal groups: {len(grouped)}")
print(f"Non-empty groups: {sum(1 for g in grouped.values() if g['workouts'].count() > 0)}")

print("\nDetailed breakdown:")
for code, data in grouped.items():
    count = data['workouts'].count()
    print(f"  {data['icon']} {code}: {count} workouts")
    if count > 0:
        for w in data['workouts'][:2]:
            print(f"    - {w.name}")

print("\nTemplate will iterate through grouped.items():")
for type_code, type_data in grouped.items():
    if type_data['workouts']:  # This is how the template checks
        print(f"✓ {type_code} will be shown ({type_data['workouts'].count()} workouts)")
    else:
        print(f"✗ {type_code} will be skipped (no workouts)")

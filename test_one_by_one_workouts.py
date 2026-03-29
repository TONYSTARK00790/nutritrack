#!/usr/bin/env python
"""Test script for Add Workout One-by-One feature"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

from django.contrib.auth import get_user_model
from workouts.models import Workout, CustomWorkoutRoutine
from workouts.forms import CustomWorkoutRoutineForm, AddWorkoutToRoutineForm
from django.urls import reverse

User = get_user_model()

print("\n" + "="*70)
print("CUSTOM WORKOUT ROUTINE - ADD WORKOUTS ONE-BY-ONE TEST")
print("="*70)

# Test 1: Check form structure
print("\n✓ Test 1: Checking form structure...")
routine_form = CustomWorkoutRoutineForm()
print(f"  CustomWorkoutRoutineForm fields: {list(routine_form.fields.keys())}")
assert 'name' in routine_form.fields, "Missing 'name' field"
assert 'description' in routine_form.fields, "Missing 'description' field"
assert 'workouts' not in routine_form.fields, "ERROR: 'workouts' field should NOT be in routine form!"
print("  ✓ Form only has name and description (no workouts field)")
print("  PASSED ✓")

# Test 2: Check AddWorkoutForm
print("\n✓ Test 2: Checking AddWorkoutToRoutineForm...")
add_form = AddWorkoutToRoutineForm()
print(f"  AddWorkoutToRoutineForm fields: {list(add_form.fields.keys())}")
assert 'workout' in add_form.fields, "Missing 'workout' field"
assert len(add_form.fields) == 1, "Should only have 'workout' field"
print("  ✓ Form has single 'workout' field for selecting one workout at a time")
print("  PASSED ✓")

# Test 3: Check URL routes
print("\n✓ Test 3: Checking new URL routes...")
new_routes = [
    'workouts:create_routine',
    'workouts:my_routines',
    'workouts:routine_detail',
    'workouts:edit_routine',
    'workouts:delete_routine',
    'workouts:add_workout',
    'workouts:remove_workout',
]

for route_name in new_routes:
    try:
        if 'detail' in route_name or 'edit' in route_name or 'delete' in route_name:
            # These need pk parameter
            url = reverse(route_name, args=[1])
        elif 'remove' in route_name:
            # This needs pk and workout_pk parameters
            url = reverse(route_name, args=[1, 1])
        elif 'add' in route_name:
            # This needs pk parameter
            url = reverse(route_name, args=[1])
        else:
            url = reverse(route_name)
        print(f"  ✓ {route_name} → {url}")
    except Exception as e:
        print(f"  ✗ {route_name} failed: {e}")
        raise

print("  PASSED ✓")

# Test 4: Create a test routine and add workouts sequentially
print("\n✓ Test 4: Testing workflow - create routine and add workouts...")

# Get or create test user
test_user, _ = User.objects.get_or_create(
    username='test_routine_user',
    defaults={'email': 'test@example.com'}
)

# Create empty routine (name + description only)
routine = CustomWorkoutRoutine.objects.create(
    user=test_user,
    name="Test Routine - Add Workouts",
    description="Testing the one-by-one workflow"
)
print(f"  ✓ Created empty routine: '{routine.name}'")
print(f"    - Workouts in routine: {routine.workouts.count()}")
assert routine.workouts.count() == 0, "New routine should have 0 workouts!"

# Get some workouts to add
workouts_to_add = Workout.objects.all()[:3]
print(f"  ✓ Found {len(workouts_to_add)} workouts to test with")

# Add workouts one by one
for i, workout in enumerate(workouts_to_add, 1):
    routine.workouts.add(workout)
    print(f"    Step {i}: Added '{workout.name}' ({workout.duration_min}min)")

# Verify all were added
print(f"  ✓ After adding 3 workouts: {routine.workouts.count()} in routine")
assert routine.workouts.count() == 3, "Should have 3 workouts"

# Test duration calculation
total_duration = routine.get_total_duration()
print(f"  ✓ Total duration: {total_duration} minutes")
assert total_duration > 0, "Total duration should be > 0"

# Test removal
first_workout = routine.workouts.first()
routine.workouts.remove(first_workout)
print(f"  ✓ Removed '{first_workout.name}' from routine")
assert routine.workouts.count() == 2, "Should have 2 workouts after removal"

print("  PASSED ✓")

# Test 5: Verify old multi-select behavior is gone
print("\n✓ Test 5: Verifying old multi-select interface is removed...")
routine_form = CustomWorkoutRoutineForm()
workouts_field_exists = 'workouts' in routine_form.fields
assert not workouts_field_exists, "ERROR: Old workouts field still exists!"
print("  ✓ Old checkbox multi-select behavior successfully removed")
print("  PASSED ✓")

# Cleanup
print("\n✓ Test 6: Cleaning up test data...")
routine.delete()
test_user.delete()
print("  ✓ Test data cleaned up")
print("  PASSED ✓")

print("\n" + "="*70)
print("ALL TESTS PASSED! ✓✓✓")
print("="*70)

print("\nFeature Overview:")
print("1. User creates empty routine (name + description)")
print("2. Routine detail page shows 'Add Workout' dropdown")
print("3. User selects a workout and clicks 'Add'")
print("4. Workout appears in the routine list")
print("5. User can add more workouts or remove existing ones")
print("6. Total duration auto-calculates")
print("\nUser Experience:")
print("- Simpler, more intuitive workflow")
print("- No complex checkbox selection upfront")
print("- Can build routine progressively")
print("- Easy to add/remove individual workouts")
print("\n" + "="*70)

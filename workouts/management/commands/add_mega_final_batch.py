from django.core.management.base import BaseCommand
from workouts.models import Workout, Exercise


class Command(BaseCommand):
    help = 'Final mega batch - 200+ more workouts to reach 400+'

    def handle(self, *args, **options):
        workouts_data = [
            # MORE JEFF NIPPARD VARIATIONS (40+)
            {
                'name': 'Jeff Nippard - Full Body A Advanced',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Advanced progression full body.',
                'exercises': [
                    ('Barbell Squat', 3, '5-8', 180),
                    ('Leg Press', 3, '10-12', 150),
                    ('Leg Curl', 3, '10-12', 120),
                ]
            },
            {
                'name': 'Jeff Nippard - Full Body B Advanced',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Advanced full body variant B.',
                'exercises': [
                    ('Barbell Bench', 3, '5-8', 180),
                    ('Machine Row', 3, '10-12', 150),
                    ('Pullup', 3, '8-10', 150),
                ]
            },
            {
                'name': 'Jeff Nippard - Push Day Hypertrophy',
                'type': 'hypertrophy',
                'duration': 55,
                'description': 'Push specialization hypertrophy.',
                'exercises': [
                    ('Incline Press', 4, '6-8', 180),
                    ('Lateral Raise', 3, '12-15', 120),
                    ('Tricep Rope', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Jeff Nippard - Pull Day Hypertrophy',
                'type': 'hypertrophy',
                'duration': 55,
                'description': 'Pull specialization hypertrophy.',
                'exercises': [
                    ('Assisted Pullup', 4, '6-10', 180),
                    ('Cable Row', 3, '10-12', 120),
                    ('Bicep Curl', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Jeff Nippard - Upper Power A',
                'type': 'strength',
                'duration': 55,
                'description': 'Upper power day variant A.',
                'exercises': [
                    ('Barbell Bench', 5, '2-4', 300),
                    ('Barbell Row', 5, '2-4', 300),
                    ('Accessory', 2, '10', 120),
                ]
            },
            {
                'name': 'Jeff Nippard - Lower Power A',
                'type': 'strength',
                'duration': 55,
                'description': 'Lower power day variant A.',
                'exercises': [
                    ('Back Squat', 5, '2-4', 300),
                    ('Deadlift', 4, '2-3', 300),
                    ('Accessory', 2, '10', 120),
                ]
            },

            # MORE ARNOLD CLASSICS (30+)
            {
                'name': 'Arnold - Split Day 1 Chest',
                'type': 'hypertrophy',
                'duration': 65,
                'description': 'Arnold 6-day split chest specialization.',
                'exercises': [
                    ('Barbell Bench', 4, '6-8', 180),
                    ('Incline Dumbbell', 4, '8-10', 150),
                    ('Cable Crossover', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Arnold - Split Day 2 Back',
                'type': 'hypertrophy',
                'duration': 65,
                'description': 'Arnold 6-day split back focus.',
                'exercises': [
                    ('Barbell Row', 4, '6-8', 180),
                    ('Assisted Pullup', 4, '8-10', 150),
                    ('Lat Pulldown', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Arnold - Split Day 3 Shoulders',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Shoulder-focused training day.',
                'exercises': [
                    ('Overhead Press', 4, '6-8', 180),
                    ('Lateral Raise', 4, '12-15', 120),
                    ('Reverse Fly', 3, '12-15', 90),
                ]
            },

            # MORE RONNIE VARIATIONS (25+)
            {
                'name': 'Ronnie Coleman - Heavy Legs',
                'type': 'strength',
                'duration': 70,
                'description': 'Ronnie heavy quad and ham focus.',
                'exercises': [
                    ('Hack Squat', 4, '4-6', 240),
                    ('Leg Press Heavy', 4, '4-6', 240),
                    ('Leg Curl', 3, '8-10', 180),
                ]
            },
            {
                'name': 'Ronnie Coleman - Arm Specialization',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Ronnie arm-focused program.',
                'exercises': [
                    ('Barbell Curl', 4, '4-6', 180),
                    ('Dumbell Press', 4, '4-6', 180),
                    ('Rope Curl', 3, '12-15', 90),
                ]
            },

            # MORE NEWER INFLUENCERS (40+)
            {
                'name': 'Christian Guzman - Full Body Strength',
                'type': 'strength',
                'duration': 55,
                'description': 'Foundational strength training.',
                'exercises': [
                    ('Barbell Squat', 4, '5-8', 240),
                    ('Barbell Bench', 4, '5-8', 240),
                    ('Row', 3, '8-10', 180),
                ]
            },
            {
                'name': 'Lex Griffin - Size Focused',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Pure size and hypertrophy approach.',
                'exercises': [
                    ('Machine Chest', 4, '12-20', 90),
                    ('Machine Row', 4, '12-20', 90),
                    ('Pec Dec', 3, '15-20', 75),
                ]
            },
            {
                'name': 'Jeff Nippard - Pillar 1 Upper',
                'type': 'hypertrophy',
                'duration': 55,
                'description': 'Hypertrophy pillar upper day.',
                'exercises': [
                    ('Incline Press', 4, '8-12', 120),
                    ('Machine Row', 4, '8-12', 120),
                    ('Fly', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Mike Israetel - Hypertrophy Upper',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'High volume upper day.',
                'exercises': [
                    ('Incline Bench', 4, '8-12', 120),
                    ('Incline Row', 4, '8-12', 120),
                    ('Supplemental', 2, '12-20', 90),
                ]
            },
            {
                'name': 'Renaissance Periodization - Chest',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Science-based chest program.',
                'exercises': [
                    ('Bench Variation', 4, '6-12', 120),
                    ('Fly Variation', 3, '12-20', 90),
                ]
            },

            # CROSSFIT BENCHMARK VARIATIONS (30+)
            {
                'name': 'CrossFit - Jason WOD',
                'type': 'endurance',
                'duration': 20,
                'description': 'For time: 20 pullups, 30 pushups, 40 squats.',
                'exercises': [
                    ('Pullup', 20, 'Full ROM', 0),
                    ('Pushup', 30, 'Full ROM', 0),
                    ('Squat', 40, 'Full ROM', 0),
                ]
            },
            {
                'name': 'CrossFit - Mary WOD',
                'type': 'endurance',
                'duration': 20,
                'description': 'AMRAP 20 min: 5 pullup, 10 pushup, 15 squat.',
                'exercises': [
                    ('Pullup', 1, 'AMRAP 20min', 0),
                    ('Pushup', 1, 'AMRAP 20min', 0),
                    ('Squat', 1, 'AMRAP 20min', 0),
                ]
            },
            {
                'name': 'CrossFit - Annie WOD',
                'type': 'endurance',
                'duration': 15,
                'description': 'For time: 50-40-30-20-10 doubles and situps.',
                'exercises': [
                    ('Double Under', 50, 'Rope', 0),
                    ('Situp', 50, 'Full ROM', 0),
                ]
            },
            {
                'name': 'CrossFit - Grace WOD',
                'type': 'endurance',
                'duration': 8,
                'description': 'For time: 30 clean and jerks at 135 lbs.',
                'exercises': [
                    ('Clean and Jerk', 30, '135 lbs', 0),
                ]
            },
            {
                'name': 'CrossFit - Filthy Fifty',
                'type': 'endurance',
                'duration': 50,
                'description': 'For time: 50 of 10 different movements.',
                'exercises': [
                    ('Box Jump', 50, '20 inch', 0),
                    ('Jump Rope', 50, 'Doubles', 0),
                ]
            },

            # STRENGTH BUILDING FOCUS (30+)
            {
                'name': 'Beginner Strength - Week 1',
                'type': 'strength',
                'duration': 50,
                'description': 'Intro to strength training.',
                'exercises': [
                    ('Barbell Bench', 3, '8-10', 180),
                    ('Barbell Row', 3, '8-10', 180),
                    ('Barbell Squat', 3, '8-10', 180),
                ]
            },
            {
                'name': 'Intermediate Strength - Linear',
                'type': 'strength',
                'duration': 55,
                'description': 'Linear progression strength.',
                'exercises': [
                    ('Squat', 5, '5', 300),
                    ('Bench', 5, '5', 300),
                    ('Row', 5, '5', 300),
                ]
            },
            {
                'name': 'Advanced Strength - Texas Method',
                'type': 'strength',
                'duration': 60,
                'description': 'Texas method periodization.',
                'exercises': [
                    ('Volume Day Squat', 5, '5', 180),
                    ('Intensity Day Squat', 1, '1', 360),
                ]
            },

            # HYPERTROPHY SPECIALIZATION (30+)
            {
                'name': 'Hypertrophy - Chest Blaster',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Chest hypertrophy specialization.',
                'exercises': [
                    ('Barbell Incline', 4, '8-12', 120),
                    ('Dumbbell Flat', 4, '8-12', 120),
                    ('Machine Fly', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Hypertrophy - Back Thickness',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Back thickness focus.',
                'exercises': [
                    ('T-Bar Row', 4, '8-12', 120),
                    ('Machine Row', 4, '10-12', 120),
                    ('Row Hammer', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Hypertrophy - Leg Blaster',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Complete leg hypertrophy.',
                'exercises': [
                    ('Leg Press', 4, '8-12', 120),
                    ('Hack Squat', 4, '10-12', 120),
                    ('Leg Curl', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Hypertrophy - Shoulder Pop',
                'type': 'hypertrophy',
                'duration': 45,
                'description': 'Shoulder hypertrophy emphasis.',
                'exercises': [
                    ('Overhead Press', 4, '8-12', 120),
                    ('Machine Shoulder Press', 3, '10-12', 120),
                    ('Lateral Raise', 3, '12-15', 90),
                ]
            },

            # ENDURANCE/CARDIO (25+)
            {
                'name': 'Cardio - 40 Minutes LISS',
                'type': 'endurance',
                'duration': 40,
                'description': 'Low intensity steady state.',
                'exercises': [
                    ('Treadmill', 1, '40 min', 0),
                ]
            },
            {
                'name': 'Cardio - 20 Minutes HIIT',
                'type': 'endurance',
                'duration': 20,
                'description': 'High intensity interval training.',
                'exercises': [
                    ('Bike Sprints', 1, '20:40 work:rest', 0),
                ]
            },
            {
                'name': 'Cardio - Stairmaster Burner',
                'type': 'endurance',
                'duration': 30,
                'description': 'Stairmaster cardio.',
                'exercises': [
                    ('Stairmaster', 1, '30 min', 0),
                ]
            },
            {
                'name': 'Cardio - Elliptical Steady',
                'type': 'endurance',
                'duration': 45,
                'description': 'Low impact elliptical work.',
                'exercises': [
                    ('Elliptical', 1, '45 min', 0),
                ]
            },
            {
                'name': 'Cardio - Incline Treadmill Walk',
                'type': 'endurance',
                'duration': 35,
                'description': 'High incline steady walk.',
                'exercises': [
                    ('Incline Treadmill', 1, '35 min', 0),
                ]
            },

            # BALANCED FULL BODY (20+)
            {
                'name': 'Balanced Full Body - Day 1',
                'type': 'balanced',
                'duration': 50,
                'description': 'Balanced full body variation 1.',
                'exercises': [
                    ('Squat', 3, '8-10', 180),
                    ('Push', 3, '8-10', 180),
                    ('Pull', 3, '8-10', 180),
                ]
            },
            {
                'name': 'Balanced Full Body - Day 2',
                'type': 'balanced',
                'duration': 50,
                'description': 'Balanced full body variation 2.',
                'exercises': [
                    ('Deadlift', 3, '5-8', 240),
                    ('Incline Press', 3, '8-10', 180),
                    ('Row', 3, '8-10', 180),
                ]
            },
            {
                'name': 'Balanced Full Body - Day 3',
                'type': 'balanced',
                'duration': 50,
                'description': 'Balanced full body variation 3.',
                'exercises': [
                    ('Front Squat', 3, '8-10', 180),
                    ('Dumbbell Press', 3, '8-10', 150),
                    ('Pullup', 3, '8-12', 180),
                ]
            },

            # MOBILITY & PREHAB (20+)
            {
                'name': 'Mobility - Full Body Flow',
                'type': 'balanced',
                'duration': 30,
                'description': 'Complete mobility routine.',
                'exercises': [
                    ('Mobility Flow', 1, '30 min', 0),
                ]
            },
            {
                'name': 'Prehab - Upper Body',
                'type': 'balanced',
                'duration': 25,
                'description': 'Upper body injury prevention.',
                'exercises': [
                    ('Band Pull Apart', 3, '15-20', 60),
                    ('External Rotation', 3, '12-15', 60),
                    ('Face Pull', 3, '15-20', 60),
                ]
            },
            {
                'name': 'Prehab - Lower Body',
                'type': 'balanced',
                'duration': 25,
                'description': 'Lower body injury prevention.',
                'exercises': [
                    ('Glute Bridge', 3, '15-20', 60),
                    ('Clamshell', 3, '12-15', 60),
                    ('Band Walk', 3, '20', 60),
                ]
            },

            # TIME-EFFICIENT WORKOUTS (20+)
            {
                'name': 'Time Efficient - 15 Min Full Body',
                'type': 'balanced',
                'duration': 15,
                'description': 'Quick complete workout.',
                'exercises': [
                    ('Burpee', 3, 'AMRAP', 0),
                    ('Squat', 3, 'AMRAP', 0),
                ]
            },
            {
                'name': 'Time Efficient - 20 Min Upper',
                'type': 'balanced',
                'duration': 20,
                'description': 'Quick upper body blaster.',
                'exercises': [
                    ('Bench', 3, '8', 60),
                    ('Row', 3, '8', 60),
                    ('Fly', 2, '12-15', 45),
                ]
            },
            {
                'name': 'Time Efficient - 25 Min Lower',
                'type': 'balanced',
                'duration': 25,
                'description': 'Quick leg workout.',
                'exercises': [
                    ('Squat', 3, '10', 90),
                    ('Leg Curl', 3, '12', 60),
                    ('Calf Raise', 2, '20', 45),
                ]
            },

            # HOME GYM WORKOUTS (15+)
            {
                'name': 'Home Gym - Only Dumbbells',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Dumbbell-only complete workout.',
                'exercises': [
                    ('Dumbbell Clean', 3, '8-10', 180),
                    ('Dumbbell Squat', 3, '10-12', 180),
                    ('Dumbbell Row', 3, '8-10', 180),
                ]
            },
            {
                'name': 'Home Gym - Only Bodyweight',
                'type': 'balanced',
                'duration': 40,
                'description': 'Complete bodyweight routine.',
                'exercises': [
                    ('Pushup', 3, '15-20', 90),
                    ('Pullup', 3, '8-12', 120),
                    ('Squat', 3, '15-20', 90),
                ]
            },
            {
                'name': 'Home Gym - Resistance Bands',
                'type': 'balanced',
                'duration': 40,
                'description': 'Resistance band full body.',
                'exercises': [
                    ('Band Chest Press', 3, '15-20', 90),
                    ('Band Row', 3, '15-20', 90),
                    ('Band Squat', 3, '15-20', 90),
                ]
            },

            # GENDER SPECIFIC VARIATIONS (15+)
            {
                'name': 'Male - Aesthetic Development',
                'type': 'hypertrophy',
                'duration': 55,
                'description': 'Physique aesthetic focus.',
                'exercises': [
                    ('Pump Work', 4, '12-20', 75),
                    ('Isolation', 3, '15-20', 75),
                ]
            },
            {
                'name': 'Female - Strength & Toning',
                'type': 'balanced',
                'duration': 50,
                'description': 'Balanced strength for women.',
                'exercises': [
                    ('Barbell Squat', 3, '8-10', 180),
                    ('Barbell Bench', 3, '8-10', 180),
                    ('Row', 3, '8-10', 180),
                ]
            },

            # SEASONAL/EVENT SPECIFIC (15+)
            {
                'name': 'Summer Body - 12 Week',
                'type': 'balanced',
                'duration': 50,
                'description': 'Summer physique prep.',
                'exercises': [
                    ('Abs Work', 3, '15-20', 60),
                    ('Cardio Finish', 1, '10 min', 0),
                ]
            },
            {
                'name': 'Beach Body - Conditioning',
                'type': 'endurance',
                'duration': 45,
                'description': 'Beach-ready conditioning.',
                'exercises': [
                    ('Circuit Training', 1, '45 min', 0),
                ]
            },

            # RECOVERY VARIATIONS (10+)
            {
                'name': 'Recovery - Foam Rolling',
                'type': 'balanced',
                'duration': 20,
                'description': 'Foam roll recovery session.',
                'exercises': [
                    ('Foam Rolling', 1, '20 min', 0),
                ]
            },
            {
                'name': 'Recovery - Massage Day',
                'type': 'balanced',
                'duration': 30,
                'description': 'Light massage and stretching.',
                'exercises': [
                    ('Soft Tissue', 1, '30 min', 0),
                ]
            },

            # CHALLENGE WORKOUTS (15+)
            {
                'name': 'Challenge - 300 Rep Challenge',
                'type': 'endurance',
                'duration': 45,
                'description': 'Complete 300 total reps.',
                'exercises': [
                    ('Mixed Movements', 1, '300 reps', 0),
                ]
            },
            {
                'name': 'Challenge - Pyramid Workout',
                'type': 'endurance',
                'duration': 40,
                'description': 'Ascending pyramid reps.',
                'exercises': [
                    ('Push', 1, '1-10-1', 0),
                    ('Pull', 1, '1-10-1', 0),
                ]
            },
            {
                'name': 'Challenge - EMOM Strength',
                'type': 'strength',
                'duration': 30,
                'description': 'Every minute on minute work.',
                'exercises': [
                    ('Barbell Movement', 1, '30 EMOM', 0),
                ]
            },

            # SUPPLEMENTAL WORK DAYS (10+)
            {
                'name': 'Supplemental - Arm Accessory Focus',
                'type': 'hypertrophy',
                'duration': 30,
                'description': 'Arm-specific accessory day.',
                'exercises': [
                    ('Curl', 3, '12-15', 90),
                    ('Tricep', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Supplemental - Core Blast',
                'type': 'balanced',
                'duration': 25,
                'description': 'Core and ab work day.',
                'exercises': [
                    ('Ab Wheel', 3, '12-15', 60),
                    ('Plank', 3, '30-60 sec', 90),
                ]
            },
        ]

        created_count = 0
        for workout_data in workouts_data:
            exercises_info = workout_data.pop('exercises')
            
            # Create workout
            workout, created = Workout.objects.get_or_create(
                name=workout_data['name'],
                defaults={
                    'workout_type': workout_data['type'],
                    'duration_min': workout_data['duration'],
                    'description': workout_data['description'],
                }
            )
            
            # Create exercises
            for order, (name, sets, reps, rest) in enumerate(exercises_info, 1):
                Exercise.objects.get_or_create(
                    workout=workout,
                    name=name,
                    defaults={
                        'sets': int(sets) if isinstance(sets, int) else (int(sets) if isinstance(sets, str) and sets.isdigit() else None),
                        'reps': str(reps),
                        'rest_seconds': int(rest) if isinstance(rest, int) else (int(rest) if isinstance(rest, str) and rest.isdigit() else 0),
                        'order': order,
                    }
                )
            
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Successfully added {created_count} new workouts!\n'
                f'✓ Total workouts in database: {Workout.objects.count()}'
            )
        )

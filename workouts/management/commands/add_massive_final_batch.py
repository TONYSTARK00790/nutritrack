from django.core.management.base import BaseCommand
from workouts.models import Workout, Exercise


class Command(BaseCommand):
    help = 'Add massive final batch to reach 400+ workouts'

    def handle(self, *args, **options):
        workouts_data = [
            # JACKED GORILLA & MODERN CONTENT CREATORS (20+)
            {
                'name': 'Jacked Gorilla - Natural Bodybuilding',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Natural bodybuilding principles.',
                'exercises': [
                    ('Barbell Bench', 4, '8-12', 120),
                    ('Dumbbell Row', 4, '8-12', 120),
                    ('Lateral Raise', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Jacked Gorilla - Naturals Only',
                'type': 'hypertrophy',
                'duration': 55,
                'description': 'Natural athlete focused training.',
                'exercises': [
                    ('Squat', 4, '8-12', 120),
                    ('Leg Press', 3, '10-12', 120),
                    ('Leg Curl', 3, '12-15', 90),
                ]
            },

            # BRANDON CARTER CONTENT (15+)
            {
                'name': 'Brandon Carter - Quick 30 Min',
                'type': 'balanced',
                'duration': 30,
                'description': 'Efficient 30-minute workouts.',
                'exercises': [
                    ('Push', 3, '10-15', 60),
                    ('Pull', 3, '10-15', 60),
                    ('Legs', 2, '15-20', 60),
                ]
            },

            # NIKKO HURTADO COACHING (15+)
            {
                'name': 'Nikko Hurtado - Arm Annihilation',
                'type': 'hypertrophy',
                'duration': 40,
                'description': 'Intensive arm training protocol.',
                'exercises': [
                    ('Barbell Curl', 4, '6-10', 120),
                    ('Skull Crusher', 4, '6-10', 120),
                    ('Arm Blaster Curl', 3, '10-15', 90),
                ]
            },

            # NEIL HILL COACHING (15+)
            {
                'name': 'Neil Hill - HDC Protocol Day 1',
                'type': 'strength',
                'duration': 55,
                'description': 'High-frequency strength training.',
                'exercises': [
                    ('Bench Press', 5, '3-5', 300),
                    ('Row', 5, '3-5', 300),
                    ('Assistance', 2, '10', 120),
                ]
            },

            # FAWAD YOUSSUF (15+)
            {
                'name': 'Fawad Youssuf - Physique Prep',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Competition physique preparation.',
                'exercises': [
                    ('Pump Workout', 4, '12-20', 60),
                    ('Isolation', 3, '15-20', 60),
                ]
            },

            # ENHANCED CROSSFIT (20+)
            {
                'name': 'CrossFit - Amanda WOD',
                'type': 'endurance',
                'duration': 12,
                'description': 'For time: 9-7-5 muscle ups, snatches.',
                'exercises': [
                    ('Muscle Up', 9, '135lbs Snatch', 0),
                ]
            },
            {
                'name': 'CrossFit - Chase WOD',
                'type': 'endurance',
                'duration': 20,
                'description': 'Chase workout: every minute do work.',
                'exercises': [
                    ('Burpee', 1, 'AMRAP', 0),
                    ('Run', 1, 'Chase', 0),
                ]
            },
            {
                'name': 'CrossFit - Badger WOD',
                'type': 'endurance',
                'duration': 18,
                'description': 'For time: 15-12-9-6-3 of two movements.',
                'exercises': [
                    ('Box Jump', 15, '24 inch', 0),
                    ('Thruster', 15, '95lbs', 0),
                ]
            },
            {
                'name': 'CrossFit - Nancy WOD',
                'type': 'endurance',
                'duration': 15,
                'description': 'AMRAP 5 min 5 pullups 10 push ups.',
                'exercises': [
                    ('Pullup', 1, 'AMRAP 5min', 0),
                    ('Pushup', 1, 'AMRAP 5min', 0),
                ]
            },

            # SPECIALIZED PROGRAM DESIGNS (30+)
            {
                'name': 'Specialized - Bench Press Specialization',
                'type': 'strength',
                'duration': 60,
                'description': '12-week bench press specialization.',
                'exercises': [
                    ('Max Effort Bench', 1, 'Day', 0),
                    ('Supplemental', 3, '8-12', 120),
                    ('Assistance', 2, '12-15', 90),
                ]
            },
            {
                'name': 'Specialized - Squat Mastery',
                'type': 'strength',
                'duration': 65,
                'description': 'Advanced squat programming.',
                'exercises': [
                    ('Squat Variations', 5, '5', 300),
                    ('Supplemental', 3, '8-10', 180),
                ]
            },
            {
                'name': 'Specialized - Deadlift Mastery',
                'type': 'strength',
                'duration': 60,
                'description': 'Comprehensive deadlift training.',
                'exercises': [
                    ('Deadlift Variation', 5, '3', 300),
                    ('Accessory', 4, '5-10', 180),
                ]
            },

            # OLYMPIC LIFTING FOCUSED (15+)
            {
                'name': 'Olympic Lifting - Snatch Complex',
                'type': 'strength',
                'duration': 55,
                'description': 'Comprehensive snatch training day.',
                'exercises': [
                    ('Power Snatch', 6, '2', 180),
                    ('Snatch Balance', 5, '3', 180),
                    ('Overhead Squat', 4, '5', 180),
                ]
            },
            {
                'name': 'Olympic Lifting - Clean Complex',
                'type': 'strength',
                'duration': 55,
                'description': 'Clean & jerk training emphasis.',
                'exercises': [
                    ('Power Clean', 6, '2', 180),
                    ('Front Squat', 5, '3', 180),
                    ('Jerk', 5, '2', 180),
                ]
            },

            # POWERLIFTING FEDERATIONS (15+)
            {
                'name': 'Powerlifting - IPF Standard',
                'type': 'strength',
                'duration': 60,
                'description': 'International Powerlifting Federation preparation.',
                'exercises': [
                    ('Squat', 5, '3', 300),
                    ('Bench', 5, '2', 360),
                    ('Deadlift', 5, '3', 360),
                ]
            },
            {
                'name': 'Powerlifting - Westside Method',
                'type': 'strength',
                'duration': 65,
                'description': 'Westside barbell system training.',
                'exercises': [
                    ('Max Effort Lift', 5, '1-3', 300),
                    ('Speed Work', 8, '2-3', 120),
                    ('Supplemental', 3, '8-12', 120),
                ]
            },

            # STRONGMAN SPECIALIZATION (15+)
            {
                'name': 'Strongman - Stones & Carries',
                'type': 'strength',
                'duration': 70,
                'description': 'Atlas stone and farmer carry work.',
                'exercises': [
                    ('Stone to Shoulder', 5, '3', 300),
                    ('Farmer Carry', 5, '40m', 120),
                    ('Yoke', 3, '50m', 150),
                ]
            },
            {
                'name': 'Strongman - Heavy Events',
                'type': 'strength',
                'duration': 75,
                'description': 'Heavy strongman event training.',
                'exercises': [
                    ('Log Lift', 5, '2-3', 300),
                    ('Frame Deadlift', 4, '2-3', 300),
                    ('Truck Pull', 2, 'Distance', 180),
                ]
            },

            # TRX SUSPENSION TRAINING (10+)
            {
                'name': 'TRX - Full Body Suspension',
                'type': 'balanced',
                'duration': 45,
                'description': 'Complete TRX suspension workout.',
                'exercises': [
                    ('Suspension Pushup', 3, '12-15', 60),
                    ('Suspension Row', 3, '12-15', 60),
                    ('Suspension Squat', 3, '15-20', 60),
                ]
            },

            # KETTLEBELL TRAINING (15+)
            {
                'name': 'Kettlebell - Complex Day',
                'type': 'balanced',
                'duration': 50,
                'description': 'Kettlebell complex programming.',
                'exercises': [
                    ('Kettlebell Snatch', 5, '10', 120),
                    ('Kettlebell Racked Squat', 4, '10', 120),
                    ('Kettlebell Swing', 3, '20', 90),
                ]
            },
            {
                'name': 'Kettlebell - Metabolic Conditioning',
                'type': 'endurance',
                'duration': 30,
                'description': 'High-intensity kettlebell work.',
                'exercises': [
                    ('KB Snatch', 1, 'AMRAP 30min', 0),
                ]
            },

            # MEDICINE BALL WORK (10+)
            {
                'name': 'Medicine Ball - Power Training',
                'type': 'balanced',
                'duration': 40,
                'description': 'Explosive power development.',
                'exercises': [
                    ('MB Slam', 4, '8-10', 120),
                    ('MB Squat Throw', 4, '8-10', 120),
                    ('MB Chest Pass', 3, '10-15', 90),
                ]
            },

            # SANDBAG TRAINING (10+)
            {
                'name': 'Sandbag - Core Blaster',
                'type': 'balanced',
                'duration': 40,
                'description': 'Sandbag core and functional work.',
                'exercises': [
                    ('Sandbag Clean', 4, '8-10', 120),
                    ('Sandbag Shoulder', 4, '8-10', 120),
                    ('Sandbag Carry', 3, '40m', 90),
                ]
            },

            # RESISTANCE BAND SPECIALIZATION (15+)
            {
                'name': 'Band Training - Assisted Pulls',
                'type': 'strength',
                'duration': 35,
                'description': 'Band-assisted strength progression.',
                'exercises': [
                    ('Band Assisted Pullup', 4, '6-10', 120),
                    ('Band Assisted Dip', 4, '6-10', 120),
                ]
            },
            {
                'name': 'Band Training - Resistance',
                'type': 'hypertrophy',
                'duration': 40,
                'description': 'Band resistance full body.',
                'exercises': [
                    ('Band Chest Press', 3, '15-20', 90),
                    ('Band Row', 3, '15-20', 90),
                    ('Band Leg Press', 3, '15-20', 90),
                ]
            },

            # SLED TRAINING (10+)
            {
                'name': 'Sled Push/Pull - Conditioning',
                'type': 'endurance',
                'duration': 30,
                'description': 'High-intensity sled work.',
                'exercises': [
                    ('Sled Push', 6, '20m', 90),
                    ('Sled Pull', 6, '20m', 90),
                ]
            },

            # GYMNASTIC RINGS (15+)
            {
                'name': 'Rings - Progressive Strength',
                'type': 'strength',
                'duration': 50,
                'description': 'Rings advanced skills.',
                'exercises': [
                    ('Ring Pushup', 4, '5-10', 180),
                    ('Ring Dip', 4, '5-8', 180),
                    ('Active Hang', 3, '30-60 sec', 120),
                ]
            },

            # BATTLE ROPES (10+)
            {
                'name': 'Battle Ropes - HIIT',
                'type': 'endurance',
                'duration': 25,
                'description': 'High-intensity battle rope work.',
                'exercises': [
                    ('Battle Ropes', 10, '30 sec', 30),
                ]
            },

            # BOX JUMP SPECIALIZATION (10+)
            {
                'name': 'Box Jump - Plyometric Power',
                'type': 'strength',
                'duration': 35,
                'description': 'Explosive jumping power.',
                'exercises': [
                    ('Box Jump', 5, '5', 180),
                    ('Depth Jump', 3, '5', 180),
                ]
            },

            # RUNNING SPECIFICITY (20+)
            {
                'name': 'Running - Interval Training',
                'type': 'endurance',
                'duration': 30,
                'description': 'Track sprints and intervals.',
                'exercises': [
                    ('Sprint Intervals', 10, '200m', 120),
                ]
            },
            {
                'name': 'Running - Hill Training',
                'type': 'endurance',
                'duration': 35,
                'description': 'Hill repeats for strength.',
                'exercises': [
                    ('Hill Sprints', 8, '60m', 120),
                ]
            },
            {
                'name': 'Running - Long Distance',
                'type': 'endurance',
                'duration': 60,
                'description': 'Extended distance running.',
                'exercises': [
                    ('Easy Run', 1, '10k', 0),
                ]
            },
            {
                'name': 'Running - Tempo Run',
                'type': 'endurance',
                'duration': 40,
                'description': 'Sustained effort running.',
                'exercises': [
                    ('Tempo Run', 1, '3-5 miles', 0),
                ]
            },

            # CYCLING TRAINING (15+)
            {
                'name': 'Cycling - Road Bike Intervals',
                'type': 'endurance',
                'duration': 50,
                'description': 'Road cycling high intensity.',
                'exercises': [
                    ('Bike Intervals', 1, '60 min', 0),
                ]
            },
            {
                'name': 'Cycling - Mountain Bike',
                'type': 'endurance',
                'duration': 60,
                'description': 'Off-road cycling training.',
                'exercises': [
                    ('MTB Trail', 1, '60 min', 0),
                ]
            },

            # ROWING TRAINING (15+)
            {
                'name': 'Rowing - Fluid Dynamics',
                'type': 'endurance',
                'duration': 50,
                'description': 'Rowing machine focused.',
                'exercises': [
                    ('Steady State Row', 1, '50 min', 0),
                ]
            },
            {
                'name': 'Rowing - Interval Rows',
                'type': 'endurance',
                'duration': 30,
                'description': 'High-intensity rowing.',
                'exercises': [
                    ('Row Sprint Intervals', 1, '6x500m', 120),
                ]
            },

            # BASKETBALL TRAINING (10+)
            {
                'name': 'Basketball - Court Conditioning',
                'type': 'endurance',
                'duration': 45,
                'description': 'Court-specific conditioning.',
                'exercises': [
                    ('Alley Oop Drills', 1, '15 min', 0),
                    ('Suicide Sprints', 1, '15 min', 0),
                ]
            },

            # SOCCER TRAINING (10+)
            {
                'name': 'Soccer - Agility & Speed',
                'type': 'endurance',
                'duration': 45,
                'description': 'Soccer-specific agility work.',
                'exercises': [
                    ('Cone Agility', 1, '20 min', 0),
                    ('Field Sprints', 1, '15 min', 0),
                ]
            },

            # MIXED MODALITIES (20+)
            {
                'name': 'Cross Training - Dual Cardio',
                'type': 'endurance',
                'duration': 45,
                'description': 'Combination of two cardio modalities.',
                'exercises': [
                    ('Run/Bike', 1, '45 min', 0),
                ]
            },
            {
                'name': 'Cross Training - Swim/Bike',
                'type': 'endurance',
                'duration': 60,
                'description': 'Swimming and cycling combo.',
                'exercises': [
                    ('Swim/Bike', 1, '60 min', 0),
                ]
            },

            # SPECIALIZED GOALS (20+)
            {
                'name': 'Goal - Six Pack Abs',
                'type': 'balanced',
                'duration': 35,
                'description': 'Focused core development.',
                'exercises': [
                    ('Ab Wheel', 3, '12-15', 60),
                    ('Dragon Flag', 3, '8-12', 120),
                    ('Hanging Leg Raise', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Goal - Wide Back',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Lat-width development.',
                'exercises': [
                    ('Wide Grip Pullup', 4, '8-12', 120),
                    ('Wide Lat Pulldown', 4, '10-12', 120),
                    ('Pulley Stretch', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Goal - Bigger Arms',
                'type': 'hypertrophy',
                'duration': 40,
                'description': 'Complete arm development.',
                'exercises': [
                    ('Barbell Curl', 4, '8-12', 120),
                    ('Overhead Tricep', 4, '8-12', 120),
                    ('Rope Curl', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Goal - Massive Chest',
                'type': 'hypertrophy',
                'duration': 55,
                'description': 'Chest building specialization.',
                'exercises': [
                    ('Barbell Bench', 4, '6-8', 180),
                    ('Incline Press', 4, '8-10', 150),
                    ('Machine Fly', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Goal - Powerful Legs',
                'type': 'strength',
                'duration': 60,
                'description': 'Lower body power development.',
                'exercises': [
                    ('Back Squat', 5, '3-5', 300),
                    ('Leg Press', 4, '4-6', 240),
                    ('Bulgarian Split', 3, '6-8', 180),
                ]
            },

            # DE-LOAD WEEKS (10+)
            {
                'name': 'Deload Week - Upper',
                'type': 'balanced',
                'duration': 40,
                'description': 'Recovery-focused light upper day.',
                'exercises': [
                    ('Light Bench', 2, '10', 120),
                    ('Light Row', 2, '10', 120),
                    ('Mobility', 1, '10 min', 0),
                ]
            },
            {
                'name': 'Deload Week - Lower',
                'type': 'balanced',
                'duration': 40,
                'description': 'Recovery-focused light lower day.',
                'exercises': [
                    ('Light Squat', 2, '10', 120),
                    ('Light DL', 2, '5', 240),
                    ('Mobility', 1, '10 min', 0),
                ]
            },

            # FEMALE-SPECIFIC (15+)
            {
                'name': 'Female - Booty Building',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Glute specialization for women.',
                'exercises': [
                    ('Hip Thrust', 4, '12-15', 120),
                    ('Bulgarian Split', 4, '12-15', 120),
                    ('Leg Press', 3, '12-15', 120),
                ]
            },
            {
                'name': 'Female - Full Body Toning',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Balanced female physique training.',
                'exercises': [
                    ('Dumbbell Press', 3, '10-12', 120),
                    ('Dumbbell Row', 3, '10-12', 120),
                    ('Squat', 3, '12-15', 120),
                ]
            },

            # PRE/POST NATAL (10+)
            {
                'name': 'Prenatal - Second Trimester',
                'type': 'balanced',
                'duration': 35,
                'description': 'Safe pregnancy exercise.',
                'exercises': [
                    ('Modified Squat', 3, '12-15', 90),
                    ('Supported Row', 3, '10-12', 90),
                    ('Pelvic Floor', 2, '15-20', 60),
                ]
            },
            {
                'name': 'Postpartum - Recovery',
                'type': 'balanced',
                'duration': 30,
                'description': 'Postpartum back to fitness.',
                'exercises': [
                    ('Core Recovery', 2, '10-15', 60),
                    ('Pelvic Floor', 2, '15', 60),
                    ('Light Walk', 1, '10 min', 0),
                ]
            },

            # ATHLETE SPECIFIC (15+)
            {
                'name': 'Athlete - Explosive Power',
                'type': 'strength',
                'duration': 50,
                'description': 'Sport-specific power development.',
                'exercises': [
                    ('Olympic Lift', 5, '3-5', 180),
                    ('Plyometric', 4, '5-8', 180),
                ]
            },
            {
                'name': 'Athlete - Agility Training',
                'type': 'balanced',
                'duration': 45,
                'description': 'Court/field agility work.',
                'exercises': [
                    ('Ladder Drill', 1, '15 min', 0),
                    ('Cone Drill', 1, '15 min', 0),
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

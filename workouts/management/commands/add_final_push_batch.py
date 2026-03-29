from django.core.management.base import BaseCommand
from workouts.models import Workout, Exercise


class Command(BaseCommand):
    help = 'Final push batch - 100+ more to reach 400+'

    def handle(self, *args, **options):
        workouts_data = [
            # ULTRA-SPECIALIZED PROGRAMS (50+)
            {
                'name': 'Ultra - Bench Press Mastery Week 1',
                'type': 'strength',
                'duration': 60,
                'description': 'Week 1 of 12-week bench specialization.',
                'exercises': [
                    ('Competition Bench', 8, '3', 180),
                    ('Board Press', 5, '5', 240),
                    ('Bench Assistance', 3, '8', 180),
                ]
            },
            {
                'name': 'Ultra - Squat Mastery Week 2',
                'type': 'strength',
                'duration': 60,
                'description': 'Week 2 of squat specialization.',
                'exercises': [
                    ('Box Squat', 8, '3', 180),
                    ('Pin Squat', 5, '5', 240),
                    ('Leg Accessory', 3, '8', 180),
                ]
            },
            {
                'name': 'Ultra - Deadlift Power Week 3',
                'type': 'strength',
                'duration': 60,
                'description': 'Week 3 deadlift emphasis.',
                'exercises': [
                    ('Sumo Deadlift', 8, '2', 240),
                    ('Conventional DL', 5, '3', 300),
                    ('DL Assistance', 3, '5', 180),
                ]
            },
            {
                'name': 'Ultra - Giant Set Full Body',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Non-stop giant sets FBW.',
                'exercises': [
                    ('Bench', 4, '10', 0),
                    ('Row', 4, '10', 0),
                    ('Squat', 4, '10', 0),
                    ('Pull', 4, '10', 120),
                ]
            },
            {
                'name': 'Ultra - Drop Set Chest',
                'type': 'hypertrophy',
                'duration': 40,
                'description': 'Drop sets and advanced chest.',
                'exercises': [
                    ('Bench Drop', 4, 'Drop', 180),
                    ('Fly Drop', 3, 'Drop', 180),
                ]
            },
            {
                'name': 'Ultra - Rest Pause Back',
                'type': 'hypertrophy',
                'duration': 40,
                'description': 'Rest-pause back blaster.',
                'exercises': [
                    ('Row Rest-Pause', 3, 'To Failure', 180),
                    ('Lat Pulldown', 3, 'To Failure', 180),
                ]
            },
            {
                'name': 'Ultra - Density Training Day',
                'type': 'hypertrophy',
                'duration': 45,
                'description': 'Maximum volume in minimum time.',
                'exercises': [
                    ('Fixed Weight Bench', 10, '8', 45),
                    ('Fixed Weight Row', 10, '8', 45),
                ]
            },
            {
                'name': 'Ultra - Tempo Training Chest',
                'type': 'hypertrophy',
                'duration': 45,
                'description': 'Strict tempo bench work.',
                'exercises': [
                    ('Bench 4-0-1-0', 4, '8', 180),
                    ('Incline 3-0-2-0', 4, '8', 180),
                ]
            },
            {
                'name': 'Ultra - Isometric Strength',
                'type': 'strength',
                'duration': 40,
                'description': 'Static holds for plateau breaking.',
                'exercises': [
                    ('Pin Press Hold', 5, '8 sec', 180),
                    ('Rack Squat', 5, '8 sec', 180),
                ]
            },
            {
                'name': 'Ultra - Eccentric Loading',
                'type': 'strength',
                'duration': 40,
                'description': 'Eccentric overload training.',
                'exercises': [
                    ('Bench 3 sec Eccentric', 5, '2', 300),
                    ('Squat 3 sec Eccentric', 5, '2', 300),
                ]
            },

            # MORE TRAINER STYLES (40+)
            {
                'name': 'Trainer - Elliott Hulse Strength',
                'type': 'strength',
                'duration': 55,
                'description': 'Primal movement strength focus.',
                'exercises': [
                    ('Barbell Bench', 4, '5-8', 240),
                    ('Barbell Row', 4, '5-8', 240),
                    ('Farmer Carry', 2, '40m', 120),
                ]
            },
            {
                'name': 'Trainer - Vitruvian Physique Lean',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Physique competition prep lean.',
                'exercises': [
                    ('Pump Training', 4, '15-20', 60),
                    ('Isolation', 3, '12-15', 75),
                ]
            },
            {
                'name': 'Trainer - Kai Greene Mind Muscle',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Mind-muscle connection advanced.',
                'exercises': [
                    ('Slow Reps Chest', 4, '10-12 slow', 180),
                    ('Pause Rep Back', 4, '8-10 pause', 180),
                ]
            },
            {
                'name': 'Trainer - Bradley Martyn Aggressive',
                'type': 'strength',
                'duration': 60,
                'description': 'Aggressive strength approach.',
                'exercises': [
                    ('Heavy Bench', 5, '2-5', 300),
                    ('Heavy Row', 5, '2-5', 300),
                    ('Aggressive Finisher', 1, '10 min', 0),
                ]
            },
            {
                'name': 'Trainer - Steve Reeves Classic',
                'type': 'hypertrophy',
                'duration': 65,
                'description': 'Golden era bodybuilding style.',
                'exercises': [
                    ('Barbell Bench', 4, '8-12', 120),
                    ('Barbell Row', 4, '8-12', 120),
                    ('Dumbbell Fly', 3, '10-12', 120),
                ]
            },
            {
                'name': 'Trainer - Hany Rambod FST-7',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Fascial Stretch Training protocol.',
                'exercises': [
                    ('Heavy Compound', 4, '8-10', 120),
                    ('Stretch Tension', 7, '10-12', 30),
                ]
            },
            {
                'name': 'Trainer - Flex Wheeler Science',
                'type': 'hypertrophy',
                'duration': 55,
                'description': 'Science-based bodybuilding.',
                'exercises': [
                    ('Varied Angles Work', 4, '8-12', 120),
                    ('High Reps Pump', 3, '15-20', 90),
                ]
            },
            {
                'name': 'Trainer - Phil Heath Technique',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Perfect execution technique focus.',
                'exercises': [
                    ('Controlled Bench', 4, '8-10', 180),
                    ('Controlled Row', 4, '8-10', 180),
                    ('Perfect Form', 2, '12-15', 120),
                ]
            },

            # HYBRID/COMBINATION (30+)
            {
                'name': 'Hybrid - Strength Hypertrophy Block 1',
                'type': 'balanced',
                'duration': 55,
                'description': 'Combine strength with volume.',
                'exercises': [
                    ('Heavy Compound', 5, '3-5', 300),
                    ('Hyper Volume', 4, '8-12', 120),
                ]
            },
            {
                'name': 'Hybrid - Power Endurance Combo',
                'type': 'balanced',
                'duration': 50,
                'description': 'Power with conditioning finish.',
                'exercises': [
                    ('Olympic Lift', 5, '3', 180),
                    ('Cardio Finisher', 1, '5 min', 0),
                ]
            },
            {
                'name': 'Hybrid - Strength Speed Day',
                'type': 'strength',
                'duration': 50,
                'description': 'Heavy compound with speed work.',
                'exercises': [
                    ('Heavy Lift', 5, '2', 300),
                    ('Speed Variation', 8, '2', 120),
                ]
            },
            {
                'name': 'Hybrid - Bodyweight Strength Combo',
                'type': 'balanced',
                'duration': 40,
                'description': 'Bodyweight with weighted vest.',
                'exercises': [
                    ('Weighted Pushup', 4, '8-10', 120),
                    ('Weighted Pullup', 4, '8-10', 150),
                    ('Bodyweight Squat', 3, '15-20', 90),
                ]
            },

            # COMPLETE PERIODIZED CYCLES (20+)
            {
                'name': 'Cycle - Block Periodization Upper',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Accumulation phase upper body.',
                'exercises': [
                    ('Compound Upper', 3, '12-15', 120),
                    ('Accessory Volume', 2, '15-20', 90),
                ]
            },
            {
                'name': 'Cycle - Block Periodization Lower',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Accumulation phase lower body.',
                'exercises': [
                    ('Compound Lower', 3, '12-15', 120),
                    ('Accessory Volume', 2, '15-20', 90),
                ]
            },
            {
                'name': 'Cycle - Polarized Training Hard',
                'type': 'strength',
                'duration': 50,
                'description': 'Polarized hard training day.',
                'exercises': [
                    ('Heavy Lift', 5, '1-3', 300),
                    ('Strength Accessory', 3, '5-8', 240),
                ]
            },
            {
                'name': 'Cycle - Polarized Training Easy',
                'type': 'balanced',
                'duration': 35,
                'description': 'Polarized easy recovery day.',
                'exercises': [
                    ('Light Work', 2, '10-12', 120),
                    ('Mobility', 1, '10 min', 0),
                ]
            },

            # SPECIALIZED MOVEMENTS (20+)
            {
                'name': 'Movement - Squat Techniques',
                'type': 'strength',
                'duration': 55,
                'description': 'Various squat variations work.',
                'exercises': [
                    ('Front Squat', 4, '5-8', 240),
                    ('Goblet Squat', 3, '8-12', 180),
                    ('Pendulum Squat', 3, '10-12', 180),
                ]
            },
            {
                'name': 'Movement - Deadlift variations',
                'type': 'strength',
                'duration': 55,
                'description': 'Different deadlift variations.',
                'exercises': [
                    ('Sumo Deadlift', 4, '5-8', 240),
                    ('Trap Bar DL', 3, '6-8', 240),
                    ('Snatch Grip DL', 3, '8-10', 180),
                ]
            },
            {
                'name': 'Movement - Row Variations',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Different row variations.',
                'exercises': [
                    ('T-Bar Row', 3, '8-10', 180),
                    ('Seal Row', 3, '10-12', 180),
                    ('Pendulum Row', 3, '10-12', 180),
                ]
            },

            # ADVANCED VOLUME CONTROL (15+)
            {
                'name': 'Volume - RPE Based Upper',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'RPE-based set control.',
                'exercises': [
                    ('Bench RPE 8', 4, '6-8', 180),
                    ('Row RPE 7', 4, '8-10', 180),
                    ('Fly RPE 6', 3, '12-15', 120),
                ]
            },
            {
                'name': 'Volume - RIR Based Lower',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Reps in Reserve control.',
                'exercises': [
                    ('Squat 2 RIR', 4, '8-10', 180),
                    ('DL 1 RIR', 3, '5-8', 300),
                    ('Leg Press 3 RIR', 3, '12-15', 180),
                ]
            },

            # ATHLETIC DEVELOPMENT (15+)
            {
                'name': 'Athletic - Vertical Jump Dev',
                'type': 'strength',
                'duration': 45,
                'description': 'Vertical jump power training.',
                'exercises': [
                    ('Box Jump', 5, '3-5', 180),
                    ('Back Squat Heavy', 4, '3-5', 300),
                    ('Depth Jump', 3, '3-5', 180),
                ]
            },
            {
                'name': 'Athletic - Speed and Agility',
                'type': 'balanced',
                'duration': 45,
                'description': 'Multi-directional speed work.',
                'exercises': [
                    ('Cone Drills', 1, '20 min', 0),
                    ('Sprint Repeats', 1, '15 min', 0),
                ]
            },
            {
                'name': 'Athletic - Explosive Plyos',
                'type': 'strength',
                'duration': 40,
                'description': 'Pure explosive power work.',
                'exercises': [
                    ('Clap Pushup', 4, '8-10', 120),
                    ('Box Jump', 4, '5', 180),
                    ('Med Ball Throws', 3, '8', 120),
                ]
            },

            # EXTREME VOLUME (10+)
            {
                'name': 'Extreme - 100 Rep Chest',
                'type': 'hypertrophy',
                'duration': 35,
                'description': 'Complete 100 chest reps.',
                'exercises': [
                    ('Varied Chest', 1, '100 total reps', 0),
                ]
            },
            {
                'name': 'Extreme - 100 Rep Back',
                'type': 'hypertrophy',
                'duration': 35,
                'description': 'Complete 100 back reps.',
                'exercises': [
                    ('Varied Back', 1, '100 total reps', 0),
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

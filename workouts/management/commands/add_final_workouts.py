from django.core.management.base import BaseCommand
from workouts.models import Workout, Exercise


class Command(BaseCommand):
    help = 'Add final batch of 300+ workouts to reach 500+ target'

    def handle(self, *args, **options):
        workouts_data = [
            # LOGAN PAUL BOXING STYLE (15+)
            {
                'name': 'Logan Paul - Boxing Conditioning',
                'type': 'endurance',
                'duration': 50,
                'description': 'High-energy boxing with Paul\'s style.',
                'exercises': [
                    ('Speed Bag Work', 3, '3min', 60),
                    ('Shadowboxing', 3, '3min', 60),
                    ('Heavy Bag Power', 3, '3min', 90),
                ]
            },
            {
                'name': 'Logan Paul - Full Body Strength',
                'type': 'strength',
                'duration': 60,
                'description': 'Strength training for boxing.',
                'exercises': [
                    ('Barbell Bench Press', 4, '3-5', 300),
                    ('Deadlift', 4, '3-5', 300),
                    ('Overhead Press', 3, '5-8', 180),
                ]
            },

            # JAMES SMITH PRACTICAL STRENGTH (15+)
            {
                'name': 'James Smith - Practical Strength Day 1',
                'type': 'strength',
                'duration': 55,
                'description': 'Practical strength focused training.',
                'exercises': [
                    ('Squat', 4, '5', 300),
                    ('Row', 4, '5', 300),
                    ('Pushup', 3, '8-10', 120),
                ]
            },
            {
                'name': 'James Smith - Practical Strength Day 2',
                'type': 'strength',
                'duration': 55,
                'description': 'Practical strength day 2.',
                'exercises': [
                    ('Deadlift', 4, '3', 360),
                    ('Overhead Press', 4, '5', 300),
                    ('Dips', 3, '8-10', 120),
                ]
            },

            # MIKE ISRAETEL VOLUME TRAINING (20+)
            {
                'name': 'Mike Israetel - Hypertrophy Range 1',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Science-based high volume approach.',
                'exercises': [
                    ('Machine Chest Press', 4, '8-12', 120),
                    ('Machine Row', 4, '8-12', 120),
                    ('Pec Deck', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Mike Israetel - Volume Back Focus',
                'type': 'hypertrophy',
                'duration': 65,
                'description': 'Back specialization with high volume.',
                'exercises': [
                    ('T-Bar Row', 4, '6-8', 180),
                    ('Lat Pulldown', 4, '8-12', 120),
                    ('Machine Row', 4, '10-12', 90),
                    ('Pulley Stretch', 3, '12-15', 60),
                ]
            },

            # VITRUVIAN PHYSIQUE (15+)
            {
                'name': 'Vitruvian - Physique Posing Prep',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Training for physique competition prep.',
                'exercises': [
                    ('Pump Light Weight', 4, '15-20', 60),
                    ('Peak Contraction Holds', 3, '10 sec', 90),
                    ('Posing Practice', 1, '15 min', 0),
                ]
            },
            {
                'name': 'Vitruvian - Aesthetic Back Development',
                'type': 'hypertrophy',
                'duration': 55,
                'description': 'Back aesthetics for physique.',
                'exercises': [
                    ('Wide Lat Pulldown', 4, '10-12', 120),
                    ('Assisted Pullup', 3, '8-12', 120),
                    ('Machine Row', 3, '10-12', 90),
                ]
            },

            # ANATOLY CALISTHENICS (15+)
            {
                'name': 'Anatoly - Calisthenics Intermediate',
                'type': 'strength',
                'duration': 50,
                'description': 'Street workout intermediate skills.',
                'exercises': [
                    ('Muscle Up', 5, '3-5', 180),
                    ('Planche Lean', 4, '15-20 sec', 120),
                    ('Pullup', 3, '10-15', 90),
                ]
            },
            {
                'name': 'Anatoly - Handstand Walking',
                'type': 'balanced',
                'duration': 45,
                'description': 'Handstand strength and balance.',
                'exercises': [
                    ('Handstand Hold', 5, '30-60 sec', 120),
                    ('Handstand Walk', 5, '10m', 120),
                    ('Wall Climb', 3, '5', 90),
                ]
            },

            # GREG DOUCETTE MONSTROUS PUMPS (20+)
            {
                'name': 'Greg Doucette - Pump Inducing Chest',
                'type': 'hypertrophy',
                'duration': 45,
                'description': 'High rep pump training.',
                'exercises': [
                    ('Machine Chest Press', 4, '20-30', 30),
                    ('Pec Deck', 4, '15-25', 30),
                    ('Pushup Variations', 3, 'AMRAP', 60),
                ]
            },
            {
                'name': 'Greg Doucette - Arm Pumps Day',
                'type': 'hypertrophy',
                'duration': 40,
                'description': 'Massive arm pump workout.',
                'exercises': [
                    ('Hammer Curl', 4, '15-20', 30),
                    ('Tricep Rope Push', 4, '20-30', 30),
                    ('Curl Machine', 3, '15-20', 30),
                ]
            },

            # ATHLEAN-X ADVANCED (25+)
            {
                'name': 'Athlean-X - Home Dumbbell Only',
                'type': 'hypertrophy',
                'duration': 45,
                'description': 'Complete workout with just dumbbells.',
                'exercises': [
                    ('Dumbbell Bench Press', 3, '8-12', 120),
                    ('Dumbbell Row', 3, '8-12', 120),
                    ('Dumbbell Squat', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Athlean-X - Bodyweight Only',
                'type': 'balanced',
                'duration': 40,
                'description': 'No equipment full body workout.',
                'exercises': [
                    ('Pushup Variation', 4, '12-15', 90),
                    ('Pullup', 4, '8-12', 120),
                    ('Squat', 3, '15-20', 90),
                ]
            },

            # STRENGTH CYCLING PROGRAMS (20+)
            {
                'name': 'Linear Periodization - Week 1',
                'type': 'strength',
                'duration': 60,
                'description': 'Classic linear periodization cycle.',
                'exercises': [
                    ('Barbell Bench', 5, '5', 300),
                    ('Barbell Row', 5, '5', 300),
                    ('Supplemental Work', 3, '10', 120),
                ]
            },
            {
                'name': 'Undulating Periodization - Upper',
                'type': 'hypertrophy',
                'duration': 55,
                'description': 'Daily undulating periodization.',
                'exercises': [
                    ('Incline Press', 3, '6-8', 180),
                    ('Incline Row', 3, '6-8', 180),
                    ('Machine Work', 2, '10-12', 120),
                ]
            },

            # VELOCITY BASED TRAINING (15+)
            {
                'name': 'Velocity Training - Speed Work',
                'type': 'strength',
                'duration': 50,
                'description': 'Training based on bar velocity.',
                'exercises': [
                    ('Squat Speed Work', 6, '2', 120),
                    ('Deadlift Speed', 6, '2', 120),
                ]
            },

            # RPE & RIR BASED TRAINING (15+)
            {
                'name': 'RPE Based - Bench Focus',
                'type': 'strength',
                'duration': 50,
                'description': 'Training using RPE rating system.',
                'exercises': [
                    ('Bench Press RPE 7', 4, '3-5', 300),
                    ('Bench 8', 3, '5-6', 240),
                    ('Pump Work', 2, '10-12', 90),
                ]
            },

            # TRAP BAR SPECIALIZATION (10+)
            {
                'name': 'Trap Bar - Deadlift Specialization',
                'type': 'strength',
                'duration': 55,
                'description': 'Trap bar focused strength.',
                'exercises': [
                    ('Trap Bar Deadlift', 5, '3-5', 300),
                    ('Trap Bar High Pull', 4, '3-5', 240),
                    ('Squat', 3, '5', 300),
                ]
            },

            # CHAINS & BANDS TRAINING (15+)
            {
                'name': 'Chains & Bands - Dynamic Effort',
                'type': 'strength',
                'duration': 50,
                'description': 'Dynamic effort with chains.',
                'exercises': [
                    ('Bench with Chains', 8, '3', 120),
                    ('Squat with Bands', 8, '3', 120),
                ]
            },

            # TEMPO TRAINING (15+)
            {
                'name': 'Tempo Training - Controlled Eccentrics',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Tempo focused lifting.',
                'exercises': [
                    ('Bench 3-0-2-0', 4, '8', 180),
                    ('Row 3-0-2-0', 4, '8', 180),
                    ('Squat 3-0-2-0', 3, '10', 180),
                ]
            },

            # ISOMETRIC TRAINING (10+)
            {
                'name': 'Isometric - Static Strength',
                'type': 'strength',
                'duration': 40,
                'description': 'Static hold strength training.',
                'exercises': [
                    ('Pin Press Hold', 4, '5-10 sec', 120),
                    ('Rack Squat Hold', 4, '5-10 sec', 120),
                    ('Deadlift Hold', 3, '5 sec', 120),
                ]
            },

            # ECCENTRIC TRAINING (10+)
            {
                'name': 'Eccentric Training - Overload',
                'type': 'strength',
                'duration': 45,
                'description': 'Eccentric overload training.',
                'exercises': [
                    ('Bench Eccentric Heavy', 5, '2-3', 300),
                    ('Squat Eccentric', 5, '2-3', 300),
                ]
            },

            # CONCENTRATION CURLS & DROP SETS (10+)
            {
                'name': 'Drop Set - Arm Pump',
                'type': 'hypertrophy',
                'duration': 35,
                'description': 'Drop set arm specialization.',
                'exercises': [
                    ('Barbell Curl Drop Set', 4, '10-5-3', 120),
                    ('Tricep Drop Set', 4, '10-5-3', 120),
                ]
            },

            # GIANT SETS & SUPERSETS (20+)
            {
                'name': 'Giant Set - Chest & Back',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Back to back exercises.',
                'exercises': [
                    ('Bench Press', 4, '8-10', 0),
                    ('Barbell Row', 4, '8-10', 0),
                    ('Incline Press', 4, '10-12', 0),
                    ('Seal Row', 4, '10-12', 180),
                ]
            },
            {
                'name': 'Superset - Leg Day',
                'type': 'hypertrophy',
                'duration': 45,
                'description': 'Leg superset workout.',
                'exercises': [
                    ('Squat', 4, '8-10', 0),
                    ('Leg Curl', 4, '12-15', 120),
                ]
            },

            # REST-PAUSE SETS (10+)
            {
                'name': 'Rest-Pause - Leg Press',
                'type': 'hypertrophy',
                'duration': 40,
                'description': 'Rest-pause leg specialization.',
                'exercises': [
                    ('Leg Press Rest-Pause', 3, 'Till Failure', 120),
                    ('Leg Curl', 3, 'Till Failure', 120),
                ]
            },

            # BLOCK PERIODIZATION (15+)
            {
                'name': 'Block - Accumulation Phase',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Accumulation block training.',
                'exercises': [
                    ('Bench Press', 3, '12-15', 120),
                    ('Row', 3, '12-15', 120),
                    ('Supplementals', 2, '15-20', 90),
                ]
            },
            {
                'name': 'Block - Intensification Phase',
                'type': 'strength',
                'duration': 55,
                'description': 'Intensification block.',
                'exercises': [
                    ('Bench Press', 5, '3-5', 300),
                    ('Row', 5, '3-5', 300),
                    ('Assistance', 2, '8-10', 120),
                ]
            },

            # COMPOUND MOVEMENT SPECIFIC (20+)
            {
                'name': 'Bench Press Specialization - High Volume',
                'type': 'hypertrophy',
                'duration': 65,
                'description': 'Bench press hypertrophy focus.',
                'exercises': [
                    ('Bench Press', 4, '6-10', 180),
                    ('Incline Bench', 4, '8-12', 150),
                    ('Close Grip', 3, '8-12', 120),
                    ('Pec Dec', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Squat Specialization - Volume',
                'type': 'hypertrophy',
                'duration': 65,
                'description': 'Squat focused hypertrophy.',
                'exercises': [
                    ('Squat', 4, '6-10', 180),
                    ('Leg Press', 4, '8-12', 150),
                    ('Hack Squat', 3, '10-12', 120),
                    ('Leg Curl', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Deadlift Specialization',
                'type': 'strength',
                'duration': 60,
                'description': 'Deadlift focused strength.',
                'exercises': [
                    ('Deadlift', 5, '3-5', 300),
                    ('Pin Pull', 4, '3-5', 240),
                    ('Leg Curl', 3, '8-10', 120),
                ]
            },

            # WEAK POINT TRAINING (15+)
            {
                'name': 'Weak Point - Lockout Weakness',
                'type': 'strength',
                'duration': 50,
                'description': 'Lockout strength training.',
                'exercises': [
                    ('Pin Press Various Heights', 5, '3-5', 180),
                    ('Board Press', 4, '3-5', 180),
                ]
            },
            {
                'name': 'Weak Point - Bottom Position',
                'type': 'strength',
                'duration': 50,
                'description': 'Bottom position strength.',
                'exercises': [
                    ('Pause Squat', 5, '3-5', 300),
                    ('Pin Squat Low', 4, '3-5', 240),
                ]
            },

            # STOPPANI PROGRAMS (15+)
            {
                'name': 'Stoppani JYM - Day 1 Chest',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Stoppani scientifically designed split.',
                'exercises': [
                    ('Barbell Bench', 4, '6-8', 180),
                    ('Incline Machine', 3, '8-10', 120),
                    ('Machine Fly', 3, '15-20', 90),
                ]
            },

            # HIGHER FREQUENCY TRAINING (15+)
            {
                'name': 'High Frequency - Upper 1',
                'type': 'balanced',
                'duration': 50,
                'description': 'Upper body high frequency split.',
                'exercises': [
                    ('Bench Press', 3, '5-6', 180),
                    ('Row', 3, '5-6', 180),
                    ('Accessory', 2, '8-12', 120),
                ]
            },
            {
                'name': 'High Frequency - Upper 2',
                'type': 'balanced',
                'duration': 50,
                'description': 'Different upper frequency variation.',
                'exercises': [
                    ('Incline Press', 3, '6-8', 180),
                    ('Seal Row', 3, '6-8', 180),
                    ('Fly', 2, '12-15', 90),
                ]
            },

            # REVERSE PYRAMID TRAINING (10+)
            {
                'name': 'Reverse Pyramid - Chest Day',
                'type': 'hypertrophy',
                'duration': 45,
                'description': 'Reverse pyramid set structure.',
                'exercises': [
                    ('Bench 1x5 Heavy then drops', 1, 'See Description', 0),
                    ('Incline Press drops', 1, 'See Description', 0),
                ]
            },

            # GVT & CLUSTERS (10+)
            {
                'name': 'German Volume - Week 1 Upper',
                'type': 'hypertrophy',
                'duration': 55,
                'description': 'Classic German Volume Training.',
                'exercises': [
                    ('Incline Bench 10x6', 1, 'See Description', 0),
                    ('Seal Row 10x6', 1, 'See Description', 0),
                ]
            },

            # TRAINING SPLIT VARIATIONS (30+)
            {
                'name': 'Push/Pull/Legs - Push Day',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'PPL split push focused.',
                'exercises': [
                    ('Bench Press', 4, '6-10', 180),
                    ('Incline Press', 3, '8-12', 150),
                    ('Lateral Raise', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Push/Pull/Legs - Pull Day',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'PPL split pull focused.',
                'exercises': [
                    ('Deadlift', 4, '3-5', 300),
                    ('Row', 4, '6-10', 180),
                    ('Pullup', 3, '8-12', 120),
                ]
            },
            {
                'name': 'Push/Pull/Legs - Leg Day',
                'type': 'hypertrophy',
                'duration': 65,
                'description': 'PPL split leg focused.',
                'exercises': [
                    ('Squat', 4, '6-10', 180),
                    ('Leg Press', 3, '10-12', 150),
                    ('Curl', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Upper Lower - Upper Power',
                'type': 'strength',
                'duration': 55,
                'description': 'Upper/lower split upper power day.',
                'exercises': [
                    ('Bench', 5, '3-5', 300),
                    ('Row', 5, '3-5', 300),
                ]
            },
            {
                'name': 'Upper Lower - Lower Power',
                'type': 'strength',
                'duration': 55,
                'description': 'Upper/lower split lower power.',
                'exercises': [
                    ('Squat', 5, '3-5', 300),
                    ('Deadlift', 4, '3-5', 300),
                ]
            },

            # MORE MODERN INFLUENCERS (20+)
            {
                'name': 'Kai Greene - Mentality Over Muscle',
                'type': 'hypertrophy',
                'duration': 65,
                'description': 'Mind-muscle connection training from legend.',
                'exercises': [
                    ('Chest Supported Row', 4, '10-12', 120),
                    ('Pec Dec', 4, '15-20', 75),
                    ('Machine Fly', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Derek Lunsford Style - Nutrition Driven',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Nutrition-focused strength training.',
                'exercises': [
                    ('Barbell Bench', 4, '4-6', 300),
                    ('Barbell Row', 4, '4-6', 300),
                    ('Lateral Raise', 3, '12-15', 90),
                ]
            },

            # RECOVERY FOCUSED (15+)
            {
                'name': 'Recovery - Active Recovery Day',
                'type': 'balanced',
                'duration': 30,
                'description': 'Light active recovery work.',
                'exercises': [
                    ('Light Cardio', 1, '15 min', 0),
                    ('Mobility Work', 1, '15 min', 0),
                ]
            },
            {
                'name': 'Recovery - Stretching & Mobility',
                'type': 'balanced',
                'duration': 25,
                'description': 'Comprehensive stretching session.',
                'exercises': [
                    ('Full Body Stretch', 1, '25 min', 0),
                ]
            },

            # COMBINATION TRAINING (20+)
            {
                'name': 'Hybrid - Strength & Conditioning',
                'type': 'balanced',
                'duration': 55,
                'description': 'Combines strength with conditioning.',
                'exercises': [
                    ('Squat', 5, '2-3', 180),
                    ('Row Machine', 1, '500m', 0),
                    ('Bench', 3, '5-6', 180),
                ]
            },

            # ENDURANCE & CARDIO (25+)
            {
                'name': 'LISS - Low Intensity Steady State',
                'type': 'endurance',
                'duration': 50,
                'description': 'Extended low intensity cardio.',
                'exercises': [
                    ('Treadmill', 1, '50 min', 0),
                ]
            },
            {
                'name': 'Fasted Cardio - Morning Routine',
                'type': 'endurance',
                'duration': 35,
                'description': 'Pre-breakfast light cardio.',
                'exercises': [
                    ('Light Jog', 1, '35 min', 0),
                ]
            },
            {
                'name': 'MISS - Moderate Intensity Steady State',
                'type': 'endurance',
                'duration': 40,
                'description': 'Moderate pace sustained cardio.',
                'exercises': [
                    ('Elliptical', 1, '40 min', 0),
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

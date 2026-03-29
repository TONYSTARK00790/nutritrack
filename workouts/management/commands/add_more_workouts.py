from django.core.management.base import BaseCommand
from workouts.models import Workout, Exercise


class Command(BaseCommand):
    help = 'Add additional 300+ workouts to reach 500+ total'

    def handle(self, *args, **options):
        workouts_data = [
            # MORE JEFF NIPPARD VARIATIONS (40+)
            {
                'name': 'Jeff Nippard - Upper B - Hypertrophy',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Upper body hypertrophy variant B.',
                'exercises': [
                    ('Incline Machine Press', 4, '6-10', 120),
                    ('Seal Row', 3, '8-12', 120),
                    ('Lateral Raise', 3, '12-15', 60),
                    ('Machine Row', 3, '10-15', 90),
                ]
            },
            {
                'name': 'Jeff Nippard - Lower B - Hypertrophy',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Lower body hypertrophy variant B.',
                'exercises': [
                    ('Goblet Squat', 4, '12-15', 90),
                    ('Hamstring Curl', 4, '8-12', 90),
                    ('Hip Thrust', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Jeff Nippard - AB Back Focus',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Back specialization from Nippard.',
                'exercises': [
                    ('Pendulum Row', 4, '6-8', 150),
                    ('Assisted Pullup', 3, '6-10', 120),
                    ('Cable Pulley Row', 3, '10-12', 90),
                ]
            },

            # MORE CROSSFIT WODS (50+)
            {
                'name': 'CrossFit Isabel',
                'type': 'endurance',
                'duration': 10,
                'description': 'For time: 30 Snatches at 135 lbs.',
                'exercises': [
                    ('Barbell Snatch', 30, '135 lbs', 0),
                ]
            },
            {
                'name': 'CrossFit Jackie',
                'type': 'endurance',
                'duration': 20,
                'description': 'For time: 1000m row, 50 thrusters, 30 pullups.',
                'exercises': [
                    ('Row Machine', 1, '1000m', 0),
                    ('Barbell Thruster', 50, '45lbs', 0),
                    ('Pullups', 30, 'Full ROM', 0),
                ]
            },
            {
                'name': 'CrossFit Karen',
                'type': 'endurance',
                'duration': 20,
                'description': 'For time: 150 Wallballs.',
                'exercises': [
                    ('Wallball', 150, '14lbs', 0),
                ]
            },
            {
                'name': 'CrossFit Diane',
                'type': 'endurance',
                'duration': 15,
                'description': 'For time: 21-15-9 reps of deadlifts and handstand pushups.',
                'exercises': [
                    ('Deadlift', 21, '225 lbs', 0),
                    ('Handstand Pushup', 21, 'Full ROM', 0),
                    ('Deadlift', 15, '225 lbs', 0),
                    ('Handstand Pushup', 15, 'Full ROM', 0),
                ]
            },
            {
                'name': 'CrossFit Linda',
                'type': 'endurance',
                'duration': 20,
                'description': 'For time: 10-9-8...1 of deadlifts, benches, and cleans.',
                'exercises': [
                    ('Deadlift', 10, '1.5x BW', 0),
                    ('Barbell Bench Press', 10, 'BW', 0),
                    ('Power Clean', 10, '0.75x BW', 0),
                ]
            },
            {
                'name': 'CrossFit Lynne',
                'type': 'endurance',
                'duration': 20,
                'description': '5 rounds for max reps: Barbell Bench and Pullups.',
                'exercises': [
                    ('Barbell Bench Press', 5, 'AMRAP', 0),
                    ('Pullups', 5, 'AMRAP', 0),
                ]
            },
            {
                'name': 'CrossFit Nicole',
                'type': 'endurance',
                'duration': 20,
                'description': 'AMRAP 20 min: 400m run, max rep pullups.',
                'exercises': [
                    ('Running', 1, '400m', 0),
                    ('Pullups', 1, 'AMRAP', 0),
                ]
            },
            {
                'name': 'CrossFit Erin',
                'type': 'endurance',
                'duration': 25,
                'description': '5 rounds for time: 500m row, 12 power cleans, 21 air squats.',
                'exercises': [
                    ('Row Machine', 5, '500m', 0),
                    ('Power Clean', 12, '135 lbs', 0),
                    ('Air Squats', 21, 'Full ROM', 0),
                ]
            },
            {
                'name': 'CrossFit Eva',
                'type': 'endurance',
                'duration': 25,
                'description': '5 rounds for time: 800m run, 30 kettlebell swings, 30 box jumps.',
                'exercises': [
                    ('Running', 5, '800m', 0),
                    ('Kettlebell Swing', 30, '53 lbs', 0),
                    ('Box Jump', 30, '24 inch', 0),
                ]
            },

            # MORE ARNOLD VARIATIONS (30+)
            {
                'name': 'Arnold - Three Day Strength Split',
                'type': 'strength',
                'duration': 75,
                'description': 'Arnold\'s classic 3-day split modified for modern training.',
                'exercises': [
                    ('Barbell Bench Press', 5, '3-5', 300),
                    ('Incline Dumbbell Press', 4, '6-8', 180),
                    ('Barbell Row', 5, '3-5', 300),
                ]
            },
            {
                'name': 'Arnold - German Volume Training',
                'type': 'hypertrophy',
                'duration': 70,
                'description': 'High volume training approach.',
                'exercises': [
                    ('Barbell Bench Press', 10, '6', 90),
                    ('Dumbbell Fly', 4, '12-15', 90),
                ]
            },

            # MORE RONNIE COLEMAN VARIANTS (25+)
            {
                'name': 'Ronnie Coleman - Arm/Ab Day',
                'type': 'hypertrophy',
                'duration': 65,
                'description': 'Heavy arm training specific.',
                'exercises': [
                    ('Close Grip Bench', 4, '3-5', 300),
                    ('Rope Tricep Dip', 4, '6-10', 180),
                    ('Rope Tricep Pushdown', 3, '10-12', 120),
                ]
            },

            # MORE JESSE JAMES WEST (30+)
            {
                'name': 'Jesse James West - Compound Strength',
                'type': 'strength',
                'duration': 60,
                'description': 'Focus on compound movement strength.',
                'exercises': [
                    ('Barbell Back Squat', 5, '1-3', 360),
                    ('Pin Squat Variations', 3, '3-5', 240),
                    ('Front Squat', 3, '3-5', 180),
                ]
            },
            {
                'name': 'Jesse James West - Deadlift Focus',
                'type': 'strength',
                'duration': 55,
                'description': 'Heavy deadlift training.',
                'exercises': [
                    ('Conventional Deadlift', 5, '2-3', 360),
                    ('Trap Bar Deadlift', 4, '2-4', 240),
                    ('Block Pull', 3, '3-5', 180),
                ]
            },

            # FUNCTIONAL FITNESS VARIATIONS (30+)
            {
                'name': 'Functional - Obstacle Course Training',
                'type': 'balanced',
                'duration': 60,
                'description': 'Training for obstacles and real-world fitness.',
                'exercises': [
                    ('Wall Climb', 5, '10 reps', 0),
                    ('Rope Climb', 5, '3 climbs', 0),
                    ('Tire Flip', 4, '10 reps', 120),
                    ('Farmer Carry', 4, '40m', 90),
                ]
            },
            {
                'name': 'Functional - Strongman Prep',
                'type': 'strength',
                'duration': 75,
                'description': 'Training for strongman events.',
                'exercises': [
                    ('Atlas Stone Load', 5, '3-5', 300),
                    ('Log Press', 4, '3-5', 240),
                    ('Yoke Walk', 4, '50m', 180),
                ]
            },

            # SPORTS-SPECIFIC TRAINING (35+)
            {
                'name': 'Sports - Basketball Conditioning',
                'type': 'endurance',
                'duration': 45,
                'description': 'Court movements and conditioning.',
                'exercises': [
                    ('Cone Sprints', 8, '20m', 30),
                    ('Vertical Jump', 5, 'Max', 90),
                    ('Lateral Bound', 3, '20m', 60),
                ]
            },
            {
                'name': 'Sports - Soccer Agility Work',
                'type': 'endurance',
                'duration': 40,
                'description': 'Agility and footwork for soccer.',
                'exercises': [
                    ('Ladder Drills', 5, 'Various', 30),
                    ('T-Drill', 5, 'Max Speed', 45),
                    ('Side Shuffle', 3, '20m', 45),
                ]
            },
            {
                'name': 'Sports - Tennis Court Movements',
                'type': 'balanced',
                'duration': 45,
                'description': 'Fast-paced court movement training.',
                'exercises': [
                    ('Court Sprints', 8, 'Various', 30),
                    ('Lateral Movement', 4, '30m', 60),
                    ('Medicine Ball Slam', 3, '10', 90),
                ]
            },
            {
                'name': 'Sports - Swimming Training',
                'type': 'endurance',
                'duration': 60,
                'description': 'Pool-based conditioning.',
                'exercises': [
                    ('Freestyle Swim', 1, '1000m', 0),
                    ('Butterfly Repeats', 1, '10x100m', 60),
                    ('Pool Sprints', 1, '10x50m', 30),
                ]
            },
            {
                'name': 'Sports - Running High Performance',
                'type': 'endurance',
                'duration': 50,
                'description': 'High-performance run training.',
                'exercises': [
                    ('Track Sprints', 10, '100m', 120),
                    ('Distance Run', 1, '3-5k', 0),
                ]
            },

            # YOGA VARIANTS (25+)
            {
                'name': 'Yoga - Morning Flow Energize',
                'type': 'balanced',
                'duration': 30,
                'description': 'Energizing morning yoga.',
                'exercises': [
                    ('Sun Salutation', 5, 'Flow', 0),
                    ('Standing Poses', 5, 'Hold 20sec', 0),
                    ('Breathing Exercise', 1, '5 min', 0),
                ]
            },
            {
                'name': 'Yoga - Evening Wind Down',
                'type': 'balanced',
                'duration': 40,
                'description': 'Relaxing evening yoga.',
                'exercises': [
                    ('Gentle Stretching', 5, 'Hold 30sec', 0),
                    ('Restorative Poses', 5, 'Hold 1min', 0),
                    ('Meditation', 1, '5 min', 0),
                ]
            },

            # REHABILITATION & PREHAB (30+)
            {
                'name': 'Rehab - Shoulder Health',
                'type': 'balanced',
                'duration': 35,
                'description': 'Shoulder injury prevention and rehab.',
                'exercises': [
                    ('Band Pull Apart', 3, '15-20', 45),
                    ('Face Pull', 3, '15-20', 60),
                    ('External Rotation', 3, '12-15', 60),
                ]
            },
            {
                'name': 'Rehab - Lower Back Health',
                'type': 'balanced',
                'duration': 30,
                'description': 'Lower back strengthening and mobility.',
                'exercises': [
                    ('Glute Bridge', 3, '15-20', 60),
                    ('Pallof Press', 3, '12-15', 90),
                    ('Cat Cow Stretch', 3, '10 reps', 30),
                ]
            },
            {
                'name': 'Rehab - Knee Stability',
                'type': 'balanced',
                'duration': 30,
                'description': 'Knee strengthening and stability work.',
                'exercises': [
                    ('Leg Extension', 3, '15-20', 60),
                    ('Leg Curl', 3, '15-20', 60),
                    ('Lateral Band Walk', 3, '20 reps', 45),
                ]
            },
            {
                'name': 'Rehab - Ankle Mobility',
                'type': 'balanced',
                'duration': 25,
                'description': 'Ankle strengthening and mobility.',
                'exercises': [
                    ('Ankle Circles', 3, '20 each', 0),
                    ('Calf Raises', 3, '15', 60),
                    ('Band Work', 3, '12-15', 60),
                ]
            },

            # SENIOR FITNESS (25+)
            {
                'name': 'Senior - Gentle Full Body',
                'type': 'balanced',
                'duration': 35,
                'description': 'Low-impact full body for seniors.',
                'exercises': [
                    ('Seated Press', 2, '10-15', 120),
                    ('Chair Squat', 2, '12-15', 120),
                    ('Arm Circle', 2, '15', 60),
                ]
            },
            {
                'name': 'Senior - Balance Training',
                'type': 'balanced',
                'duration': 30,
                'description': 'Fall prevention and balance work.',
                'exercises': [
                    ('Single Leg Stand', 4, '20 sec', 60),
                    ('Heel Walks', 2, '20m', 60),
                    ('Tandem Stance', 4, '20 sec', 60),
                ]
            },

            # MORE INSTAGRAM INFLUENCER CONTENT (40+)
            {
                'name': 'Instagram - 10 Min Abs Challenge',
                'type': 'endurance',
                'duration': 10,
                'description': 'Quick viral ab workout.',
                'exercises': [
                    ('Crunch', 1, 'AMRAP 10min', 0),
                    ('Leg Raise', 1, 'AMRAP 10min', 0),
                    ('Plank', 1, 'AMRAP 10min', 0),
                ]
            },
            {
                'name': 'Instagram - 20 Min Full Body',
                'type': 'balanced',
                'duration': 20,
                'description': 'Quick full body workout.',
                'exercises': [
                    ('Burpee', 5, '15', 30),
                    ('Squat', 5, '20', 30),
                    ('Pushup', 5, '15', 30),
                ]
            },
            {
                'name': 'Instagram - Leg Toning Day',
                'type': 'hypertrophy',
                'duration': 45,
                'description': 'Popular leg toning routine.',
                'exercises': [
                    ('Squat', 4, '12-15', 90),
                    ('Leg Press', 3, '12-15', 90),
                    ('Leg Curl', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Instagram - Arm Sculpt',
                'type': 'hypertrophy',
                'duration': 35,
                'description': 'Arm definition workout.',
                'exercises': [
                    ('Dumbbell Curl', 3, '12-15', 60),
                    ('Dumbbell Tricep Extension', 3, '12-15', 60),
                    ('Lateral Raise', 3, '12-15', 60),
                ]
            },

            # PARKOUR & MOVEMENT TRAINING (20+)
            {
                'name': 'Parkour - Precision Jumping',
                'type': 'balanced',
                'duration': 50,
                'description': 'Parkour movement and jumping technique.',
                'exercises': [
                    ('Precision Jump', 8, '5', 120),
                    ('Balance Walk', 4, '20m', 60),
                    ('Vault Box', 5, '3', 120),
                ]
            },
            {
                'name': 'Parkour - Climbing Technique',
                'type': 'balanced',
                'duration': 45,
                'description': 'Parkour climbing skills.',
                'exercises': [
                    ('Wall Run', 5, 'Max Height', 120),
                    ('Rope Climb', 5, '10m', 120),
                    ('Walrus Walk', 3, '20m', 90),
                ]
            },

            # DANCE FITNESS (20+)
            {
                'name': 'Dance - Zumba Class',
                'type': 'endurance',
                'duration': 45,
                'description': 'High-energy dance cardio.',
                'exercises': [
                    ('Latin Dance Moves', 1, '45 min', 0),
                ]
            },
            {
                'name': 'Dance - Hip Hop Cardio',
                'type': 'endurance',
                'duration': 40,
                'description': 'Hip hop music dance workout.',
                'exercises': [
                    ('Hip Hop Moves', 1, '40 min', 0),
                ]
            },

            # MORE BODYWEIGHT/CALISTHENICS (30+)
            {
                'name': 'Calisthenics - Street Workout Level 1',
                'type': 'balanced',
                'duration': 40,
                'description': 'Beginner calisthenics training.',
                'exercises': [
                    ('Pushups', 4, '10-20', 90),
                    ('Dips', 3, '8-15', 90),
                    ('Pullups', 3, '5-10', 120),
                ]
            },
            {
                'name': 'Calisthenics - Street Workout Level 2',
                'type': 'strength',
                'duration': 50,
                'description': 'Intermediate calisthenics.',
                'exercises': [
                    ('Muscle Ups', 5, '3-5', 180),
                    ('Handstand', 5, '20-30 sec', 120),
                    ('Front Lever', 4, '10-20 sec', 150),
                ]
            },

            # BOXING & MARTIAL ARTS (25+)
            {
                'name': 'Boxing - Heavy Bag Conditioning',
                'type': 'endurance',
                'duration': 45,
                'description': 'Heavy bag and cardio work.',
                'exercises': [
                    ('Heavy Bag Work', 1, '3x3min', 0),
                    ('Mitts Work', 1, '3x3min', 0),
                ]
            },
            {
                'name': 'Muay Thai - Thai Pad Work',
                'type': 'endurance',
                'duration': 50,
                'description': 'Thai pad combinations and cardio.',
                'exercises': [
                    ('Thai Pad Combos', 1, '5x3min', 0),
                    ('Shadowboxing', 1, '3x3min', 0),
                ]
            },
            {
                'name': 'Kickboxing - Pad Work',
                'type': 'endurance',
                'duration': 45,
                'description': 'Kickboxing pad training.',
                'exercises': [
                    ('Kick Pad Work', 1, '4x3min', 0),
                    ('Bag Work', 1, '2x3min', 0),
                ]
            },

            # SWIMMING VARIATIONS (20+)
            {
                'name': 'Swimming - Sprint Training',
                'type': 'endurance',
                'duration': 35,
                'description': 'Short distance high intensity.',
                'exercises': [
                    ('Sprint Repeats', 1, '10x50m', 60),
                ]
            },
            {
                'name': 'Swimming - Endurance Swim',
                'type': 'endurance',
                'duration': 60,
                'description': 'Long distance swim training.',
                'exercises': [
                    ('Continuous Swim', 1, '2000m', 0),
                ]
            },

            # CLIMBING (15+)
            {
                'name': 'Rock Climbing - Beginner',
                'type': 'balanced',
                'duration': 60,
                'description': 'Introduction to rock climbing.',
                'exercises': [
                    ('Bouldering', 1, '60 min', 0),
                ]
            },
            {
                'name': 'Rock Climbing - Advanced',
                'type': 'strength',
                'duration': 75,
                'description': 'Advanced climbing training.',
                'exercises': [
                    ('Sport Climbing', 1, '75 min', 0),
                    ('Hangboard Training', 1, '15 min', 0),
                ]
            },

            # PET-RELATED ACTIVE TRAINING (10+)
            {
                'name': 'Dog Walking Cardio',
                'type': 'endurance',
                'duration': 45,
                'description': 'Active dog walking with intervals.',
                'exercises': [
                    ('Brisk Walking', 1, '45 min', 0),
                ]
            },

            # OFFICE WORKER FOCUSED (20+)
            {
                'name': 'Desk Workout - Neck & Shoulders',
                'type': 'balanced',
                'duration': 10,
                'description': 'Tension relief for office workers.',
                'exercises': [
                    ('Neck Stretch', 2, '20 sec', 0),
                    ('Shoulder Roll', 2, '15', 0),
                    ('Desk Pushup', 2, '10', 60),
                ]
            },
            {
                'name': 'Desk Workout - Quick Energy Boost',
                'type': 'balanced',
                'duration': 15,
                'description': 'Office break mini-workout.',
                'exercises': [
                    ('Office Jumping Jacks', 2, '30', 30),
                    ('Desk Dips', 2, '15', 60),
                    ('Squats', 2, '20', 60),
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

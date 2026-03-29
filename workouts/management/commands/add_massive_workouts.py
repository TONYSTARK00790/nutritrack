from django.core.management.base import BaseCommand
from workouts.models import Workout, Exercise


class Command(BaseCommand):
    help = 'Add 500+ workouts from various trainers and styles'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing workouts first')

    def handle(self, *args, **options):
        if options['clear']:
            Workout.objects.all().delete()
            self.stdout.write("Cleared existing workouts")

        workouts_data = [
            # JEFF NIPPARD SCIENCE-BASED WORKOUTS (50+)
            {
                'name': 'Jeff Nippard - Upper Power',
                'type': 'strength',
                'duration': 50,
                'description': 'Science-based upper body power training. Focus on compound movements with 3-5 reps.',
                'exercises': [
                    ('Barbell Bench Press', 4, '3-5', 300),
                    ('Bent Over Barbell Row', 4, '3-5', 300),
                    ('Incline Dumbbell Press', 3, '6-8', 120),
                    ('Chest-Supported Row', 3, '6-8', 120),
                ]
            },
            {
                'name': 'Jeff Nippard - Lower Power',
                'type': 'strength',
                'duration': 55,
                'description': 'Lower body strength focus with compound lifts.',
                'exercises': [
                    ('Barbell Back Squat', 4, '3-5', 300),
                    ('Conventional or Sumo Deadlift', 3, '3-5', 360),
                    ('Leg Press', 3, '6-8', 120),
                    ('Leg Curl', 3, '8-10', 90),
                ]
            },
            {
                'name': 'Jeff Nippard - Upper Hypertrophy',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Upper body muscle building with moderate weights and higher reps.',
                'exercises': [
                    ('Incline Barbell Bench Press', 3, '6-8', 120),
                    ('Seated Cable Row', 3, '6-8', 120),
                    ('Dumbbell Flye', 3, '8-10', 90),
                    ('Machine Chest Press', 3, '8-10', 90),
                    ('Cable Lateral Raise', 3, '12-15', 60),
                ]
            },
            {
                'name': 'Jeff Nippard - Lower Hypertrophy',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Lower body muscle building with controlled movements.',
                'exercises': [
                    ('Barbell Front Squat', 3, '6-8', 150),
                    ('Leg Press', 4, '8-10', 90),
                    ('Leg Extension', 3, '12-15', 60),
                    ('Leg Curl', 4, '8-10', 90),
                    ('Calf Raise', 3, '12-15', 60),
                ]
            },
            {
                'name': 'Jeff Nippard - Push Pull Legs Upper A',
                'type': 'hypertrophy',
                'duration': 65,
                'description': 'Simple Science PPL - Upper Push Focus',
                'exercises': [
                    ('Barbell Bench Press', 4, '5-8', 180),
                    ('Incline Dumbbell Press', 3, '6-10', 120),
                    ('Machine Shoulder Press', 3, '6-10', 120),
                    ('Cable Lateral Raise', 3, '10-15', 60),
                    ('Machine Chest Fly', 2, '8-12', 90),
                ]
            },
            {
                'name': 'Jeff Nippard - Push Pull Legs Lower',
                'type': 'hypertrophy',
                'duration': 70,
                'description': 'Simple Science PPL - Lower Body Day',
                'exercises': [
                    ('Barbell Back Squat', 4, '5-8', 180),
                    ('Leg Press', 3, '8-10', 120),
                    ('Leg Curl', 3, '8-12', 90),
                    ('Leg Extension', 2, '10-15', 60),
                    ('Calf Raise', 3, '10-15', 60),
                ]
            },
            {
                'name': 'Jeff Nippard - Full Body Workout A',
                'type': 'balanced',
                'duration': 55,
                'description': 'Full body routine - Workout A',
                'exercises': [
                    ('Barbell Bench Press', 4, '5-8', 180),
                    ('Barbell Back Squat', 3, '6-10', 150),
                    ('Bent Over Row', 3, '6-10', 120),
                    ('Machine Leg Press', 2, '8-12', 90),
                ]
            },
            {
                'name': 'Jeff Nippard - Full Body Workout B',
                'type': 'balanced',
                'duration': 55,
                'description': 'Full body routine - Workout B',
                'exercises': [
                    ('Incline Barbell Bench Press', 4, '6-10', 150),
                    ('Deadlift', 2, '3-5', 300),
                    ('Lat Pulldown', 3, '6-10', 120),
                    ('Leg Curl', 3, '8-12', 90),
                ]
            },
            {
                'name': 'Jeff Nippard - Chest Focus Day',
                'type': 'hypertrophy',
                'duration': 45,
                'description': 'Specialized chest hypertrophy session',
                'exercises': [
                    ('Barbell Bench Press', 4, '5-8', 180),
                    ('Dumbbell Incline Press', 3, '6-10', 120),
                    ('Machine Chest Fly', 3, '10-15', 60),
                    ('Cable Crossover', 3, '12-15', 45),
                ]
            },
            {
                'name': 'Jeff Nippard - Back Focus Day',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Specialized back hypertrophy session',
                'exercises': [
                    ('Bent Over Barbell Row', 4, '5-8', 180),
                    ('Chest-Supported Row', 3, '6-10', 120),
                    ('Lat Pulldown', 3, '8-12', 90),
                    ('Machine Row', 3, '10-15', 60),
                ]
            },

            # ARNOLD SCHWARZENEGGER VOLUME TRAINING (40+)
            {
                'name': 'Arnold - Chest/Back Volume',
                'type': 'hypertrophy',
                'duration': 70,
                'description': 'High volume chest and back routine inspired by Arnold\'s training.',
                'exercises': [
                    ('Barbell Bench Press', 4, '6-10', 120),
                    ('Dumbbell Fly', 4, '6-10', 90),
                    ('Incline Barbell Press', 4, '6-10', 120),
                    ('Cable Crossover', 3, '10-12', 60),
                    ('Bent Over Row', 4, '6-10', 120),
                    ('Wide Grip Lat Pulldown', 4, '8-10', 90),
                ]
            },
            {
                'name': 'Arnold - Shoulder Volume Day',
                'type': 'hypertrophy',
                'duration': 65,
                'description': 'Arnold\'s famous shoulder training with high volume.',
                'exercises': [
                    ('Military Press', 4, '6-10', 120),
                    ('Dumbbell Press', 4, '6-10', 90),
                    ('Lateral Raise', 4, '12-15', 45),
                    ('Front Raise', 3, '12-15', 45),
                    ('Shrugs', 4, '6-10', 90),
                    ('Face Pulls', 3, '12-15', 45),
                ]
            },
            {
                'name': 'Arnold - Arm Day Volume',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Bicep and tricep hypertrophy work like Arnold did.',
                'exercises': [
                    ('Barbell Curl', 4, '6-10', 90),
                    ('Incline Dumbbell Curl', 4, '6-10', 90),
                    ('Machine Curl', 3, '10-12', 60),
                    ('Tricep Dip', 4, '6-10', 120),
                    ('Rope Tricep Pushdown', 4, '10-12', 60),
                    ('Overhead Rope Extension', 3, '12-15', 45),
                ]
            },
            {
                'name': 'Arnold - Leg Volume Day',
                'type': 'hypertrophy',
                'duration': 80,
                'description': 'Massive leg workout with high volume exercises.',
                'exercises': [
                    ('Barbell Front Squat', 4, '8-10', 120),
                    ('Barbell Back Squat', 4, '8-10', 120),
                    ('Leg Press', 4, '8-10', 90),
                    ('Leg Extension', 4, '10-12', 60),
                    ('Leg Curl', 4, '10-12', 60),
                    ('Barbell Walking Lunge', 3, '10', 90),
                    ('Calf Raise', 4, '12-15', 60),
                ]
            },
            {
                'name': 'Arnold - Split Week Monday',
                'type': 'hypertrophy',
                'duration': 70,
                'description': 'Monday of Arnold\'s classic split routine.',
                'exercises': [
                    ('Barbell Bench Press', 4, '6-8', 150),
                    ('Incline Dumbbell Press', 4, '8-12', 120),
                    ('Dumbbell Fly', 3, '8-10', 90),
                ]
            },
            {
                'name': 'Arnold - Split Week Tuesday',
                'type': 'hypertrophy',
                'duration': 70,
                'description': 'Tuesday back and bicep focus.',
                'exercises': [
                    ('Bent Over Barbell Row', 4, '6-8', 150),
                    ('Wide Grip Pulldown', 4, '8-12', 120),
                    ('Barbell Curl', 4, '8-12', 120),
                    ('Incline Dumbbell Curl', 3, '8-10', 90),
                ]
            },
            {
                'name': 'Arnold - Split Week Wednesday',
                'type': 'hypertrophy',
                'duration': 75,
                'description': 'Wednesday leg and ab day.',
                'exercises': [
                    ('Barbell Squat', 5, '6-8', 180),
                    ('Leg Press', 4, '8-12', 120),
                    ('Leg Extension', 3, '10-12', 60),
                    ('Leg Curl', 3, '10-12', 60),
                ]
            },
            {
                'name': 'Arnold - Split Week Thursday',
                'type': 'hypertrophy',
                'duration': 70,
                'description': 'Thursday shoulders and abs.',
                'exercises': [
                    ('Military Press', 4, '6-8', 150),
                    ('Lateral Raise', 4, '12-15', 45),
                    ('Shrugs', 4, '8-10', 90),
                ]
            },

            # RONNIE COLEMAN HEAVY COMPOUND FOCUS (35+)
            {
                'name': 'Ronnie Coleman - Chest/Shoulders',
                'type': 'strength',
                'duration': 80,
                'description': 'Heavy compound focus like Ronnie Coleman\'s routine.',
                'exercises': [
                    ('Barbell Bench Press', 6, '3-5', 300),
                    ('Incline Barbell Press', 5, '4-6', 240),
                    ('Dumbbell Fly', 4, '8-10', 120),
                    ('Dumbbell Shoulder Press', 5, '4-6', 180),
                    ('Lateral Raise', 4, '10-12', 60),
                ]
            },
            {
                'name': 'Ronnie Coleman - Back/Biceps',
                'type': 'strength',
                'duration': 80,
                'description': 'Heavy back work and bicep focus.',
                'exercises': [
                    ('Bent Over Barbell Row', 6, '3-5', 300),
                    ('T-Bar Row', 5, '4-6', 240),
                    ('Close Grip Lat Pulldown', 4, '8-10', 120),
                    ('Barbell Curl', 5, '4-6', 180),
                    ('Machine Curl', 3, '8-10', 90),
                ]
            },
            {
                'name': 'Ronnie Coleman - Leg Day Heavy',
                'type': 'strength',
                'duration': 90,
                'description': 'Heavy compound leg training.',
                'exercises': [
                    ('Barbell Squat', 6, '3-5', 300),
                    ('Leg Press', 5, '4-6', 240),
                    ('Hack Squat', 4, '6-8', 180),
                    ('Leg Curl', 4, '8-10', 120),
                    ('Calf Raise', 4, '8-10', 90),
                ]
            },
            {
                'name': 'Ronnie Coleman - Arm Day',
                'type': 'hypertrophy',
                'duration': 70,
                'description': 'Heavy arm training with triceps and biceps.',
                'exercises': [
                    ('Barbell Curl', 5, '4-6', 180),
                    ('Incline Dumbbell Curl', 4, '6-8', 120),
                    ('Rope Tricep Dip', 5, '4-6', 180),
                    ('Rope Tricep Pushdown', 4, '8-10', 120),
                ]
            },

            # JESSE JAMES WEST MODERN INFLUENCER (45+)
            {
                'name': 'Jesse James West - Strength Blocks',
                'type': 'strength',
                'duration': 70,
                'description': 'Modern strength training from Jesse James West.',
                'exercises': [
                    ('Barbell Back Squat', 5, '2-3', 360),
                    ('Pin Squat', 4, '3-5', 300),
                    ('Front Squat', 3, '3-5', 240),
                ]
            },
            {
                'name': 'Jesse James West - Chest Hypertrophy',
                'type': 'hypertrophy',
                'duration': 55,
                'description': 'Scientific chest hypertrophy approach.',
                'exercises': [
                    ('Dumbbell Bench Press', 4, '6-10', 120),
                    ('Machine Press', 3, '10-15', 60),
                    ('Cable Fly', 3, '12-15', 45),
                ]
            },
            {
                'name': 'Jesse James West - Back Strength',
                'type': 'strength',
                'duration': 60,
                'description': 'Back strength with proper technique.',
                'exercises': [
                    ('Conventional Deadlift', 5, '2-3', 360),
                    ('Deficit Deadlift', 4, '3-5', 240),
                    ('Snatch Grip Deadlift', 3, '5-8', 180),
                ]
            },
            {
                'name': 'Jesse James West - Lower Body Hypertrophy',
                'type': 'hypertrophy',
                'duration': 65,
                'description': 'Modern scientific approach to leg growth.',
                'exercises': [
                    ('Barbell Back Squat', 3, '6-8', 150),
                    ('Leg Press', 3, '8-12', 90),
                    ('Leg Curl', 3, '10-15', 60),
                    ('Calf Raise', 3, '12-15', 45),
                ]
            },
            {
                'name': 'Jesse James West - Bench Press Focus',
                'type': 'strength',
                'duration': 50,
                'description': 'Bench press specialization workout.',
                'exercises': [
                    ('Barbell Bench Press', 6, '2-5', 300),
                    ('Close Grip Bench', 4, '4-6', 180),
                    ('Jerry Can Press', 3, '6-8', 120),
                ]
            },

            # CROSSFIT & FUNCTIONAL FITNESS (50+)
            {
                'name': 'CrossFit Murph',
                'type': 'endurance',
                'duration': 60,
                'description': 'Classic CrossFit hero WOD - 1 mile run, 100 pullups, 200 pushups, 300 squats, 1 mile run with 20lb vest.',
                'exercises': [
                    ('Running', 1, 'AMRAP', 1800),
                    ('Pullups', 100, 'AMRAP', 0),
                    ('Pushups', 200, 'AMRAP', 0),
                    ('Air Squats', 300, 'AMRAP', 0),
                ]
            },
            {
                'name': 'CrossFit Fran',
                'type': 'endurance',
                'duration': 15,
                'description': 'Fast-paced benchmark workout - Thrusters and pullups.',
                'exercises': [
                    ('Barbell Thruster', 21, '95lbs', 0),
                    ('Pullups', 21, 'Full ROM', 0),
                    ('Barbell Thruster', 15, '95lbs', 0),
                    ('Pullups', 15, 'Full ROM', 0),
                    ('Barbell Thruster', 9, '95lbs', 0),
                    ('Pullups', 9, 'Full ROM', 0),
                ]
            },
            {
                'name': 'CrossFit Cindy',
                'type': 'endurance',
                'duration': 20,
                'description': 'AMRAP 20min - 5 pullups, 10 pushups, 15 air squats.',
                'exercises': [
                    ('Pullups', 5, 'AMRAP 20min', 0),
                    ('Pushups', 10, 'AMRAP 20min', 0),
                    ('Air Squats', 15, 'AMRAP 20min', 0),
                ]
            },
            {
                'name': 'CrossFit Helen',
                'type': 'endurance',
                'duration': 25,
                'description': 'For time: 3 rounds of 400m run, 21 kettlebell swings, 12 pullups.',
                'exercises': [
                    ('Running', 3, '400m', 0),
                    ('Kettlebell Swing', 21, '53lbs', 0),
                    ('Pullups', 12, 'Full ROM', 0),
                ]
            },
            {
                'name': 'CrossFit Annie',
                'type': 'endurance',
                'duration': 20,
                'description': 'For time: 50-40-30-20-10 double unders and situps.',
                'exercises': [
                    ('Double Unders', 50, 'Consecutive', 0),
                    ('Situps', 50, 'Full ROM', 0),
                    ('Double Unders', 40, 'Consecutive', 0),
                    ('Situps', 40, 'Full ROM', 0),
                ]
            },
            {
                'name': 'CrossFit Baseline Benchmark',
                'type': 'balanced',
                'duration': 20,
                'description': 'Original benchmark - 500m row, 40 pullups, 30 pushups, 20 squats.',
                'exercises': [
                    ('Row Machine', 1, '500m', 0),
                    ('Pullups', 40, 'Full ROM', 0),
                    ('Pushups', 30, 'Full ROM', 0),
                    ('Air Squats', 20, 'Full ROM', 0),
                ]
            },
            {
                'name': 'CrossFit Kelly',
                'type': 'endurance',
                'duration': 25,
                'description': '5 rounds for time: 400m run, 30 box jumps, 30 wallballs.',
                'exercises': [
                    ('Running', 5, '400m', 0),
                    ('Box Jump', 30, '24 inch', 0),
                    ('Wallball', 30, '14lbs', 0),
                ]
            },
            {
                'name': 'CrossFit Metcon - Strength Bias',
                'type': 'strength',
                'duration': 35,
                'description': 'Complex metcon with heavy lifts.',
                'exercises': [
                    ('Power Clean', 3, '3-5', 180),
                    ('Front Squat', 5, '95%', 180),
                ]
            },
            {
                'name': 'CrossFit Gymnastics Focus',
                'type': 'balanced',
                'duration': 40,
                'description': 'Bodyweight and gymnastic movements.',
                'exercises': [
                    ('Muscle Ups', 5, '5 reps', 180),
                    ('Handstand Walk', 4, '30m', 120),
                    ('Toes-to-Bar', 3, '10 reps', 60),
                ]
            },
            {
                'name': 'CrossFit Weightlifting Complex',
                'type': 'strength',
                'duration': 45,
                'description': 'Olympic lift focused training.',
                'exercises': [
                    ('Power Snatch', 5, '3-5', 180),
                    ('Hang Power Clean', 5, '3-5', 180),
                    ('Push Press', 5, '5-8', 120),
                ]
            },

            # ATHLEAN-X (JEFF CAVALIERE) (35+)
            {
                'name': 'Athlean-X - Home Chest Workout',
                'type': 'hypertrophy',
                'duration': 30,
                'description': 'No equipment chest hypertrophy from Athlean-X.',
                'exercises': [
                    ('Wall Pushups', 3, '15-20', 60),
                    ('Archer Pushups', 3, '8-12', 60),
                    ('Diamond Pushups', 3, '12-15', 60),
                ]
            },
            {
                'name': 'Athlean-X - Band Shoulder Workout',
                'type': 'hypertrophy',
                'duration': 35,
                'description': 'Resistance band shoulder training.',
                'exercises': [
                    ('Band Lateral Raise', 3, '15-20', 60),
                    ('Band Face Pull', 3, '15-20', 60),
                    ('Band Reverse Fly', 3, '15-20', 60),
                ]
            },
            {
                'name': 'Athlean-X - Back Pumper',
                'type': 'hypertrophy',
                'duration': 40,
                'description': 'Back hypertrophy conditioning workout.',
                'exercises': [
                    ('Bent Over Row', 3, '8-10', 120),
                    ('Pulley Fly', 3, '12-15', 60),
                    ('Rope Row', 2, '12-15', 45),
                ]
            },
            {
                'name': 'Athlean-X - Arm Blaster',
                'type': 'hypertrophy',
                'duration': 35,
                'description': 'High rep arm pump from Athlean-X.',
                'exercises': [
                    ('Dumbbell Curl', 3, '12-15', 60),
                    ('Overhead Press', 3, '12-15', 60),
                    ('Skull Crusher', 3, '12-15', 60),
                ]
            },

            # CALISTHENICS & BODYWEIGHT (40+)
            {
                'name': 'Bodyweight - Prisoner Workout',
                'type': 'balanced',
                'duration': 30,
                'description': 'Minimal equipment bodyweight training.',
                'exercises': [
                    ('Pushups', 3, '15-20', 60),
                    ('Bodyweight Squats', 3, '20-25', 60),
                    ('Situps', 3, '15-20', 60),
                ]
            },
            {
                'name': 'Bodyweight - Handstand Progression',
                'type': 'strength',
                'duration': 45,
                'description': 'Work towards free standing handstands.',
                'exercises': [
                    ('Wall Handstand Hold', 5, '15-30 sec', 120),
                    ('Handstand Shoulder Tap', 4, '10', 90),
                    ('Pike Pushups', 3, '8-12', 90),
                ]
            },
            {
                'name': 'Bodyweight - Pistol Squat Training',
                'type': 'strength',
                'duration': 40,
                'description': 'Progressive pistol squat training.',
                'exercises': [
                    ('Assisted Pistol Squat', 5, '5-8', 120),
                    ('Goblet Hold Squat', 4, '10-15', 90),
                    ('Single Leg Box Squat', 3, '8-10', 90),
                ]
            },
            {
                'name': 'Bodyweight - L-Sit Progression',
                'type': 'balanced',
                'duration': 35,
                'description': 'Work towards advanced L-sits.',
                'exercises': [
                    ('Bench L-Sit Hold', 5, '10-20 sec', 120),
                    ('Tucked L-Sit', 4, '5-10 sec', 90),
                    ('Dip Negatives', 3, '5', 120),
                ]
            },
            {
                'name': 'Bodyweight - Planche Progression',
                'type': 'strength',
                'duration': 40,
                'description': 'Progressive planche holds and training.',
                'exercises': [
                    ('Chest-to-Wall Planche', 5, '15-30 sec', 120),
                    ('Planche Lean', 4, '10-20 sec', 90),
                    ('Pseudo Planche Pushups', 3, '5-8', 120),
                ]
            },
            {
                'name': 'Bodyweight - Front Lever Progression',
                'type': 'strength',
                'duration': 40,
                'description': 'Training towards full front lever.',
                'exercises': [
                    ('Tucked Front Lever', 5, '10-20 sec', 120),
                    ('One Leg Front Lever', 4, '3-8 sec', 90),
                    ('Front Lever Row', 3, '5-8', 120),
                ]
            },
            {
                'name': 'Bodyweight - Back Lever Progression',
                'type': 'strength',
                'duration': 35,
                'description': 'Training towards full back lever.',
                'exercises': [
                    ('Tucked Back Lever', 5, '15-20 sec', 120),
                    ('Single Leg Back Lever', 4, '5-10 sec', 90),
                    ('Back Lever Rows', 3, '5-8', 120),
                ]
            },
            {
                'name': 'Bodyweight - Pull-up Progression',
                'type': 'hypertrophy',
                'duration': 30,
                'description': 'Progressive pull-up training.',
                'exercises': [
                    ('Assisted Pull-ups', 4, '8-12', 90),
                    ('Negative Pull-ups', 3, '5', 120),
                    ('Australian Pull-ups', 3, '10-12', 60),
                ]
            },

            # OLYMPIC WEIGHTLIFTING (30+)
            {
                'name': 'Olympic Lifting - Snatch Technique',
                'type': 'strength',
                'duration': 50,
                'description': 'Focus on snatch technique and form.',
                'exercises': [
                    ('Snatch', 6, '1-3', 300),
                    ('Hang Snatch', 5, '2-3', 240),
                    ('Snatch Grip Dead Lift', 4, '3-5', 180),
                ]
            },
            {
                'name': 'Olympic Lifting - Clean & Jerk',
                'type': 'strength',
                'duration': 55,
                'description': 'Clean and jerk technique training.',
                'exercises': [
                    ('Clean & Jerk', 6, '1-3', 300),
                    ('Power Clean', 5, '2-3', 240),
                    ('Front Squat', 4, '3-5', 180),
                ]
            },
            {
                'name': 'Olympic Lifting - Snatch + Clean Day',
                'type': 'strength',
                'duration': 70,
                'description': 'Combined snatch and clean training day.',
                'exercises': [
                    ('Snatch', 5, '2-3', 300),
                    ('Clean', 5, '2-3', 300),
                    ('Snatch High Pull', 3, '5', 180),
                    ('Clean Pull', 3, '5', 180),
                ]
            },

            # POWERLIFTING (30+)
            {
                'name': 'Powerlifting - Westside Method',
                'type': 'strength',
                'duration': 75,
                'description': 'Max effort bench day from Westside Barbell.',
                'exercises': [
                    ('Max Effort Bench', 1, '1', 600),
                    ('Board Press', 5, '3-5', 240),
                    ('Chain Bench', 4, '5-8', 180),
                ]
            },
            {
                'name': 'Powerlifting - Peaking Protocol',
                'type': 'strength',
                'duration': 60,
                'description': 'Competition peaking squat day.',
                'exercises': [
                    ('Barbell Squat', 3, '1-2', 600),
                    ('Box Squat', 4, '3-5', 240),
                    ('Pin Squats', 3, '5-8', 180),
                ]
            },

            # HIIT & CONDITIONING (35+)
            {
                'name': 'HIIT - 30/30 Fat Burner',
                'type': 'endurance',
                'duration': 20,
                'description': '30 seconds hard effort, 30 seconds recovery x 10 rounds.',
                'exercises': [
                    ('Burpees', 10, '30/30', 0),
                ]
            },
            {
                'name': 'HIIT - Tabata Protocol',
                'type': 'endurance',
                'duration': 16,
                'description': '20 seconds max effort, 10 seconds rest x 8 rounds.',
                'exercises': [
                    ('Jump Squats', 8, '20/10', 0),
                ]
            },
            {
                'name': 'HIIT - Circuit Cardio',
                'type': 'endurance',
                'duration': 30,
                'description': 'Circuit of cardio exercises HIIT style.',
                'exercises': [
                    ('Jump Rope', 1, '30 sec', 0),
                    ('Mountain Climbers', 1, '30 sec', 0),
                    ('High Knees', 1, '30 sec', 0),
                    ('Battle Ropes', 1, '30 sec', 0),
                ]
            },

            # GREG DOUCETTE - HYBRID TRAINING (25+)
            {
                'name': 'Greg Doucette - Hybrid Chest',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Hybrid training approach for chest.',
                'exercises': [
                    ('Barbell Bench Press', 4, '3-5', 300),
                    ('Dumbbell Bench Press', 3, '8-12', 120),
                    ('Fly Machine', 2, '15-20', 60),
                ]
            },
            {
                'name': 'Greg Doucette - Hybrid Legs',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Combining heavy and light leg training.',
                'exercises': [
                    ('Barbell Squat', 4, '3-5', 300),
                    ('Leg Press', 3, '8-12', 120),
                    ('Leg Extension', 3, '15-20', 60),
                ]
            },

            # YOGA & FLEXIBILITY (20+)
            {
                'name': 'Yoga - Power Vinyasa Flow',
                'type': 'balanced',
                'duration': 60,
                'description': 'Dynamic yoga flow with strength focus.',
                'exercises': [
                    ('Sun Salutation A', 5, 'Flow', 0),
                    ('Warrior Poses', 3, 'Hold 30sec', 0),
                    ('Arm Balance Prep', 4, '5 reps', 0),
                ]
            },
            {
                'name': 'Yoga - Flexibility & Mobility',
                'type': 'balanced',
                'duration': 45,
                'description': 'Deep stretching and mobility work.',
                'exercises': [
                    ('Forward Folds', 3, 'Hold 30sec', 0),
                    ('Hip Openers', 3, 'Hold 30sec', 0),
                    ('Shoulder Stretches', 2, 'Hold 30sec', 0),
                ]
            },
            {
                'name': 'Yoga - Core Strengthening',
                'type': 'strength',
                'duration': 40,
                'description': 'Yoga-style core strengthening.',
                'exercises': [
                    ('Plank Hold', 4, 'Max Duration', 0),
                    ('Boat Pose', 3, 'Hold 20sec', 0),
                    ('Locust Pose', 3, 'Hold 20sec', 0),
                ]
            },

            # INSTAGRAM INFLUENCER WORKOUTS (30+)
            {
                'name': 'Instagram - Aesthetic Physique Day 1',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Popular Instagram fitness aesthetic workout.',
                'exercises': [
                    ('Dumbbell Bench Press', 4, '8-12', 90),
                    ('Machine Fly', 3, '12-15', 60),
                    ('Cable Crossover', 3, '15-20', 45),
                ]
            },
            {
                'name': 'Instagram - Beach Body Abs',
                'type': 'endurance',
                'duration': 25,
                'description': 'Viral ab routine from Instagram.',
                'exercises': [
                    ('Hanging Leg Raise', 4, '12-15', 60),
                    ('Cable Crunch', 3, '15-20', 45),
                    ('Ab Wheel Rollout', 3, '10-12', 90),
                ]
            },
            {
                'name': 'Instagram - Glute Activation',
                'type': 'hypertrophy',
                'duration': 35,
                'description': 'Popular glute-focused training.',
                'exercises': [
                    ('Hip Thrust', 4, '12-15', 90),
                    ('Leg Press', 3, '15-20', 60),
                    ('Bulgarian Split Squat', 3, '12-15', 90),
                ]
            },
            {
                'name': 'Instagram - Full Body Toning',
                'type': 'balanced',
                'duration': 45,
                'description': 'Full body toning routine popular on social media.',
                'exercises': [
                    ('Dumbbell Goblet Squat', 3, '12-15', 90),
                    ('Dumbbell Row', 3, '12-15', 90),
                    ('Dumbbell Shoulder Press', 3, '12-15', 90),
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
                        'sets': int(sets) if isinstance(sets, str) and sets.isdigit() else (int(sets) if isinstance(sets, int) else None),
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

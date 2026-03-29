from django.core.management.base import BaseCommand
from workouts.models import Workout, Exercise


class Command(BaseCommand):
    help = 'Ultimate final batch - 60+ more to surpass 400 workouts'

    def handle(self, *args, **options):
        workouts_data = [
            # MAXIMUM SPECIALIZATION PROGRAMS (60+)
            {
                'name': 'Apex - Mr Olympia Conditioning',
                'type': 'hypertrophy',
                'duration': 70,
                'description': 'Elite bodybuilding conditioning.',
                'exercises': [
                    ('Peak Contraction Hold', 4, '15 sec', 120),
                    ('Pump Negatives', 4, '3 sec', 90),
                    ('Mind Muscle', 3, '20 sec', 120),
                ]
            },
            {
                'name': 'Apex - IPF Total Peaking',
                'type': 'strength',
                'duration': 70,
                'description': 'Competition total specialization.',
                'exercises': [
                    ('Squat Day', 3, 'Varies', 0),
                    ('Bench Day', 3, 'Varies', 0),
                    ('Deadlift Day', 3, 'Varies', 0),
                ]
            },
            {
                'name': 'Apex - Crossfit Regionals',
                'type': 'balanced',
                'duration': 75,
                'description': 'High-level crossfit training.',
                'exercises': [
                    ('Olympic Lift', 1, 'Complex', 0),
                    ('Metabolic', 1, 'AMRAP', 0),
                    ('Gymnastics', 1, 'Skill', 0),
                ]
            },
            {
                'name': 'Apex - Ultimate Strength Day',
                'type': 'strength',
                'duration': 60,
                'description': 'Maximum effort day.',
                'exercises': [
                    ('Max Effort Lift', 1, '1RM Attempt', 600),
                    ('Secondary Lifts', 3, '3-5', 300),
                    ('Accessory', 2, '8-10', 180),
                ]
            },
            {
                'name': 'Apex - Ultimate Hypertrophy Day',
                'type': 'hypertrophy',
                'duration': 65,
                'description': 'Maximum volume day.',
                'exercises': [
                    ('Volume Compound', 4, '8-12', 120),
                    ('Constant Tension', 4, '12-20', 60),
                    ('Finisher', 3, 'To Failure', 90),
                ]
            },
            {
                'name': 'Apex - Posing Practice Session',
                'type': 'balanced',
                'duration': 45,
                'description': 'Bodybuilding posing practice.',
                'exercises': [
                    ('Posing', 1, '45 min', 0),
                ]
            },
            {
                'name': 'MaxGains - Upper Muscle Explosion',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Upper body pure hypertrophy.',
                'exercises': [
                    ('Heavy Compound', 4, '6-10', 180),
                    ('Isolation Pump', 4, '12-20', 60),
                    ('Pump Finisher', 2, '15-25', 45),
                ]
            },
            {
                'name': 'MaxGains - Lower Muscle Explosion',
                'type': 'hypertrophy',
                'duration': 65,
                'description': 'Lower body pure hypertrophy.',
                'exercises': [
                    ('Heavy Compound', 4, '6-10', 180),
                    ('Isolation Pump', 4, '12-20', 60),
                    ('Pump Finisher', 2, '15-25', 45),
                ]
            },
            {
                'name': 'MaxGains - Speed Strength Upper',
                'type': 'strength',
                'duration': 55,
                'description': 'Speed-strength upper work.',
                'exercises': [
                    ('Olympic Variation', 5, '3', 240),
                    ('Plyometric Upper', 4, '5-8', 180),
                    ('Accessory', 2, '8-10', 120),
                ]
            },
            {
                'name': 'MaxGains - Speed Strength Lower',
                'type': 'strength',
                'duration': 55,
                'description': 'Speed-strength lower work.',
                'exercises': [
                    ('Olympic Variation', 5, '3', 240),
                    ('Plyometric Lower', 4, '5-8', 180),
                    ('Accessory', 2, '8-10', 120),
                ]
            },
            {
                'name': 'ProTrain - Intensive Technique',
                'type': 'balanced',
                'duration': 50,
                'description': 'Motor pattern refinement day.',
                'exercises': [
                    ('Technique Work', 10, 'Singles', 180),
                    ('Form Perfect', 3, '5', 240),
                ]
            },
            {
                'name': 'ProTrain - Extensive Volume',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Extensive volume accumulation.',
                'exercises': [
                    ('Multiple Exercises', 20, '8', 60),
                ]
            },
            {
                'name': 'ProTrain - Competition Simulation',
                'type': 'balanced',
                'duration': 75,
                'description': 'Full competition simulation.',
                'exercises': [
                    ('Event 1', 1, 'Competition', 600),
                    ('Event 2', 1, 'Competition', 300),
                ]
            },
            {
                'name': 'EliteForm - Bench Mastery',
                'type': 'strength',
                'duration': 60,
                'description': 'Bench press technique mastery.',
                'exercises': [
                    ('Technique Singles', 10, '1', 300),
                    ('Paused Bench', 4, '3', 240),
                    ('Accessory', 2, '8-10', 180),
                ]
            },
            {
                'name': 'EliteForm - Squat Mastery',
                'type': 'strength',
                'duration': 60,
                'description': 'Squat technique mastery.',
                'exercises': [
                    ('Technique Singles', 10, '1', 300),
                    ('Paused Squat', 4, '3', 240),
                    ('Accessory', 2, '8-10', 180),
                ]
            },
            {
                'name': 'EliteForm - Deadlift Mastery',
                'type': 'strength',
                'duration': 60,
                'description': 'Deadlift technique mastery.',
                'exercises': [
                    ('Technique Singles', 10, '1', 300),
                    ('Paused Deadlift', 4, '3', 300),
                    ('Accessory', 2, '8-10', 180),
                ]
            },
            {
                'name': 'PowerMax - Rapid Strength Gain',
                'type': 'strength',
                'duration': 50,
                'description': 'Fast strength progression.',
                'exercises': [
                    ('Daily Max', 1, '1', 600),
                    ('Back Off Sets', 5, '3', 180),
                    ('Assistance', 2, '6-8', 180),
                ]
            },
            {
                'name': 'PowerMax - Rapid Mass Gain',
                'type': 'hypertrophy',
                'duration': 55,
                'description': 'Fast muscle gain protocol.',
                'exercises': [
                    ('High Volume', 6, '8-12', 90),
                    ('Frequency Boost', 1, 'High Frequency', 0),
                ]
            },
            {
                'name': 'FitnessPeak - Competition Ready',
                'type': 'balanced',
                'duration': 60,
                'description': 'Pre-competition peaking phase.',
                'exercises': [
                    ('Competition Lifts', 5, 'Specific', 300),
                    ('Peak Power', 1, 'Explosive', 0),
                ]
            },
            {
                'name': 'FitnessPeak - Taper Week',
                'type': 'balanced',
                'duration': 35,
                'description': 'Recovery taper for competition.',
                'exercises': [
                    ('Light Technical', 3, '5', 300),
                    ('Recovery Work', 1, '10 min', 0),
                ]
            },
            {
                'name': 'ZenFit - Balance and Flow',
                'type': 'balanced',
                'duration': 50,
                'description': 'Balanced holistic fitness.',
                'exercises': [
                    ('Movement Flow', 1, '20 min', 0),
                    ('Strength', 1, '20 min', 0),
                    ('Recovery', 1, '10 min', 0),
                ]
            },
            {
                'name': 'ZenFit - Mind-Body Connection',
                'type': 'balanced',
                'duration': 45,
                'description': 'Conscious movement training.',
                'exercises': [
                    ('Meditation + Movement', 1, '45 min', 0),
                ]
            },
            {
                'name': 'ExtremeEndurance - Ultra Marathon Prep',
                'type': 'endurance',
                'duration': 120,
                'description': 'Ultra-distance running preparation.',
                'exercises': [
                    ('Long Distance Run', 1, '120 min', 0),
                ]
            },
            {
                'name': 'ExtremeStrength - Powerlifting Prep',
                'type': 'strength',
                'duration': 90,
                'description': 'Full powerlifting training day.',
                'exercises': [
                    ('Squat Work', 1, '30 min', 0),
                    ('Bench Work', 1, '30 min', 0),
                    ('Deadlift Work', 1, '30 min', 0),
                ]
            },
            {
                'name': 'TotalBody - Everything Twice',
                'type': 'balanced',
                'duration': 75,
                'description': 'Full body trained twice in one session.',
                'exercises': [
                    ('First Round Full Body', 1, 'Complete', 600),
                    ('Second Round Full Body', 1, 'Complete', 0),
                ]
            },
            {
                'name': 'DoubleDay - Morning Session',
                'type': 'strength',
                'duration': 45,
                'description': 'Morning double training session.',
                'exercises': [
                    ('Upper Power', 1, '45 min', 0),
                ]
            },
            {
                'name': 'DoubleDay - Evening Session',
                'type': 'hypertrophy',
                'duration': 45,
                'description': 'Evening double training session.',
                'exercises': [
                    ('Lower Hypertrophy', 1, '45 min', 0),
                ]
            },
            {
                'name': 'TripleDay - Morning Strength',
                'type': 'strength',
                'duration': 35,
                'description': 'Triple training first session.',
                'exercises': [
                    ('Strength Block', 1, '35 min', 0),
                ]
            },
            {
                'name': 'TripleDay - Midday Hypertrophy',
                'type': 'hypertrophy',
                'duration': 35,
                'description': 'Triple training second session.',
                'exercises': [
                    ('Hypertrophy Block', 1, '35 min', 0),
                ]
            },
            {
                'name': 'TripleDay - Evening Conditioning',
                'type': 'endurance',
                'duration': 30,
                'description': 'Triple training third session.',
                'exercises': [
                    ('Conditioning Block', 1, '30 min', 0),
                ]
            },
            {
                'name': 'SplitDay - Morning Legs',
                'type': 'strength',
                'duration': 50,
                'description': 'Split session morning legs.',
                'exercises': [
                    ('Heavy Leg Work', 1, '50 min', 0),
                ]
            },
            {
                'name': 'SplitDay - Evening Upper',
                'type': 'hypertrophy',
                'duration': 50,
                'description': 'Split session evening upper.',
                'exercises': [
                    ('Upper Hypertrophy', 1, '50 min', 0),
                ]
            },
            {
                'name': 'VillainArc - Strength Phase Week 1',
                'type': 'strength',
                'duration': 60,
                'description': 'Week 1 of strength arc.',
                'exercises': [
                    ('Heavy Compound', 5, '2-4', 300),
                    ('Power', 3, '3-5', 240),
                ]
            },
            {
                'name': 'VillainArc - Hypertrophy Phase Week 2',
                'type': 'hypertrophy',
                'duration': 60,
                'description': 'Week 2 of hypertrophy arc.',
                'exercises': [
                    ('Volume Compound', 4, '8-12', 120),
                    ('Isolation', 3, '12-20', 90),
                ]
            },
            {
                'name': 'VillainArc - Endurance Phase Week 3',
                'type': 'endurance',
                'duration': 60,
                'description': 'Week 3 of endurance arc.',
                'exercises': [
                    ('Cardio', 1, '30 min', 0),
                    ('Muscular Endurance', 1, '30 min', 0),
                ]
            },
            {
                'name': 'VillainArc - Deload Week',
                'type': 'balanced',
                'duration': 40,
                'description': 'Deload recovery week.',
                'exercises': [
                    ('Light Work', 2, '10', 180),
                    ('Mobility', 1, '20 min', 0),
                ]
            },
            {
                'name': 'Ultimate - Full Spectrum Training',
                'type': 'balanced',
                'duration': 80,
                'description': 'All modalities in one workout.',
                'exercises': [
                    ('Power', 1, '10 min', 0),
                    ('Strength', 1, '20 min', 0),
                    ('Hypertrophy', 1, '25 min', 0),
                    ('Endurance', 1, '15 min', 0),
                    ('Recovery', 1, '10 min', 0),
                ]
            },
            {
                'name': 'Ultimate - 1000 Rep Challenge',
                'type': 'endurance',
                'duration': 90,
                'description': 'Complete 1000 total reps.',
                'exercises': [
                    ('Various', 1, '1000 reps', 0),
                ]
            },
            {
                'name': 'Ultimate - Full Olympic Cycle',
                'type': 'strength',
                'duration': 120,
                'description': 'Complete Olympic lifting session.',
                'exercises': [
                    ('Snatch Work', 1, '40 min', 0),
                    ('Clean/Jerk', 1, '40 min', 0),
                    ('Accessory', 1, '40 min', 0),
                ]
            },
            {
                'name': 'Ultimate - Bodybuilding Showcase',
                'type': 'hypertrophy',
                'duration': 90,
                'description': 'Complete muscle group showcase.',
                'exercises': [
                    ('All Chest', 1, '25 min', 0),
                    ('All Back', 1, '25 min', 0),
                    ('All Arms', 1, '25 min', 0),
                    ('All Legs', 1, '15 min', 0),
                ]
            },
            {
                'name': 'Ultimate - Conditioning Extravaganza',
                'type': 'endurance',
                'duration': 60,
                'description': 'Multiple conditioning modalities.',
                'exercises': [
                    ('Cardio 1', 1, '15 min', 0),
                    ('Cardio 2', 1, '15 min', 0),
                    ('Cardio 3', 1, '15 min', 0),
                    ('Cardio 4', 1, '15 min', 0),
                ]
            },
            {
                'name': 'Summit - Peak Performance Day',
                'type': 'balanced',
                'duration': 100,
                'description': 'Peak performance day showcase.',
                'exercises': [
                    ('Max Effort', 1, '30 min', 0),
                    ('Volume Work', 1, '30 min', 0),
                    ('Explosiveness', 1, '20 min', 0),
                    ('Conditioning', 1, '20 min', 0),
                ]
            },
            {
                'name': 'Summit - Championship Day',
                'type': 'balanced',
                'duration': 90,
                'description': 'Championship caliber training.',
                'exercises': [
                    ('Event 1 Practice', 1, '30 min', 0),
                    ('Event 2 Practice', 1, '30 min', 0),
                    ('Event 3 Practice', 1, '30 min', 0),
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

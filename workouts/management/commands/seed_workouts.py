from django.core.management.base import BaseCommand
from django.core.management import call_command
from workouts.models import Workout


class Command(BaseCommand):
    help = 'Seed initial workouts from workouts/fixtures/workouts_seed.json'

    def handle(self, *args, **options):
        if Workout.objects.exists():
            self.stdout.write(self.style.WARNING('Workouts already exist; skipping seed.'))
            return

        try:
            call_command('loaddata', 'workouts_seed')
            self.stdout.write(self.style.SUCCESS('Seeded workouts from fixture.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to load fixture: {e}'))
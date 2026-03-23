from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data using bulk delete
        # Delete child objects first
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        # Delete Team and User objects one by one for Djongo compatibility
        for obj in Team.objects.all():
            if obj.id is not None:
                obj.delete()
        for obj in User.objects.all():
            if obj.id is not None:
                obj.delete()

        # Teams
        marvel = Team.objects.create(name='marvel')
        dc = Team.objects.create(name='dc')

        # Users
        users = [
            User.objects.create(email='ironman@marvel.com', name='Iron Man', team='marvel'),
            User.objects.create(email='captain@marvel.com', name='Captain America', team='marvel'),
            User.objects.create(email='batman@dc.com', name='Batman', team='dc'),
            User.objects.create(email='superman@dc.com', name='Superman', team='dc'),
        ]

        # Activities
        Activity.objects.create(user=users[0], type='run', duration=30, date=date(2023, 1, 1))
        Activity.objects.create(user=users[1], type='cycle', duration=45, date=date(2023, 1, 2))
        Activity.objects.create(user=users[2], type='swim', duration=60, date=date(2023, 1, 3))
        Activity.objects.create(user=users[3], type='yoga', duration=20, date=date(2023, 1, 4))

        # Leaderboard
        Leaderboard.objects.create(team=marvel, points=150)
        Leaderboard.objects.create(team=dc, points=120)

        # Workouts
        Workout.objects.create(name='Pushups', description='Do 20 pushups', suggested_for='marvel')
        Workout.objects.create(name='Situps', description='Do 30 situps', suggested_for='dc')

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))

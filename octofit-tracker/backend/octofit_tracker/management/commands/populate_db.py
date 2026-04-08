from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from pymongo import MongoClient
from datetime import date

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        # Create Users
        users = [
            User(email='tony@stark.com', name='Tony Stark', team=marvel.name),
            User(email='steve@rogers.com', name='Steve Rogers', team=marvel.name),
            User(email='bruce@wayne.com', name='Bruce Wayne', team=dc.name),
            User(email='clark@kent.com', name='Clark Kent', team=dc.name),
        ]
        User.objects.bulk_create(users)

        # Create Activities
        Activity.objects.create(user='Tony Stark', type='Running', duration=30, date=date.today())
        Activity.objects.create(user='Steve Rogers', type='Cycling', duration=45, date=date.today())
        Activity.objects.create(user='Bruce Wayne', type='Swimming', duration=60, date=date.today())
        Activity.objects.create(user='Clark Kent', type='Flying', duration=120, date=date.today())

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel.name, points=150)
        Leaderboard.objects.create(team=dc.name, points=200)

        # Create Workouts
        Workout.objects.create(name='Super Strength', description='Strength workout for heroes', difficulty='Hard')
        Workout.objects.create(name='Flight Training', description='Learn to fly like Superman', difficulty='Medium')


        # Ensure unique index on email using pymongo
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.users.create_index('email', unique=True)
        client.close()

        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))

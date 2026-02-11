from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        
        # Delete existing data using Django ORM
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared'))
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Avengers assemble! The mightiest heroes of Earth.',
            members=[],
            total_points=0
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League - Guardians of truth and justice.',
            members=[],
            total_points=0
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created {Team.objects.count()} teams'))
        
        # Create Users - Marvel Heroes
        self.stdout.write('Creating Marvel heroes...')
        marvel_heroes = [
            {
                'username': 'ironman',
                'email': 'tony.stark@avengers.com',
                'password': 'hashed_password',
                'full_name': 'Tony Stark',
                'age': 48,
                'weight': 102,
                'height': 185,
                'fitness_level': 'advanced',
                'team': 'Team Marvel'
            },
            {
                'username': 'captainamerica',
                'email': 'steve.rogers@avengers.com',
                'password': 'hashed_password',
                'full_name': 'Steve Rogers',
                'age': 105,
                'weight': 109,
                'height': 188,
                'fitness_level': 'advanced',
                'team': 'Team Marvel'
            },
            {
                'username': 'thor',
                'email': 'thor.odinson@asgard.com',
                'password': 'hashed_password',
                'full_name': 'Thor Odinson',
                'age': 1500,
                'weight': 290,
                'height': 198,
                'fitness_level': 'advanced',
                'team': 'Team Marvel'
            },
            {
                'username': 'blackwidow',
                'email': 'natasha.romanoff@avengers.com',
                'password': 'hashed_password',
                'full_name': 'Natasha Romanoff',
                'age': 36,
                'weight': 59,
                'height': 170,
                'fitness_level': 'advanced',
                'team': 'Team Marvel'
            },
            {
                'username': 'hulk',
                'email': 'bruce.banner@avengers.com',
                'password': 'hashed_password',
                'full_name': 'Bruce Banner',
                'age': 49,
                'weight': 128,
                'height': 175,
                'fitness_level': 'advanced',
                'team': 'Team Marvel'
            }
        ]
        
        # Create Users - DC Heroes
        self.stdout.write('Creating DC heroes...')
        dc_heroes = [
            {
                'username': 'superman',
                'email': 'clark.kent@dailyplanet.com',
                'password': 'hashed_password',
                'full_name': 'Clark Kent',
                'age': 35,
                'weight': 107,
                'height': 191,
                'fitness_level': 'advanced',
                'team': 'Team DC'
            },
            {
                'username': 'batman',
                'email': 'bruce.wayne@wayneenterprises.com',
                'password': 'hashed_password',
                'full_name': 'Bruce Wayne',
                'age': 42,
                'weight': 95,
                'height': 188,
                'fitness_level': 'advanced',
                'team': 'Team DC'
            },
            {
                'username': 'wonderwoman',
                'email': 'diana.prince@themyscira.com',
                'password': 'hashed_password',
                'full_name': 'Diana Prince',
                'age': 5000,
                'weight': 74,
                'height': 183,
                'fitness_level': 'advanced',
                'team': 'Team DC'
            },
            {
                'username': 'flash',
                'email': 'barry.allen@ccpd.com',
                'password': 'hashed_password',
                'full_name': 'Barry Allen',
                'age': 29,
                'weight': 82,
                'height': 180,
                'fitness_level': 'advanced',
                'team': 'Team DC'
            },
            {
                'username': 'aquaman',
                'email': 'arthur.curry@atlantis.com',
                'password': 'hashed_password',
                'full_name': 'Arthur Curry',
                'age': 37,
                'weight': 148,
                'height': 185,
                'fitness_level': 'advanced',
                'team': 'Team DC'
            }
        ]
        
        all_heroes = marvel_heroes + dc_heroes
        created_users = []
        
        for hero_data in all_heroes:
            user = User.objects.create(**hero_data)
            created_users.append(user)
            
            # Update team members
            if hero_data['team'] == 'Team Marvel':
                team_marvel.members.append(user.username)
            else:
                team_dc.members.append(user.username)
        
        team_marvel.save()
        team_dc.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {User.objects.count()} users'))
        
        # Create Activities
        self.stdout.write('Creating activities...')
        activity_types = [
            'Running', 'Swimming', 'Cycling', 'Weight Training', 
            'Yoga', 'Boxing', 'HIIT', 'CrossFit', 'Rock Climbing'
        ]
        
        activities_created = 0
        for user in created_users:
            # Create 3-7 random activities per user
            num_activities = random.randint(3, 7)
            for _ in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(15, 120)
                distance = round(random.uniform(1, 20), 2) if activity_type in ['Running', 'Swimming', 'Cycling'] else None
                calories = random.randint(100, 800)
                points = duration + (calories // 10)
                
                Activity.objects.create(
                    user_id=user._id,
                    username=user.username,
                    activity_type=activity_type,
                    duration=duration,
                    distance=distance,
                    calories_burned=calories,
                    points=points,
                    notes=f'Great {activity_type.lower()} session!'
                )
                activities_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {activities_created} activities'))
        
        # Calculate and create Leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        
        # User leaderboard
        for user in created_users:
            user_activities = Activity.objects.filter(user_id=user._id)
            total_points = sum(activity.points for activity in user_activities)
            total_activities = user_activities.count()
            
            Leaderboard.objects.create(
                user_id=user._id,
                username=user.username,
                team_name=user.team,
                total_points=total_points,
                total_activities=total_activities,
                rank=0,  # Will be calculated after all entries
                entry_type='user'
            )
        
        # Team leaderboard
        for team in [team_marvel, team_dc]:
            team_users = User.objects.filter(team=team.name)
            team_activities = Activity.objects.filter(username__in=[u.username for u in team_users])
            total_points = sum(activity.points for activity in team_activities)
            total_activities = team_activities.count()
            
            team.total_points = total_points
            team.save()
            
            Leaderboard.objects.create(
                team_name=team.name,
                total_points=total_points,
                total_activities=total_activities,
                rank=0,
                entry_type='team'
            )
        
        # Update ranks
        user_entries = Leaderboard.objects.filter(entry_type='user').order_by('-total_points')
        for rank, entry in enumerate(user_entries, start=1):
            entry.rank = rank
            entry.save()
        
        team_entries = Leaderboard.objects.filter(entry_type='team').order_by('-total_points')
        for rank, entry in enumerate(team_entries, start=1):
            entry.rank = rank
            entry.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {Leaderboard.objects.count()} leaderboard entries'))
        
        # Create Workouts
        self.stdout.write('Creating workout templates...')
        workouts = [
            {
                'name': 'Hero Morning Routine',
                'description': 'Start your day like a superhero with this energizing workout',
                'fitness_level': 'beginner',
                'duration': 30,
                'activity_type': 'HIIT',
                'exercises': ['Jumping Jacks', 'Push-ups', 'Squats', 'Plank', 'Burpees'],
                'estimated_calories': 250,
                'points': 30
            },
            {
                'name': 'Avenger Strength Training',
                'description': 'Build strength worthy of an Avenger',
                'fitness_level': 'intermediate',
                'duration': 45,
                'activity_type': 'Weight Training',
                'exercises': ['Bench Press', 'Deadlifts', 'Squats', 'Pull-ups', 'Shoulder Press'],
                'estimated_calories': 400,
                'points': 50
            },
            {
                'name': 'Justice League Cardio Blast',
                'description': 'High-intensity cardio to match the Flash',
                'fitness_level': 'advanced',
                'duration': 60,
                'activity_type': 'Running',
                'exercises': ['Sprint Intervals', 'Hill Runs', 'Tempo Run', 'Cool Down Jog'],
                'estimated_calories': 600,
                'points': 70
            },
            {
                'name': 'Warrior Yoga Flow',
                'description': 'Find your inner peace and flexibility like Wonder Woman',
                'fitness_level': 'beginner',
                'duration': 45,
                'activity_type': 'Yoga',
                'exercises': ['Sun Salutation', 'Warrior Poses', 'Tree Pose', 'Downward Dog', 'Shavasana'],
                'estimated_calories': 200,
                'points': 40
            },
            {
                'name': 'Thor Hammer Workout',
                'description': 'Swing into action with this full-body power workout',
                'fitness_level': 'advanced',
                'duration': 50,
                'activity_type': 'CrossFit',
                'exercises': ['Kettlebell Swings', 'Box Jumps', 'Rope Climbs', 'Tire Flips', 'Battle Ropes'],
                'estimated_calories': 550,
                'points': 65
            },
            {
                'name': 'Black Widow Agility Training',
                'description': 'Develop speed, agility, and precision',
                'fitness_level': 'intermediate',
                'duration': 40,
                'activity_type': 'HIIT',
                'exercises': ['Ladder Drills', 'Box Jumps', 'Cone Drills', 'Jump Rope', 'Mountain Climbers'],
                'estimated_calories': 350,
                'points': 45
            },
            {
                'name': 'Aquaman Swimming Challenge',
                'description': 'Dive into this comprehensive swimming workout',
                'fitness_level': 'intermediate',
                'duration': 45,
                'activity_type': 'Swimming',
                'exercises': ['Freestyle Laps', 'Backstroke', 'Butterfly', 'Treading Water', 'Underwater Holds'],
                'estimated_calories': 450,
                'points': 55
            },
            {
                'name': 'Batman Combat Training',
                'description': 'Master hand-to-hand combat techniques',
                'fitness_level': 'advanced',
                'duration': 55,
                'activity_type': 'Boxing',
                'exercises': ['Heavy Bag Work', 'Speed Bag', 'Shadow Boxing', 'Pad Work', 'Footwork Drills'],
                'estimated_calories': 500,
                'points': 60
            }
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {Workout.objects.count()} workout templates'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Teams: {Team.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {Activity.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard Entries: {Leaderboard.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {Workout.objects.count()}'))

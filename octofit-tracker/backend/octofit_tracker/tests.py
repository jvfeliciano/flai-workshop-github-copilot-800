from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpass',
            full_name='Test User',
            age=30,
            weight=75,
            height=180,
            fitness_level='intermediate',
            team='Test Team'
        )
    
    def test_user_creation(self):
        """Test that a user can be created"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(str(self.user), 'testuser')
    
    def test_user_unique_email(self):
        """Test that email must be unique"""
        with self.assertRaises(Exception):
            User.objects.create(
                username='testuser2',
                email='test@example.com',  # Duplicate email
                password='testpass2',
                full_name='Test User 2'
            )


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        """Set up test data"""
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            members=['user1', 'user2'],
            total_points=100
        )
    
    def test_team_creation(self):
        """Test that a team can be created"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(len(self.team.members), 2)
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        """Set up test data"""
        self.activity = Activity.objects.create(
            user_id=1,
            username='testuser',
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories_burned=300,
            points=50,
            notes='Great run!'
        )
    
    def test_activity_creation(self):
        """Test that an activity can be created"""
        self.assertEqual(self.activity.username, 'testuser')
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)


class LeaderboardModelTest(TestCase):
    """Test cases for Leaderboard model"""
    
    def setUp(self):
        """Set up test data"""
        self.leaderboard_entry = Leaderboard.objects.create(
            user_id=1,
            username='testuser',
            team_name='Test Team',
            total_points=500,
            total_activities=10,
            rank=1,
            entry_type='user'
        )
    
    def test_leaderboard_creation(self):
        """Test that a leaderboard entry can be created"""
        self.assertEqual(self.leaderboard_entry.username, 'testuser')
        self.assertEqual(self.leaderboard_entry.total_points, 500)
        self.assertEqual(self.leaderboard_entry.rank, 1)


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        """Set up test data"""
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='A test workout',
            fitness_level='beginner',
            duration=30,
            activity_type='HIIT',
            exercises=['Jumping Jacks', 'Push-ups'],
            estimated_calories=250,
            points=30
        )
    
    def test_workout_creation(self):
        """Test that a workout can be created"""
        self.assertEqual(self.workout.name, 'Test Workout')
        self.assertEqual(self.workout.fitness_level, 'beginner')
        self.assertEqual(len(self.workout.exercises), 2)


class APIEndpointTest(APITestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create(
            username='apiuser',
            email='api@example.com',
            password='apipass',
            full_name='API User',
            team='API Team'
        )
        
        self.team = Team.objects.create(
            name='API Team',
            description='Team for API testing',
            members=['apiuser'],
            total_points=0
        )
    
    def test_api_root(self):
        """Test that API root endpoint returns correct links"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)
    
    def test_users_list(self):
        """Test that users list endpoint works"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_teams_list(self):
        """Test that teams list endpoint works"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_user_detail(self):
        """Test that user detail endpoint works"""
        response = self.client.get(f'/api/users/{self.user._id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'apiuser')
    
    def test_team_detail(self):
        """Test that team detail endpoint works"""
        response = self.client.get(f'/api/teams/{self.team._id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'API Team')

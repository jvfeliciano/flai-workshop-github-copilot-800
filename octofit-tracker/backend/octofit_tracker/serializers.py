from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'password', 'full_name', 'age', 
                  'weight', 'height', 'fitness_level', 'team', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'members', 'total_points', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    class Meta:
        model = Activity
        fields = ['_id', 'user_id', 'username', 'activity_type', 'duration', 
                  'distance', 'calories_burned', 'points', 'date', 'notes']


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    class Meta:
        model = Leaderboard
        fields = ['_id', 'user_id', 'username', 'team_name', 'total_points', 
                  'total_activities', 'rank', 'entry_type', 'last_updated']


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    class Meta:
        model = Workout
        fields = ['_id', 'name', 'description', 'fitness_level', 'duration', 
                  'activity_type', 'exercises', 'estimated_calories', 'points', 'created_at']

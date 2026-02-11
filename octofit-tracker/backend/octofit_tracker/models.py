from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    """User model for OctoFit Tracker"""
    _id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=200)
    age = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    fitness_level = models.CharField(max_length=50, null=True, blank=True)
    team = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.username


class Team(models.Model):
    """Team model for organizing users"""
    _id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    members = models.JSONField(default=list)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'teams'
    
    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity model for tracking user exercises"""
    _id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    username = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    distance = models.FloatField(null=True, blank=True)  # in km
    calories_burned = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'activities'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.username} - {self.activity_type}"


class Leaderboard(models.Model):
    """Leaderboard model for ranking users and teams"""
    _id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    team_name = models.CharField(max_length=100, null=True, blank=True)
    total_points = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    entry_type = models.CharField(max_length=20)  # 'user' or 'team'
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leaderboard'
        ordering = ['-total_points']
    
    def __str__(self):
        return f"{self.username or self.team_name} - {self.total_points} points"


class Workout(models.Model):
    """Workout model for personalized workout suggestions"""
    _id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    fitness_level = models.CharField(max_length=50)  # beginner, intermediate, advanced
    duration = models.IntegerField()  # in minutes
    activity_type = models.CharField(max_length=100)
    exercises = models.JSONField(default=list)
    estimated_calories = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'workouts'
    
    def __str__(self):
        return f"{self.name} ({self.fitness_level})"

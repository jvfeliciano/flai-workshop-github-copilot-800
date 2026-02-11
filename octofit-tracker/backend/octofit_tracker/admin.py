from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ['username', 'email', 'full_name', 'team', 'fitness_level', 'created_at']
    list_filter = ['team', 'fitness_level', 'created_at']
    search_fields = ['username', 'email', 'full_name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'password', 'full_name')
        }),
        ('Physical Information', {
            'fields': ('age', 'weight', 'height', 'fitness_level')
        }),
        ('Team Information', {
            'fields': ('team',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    list_display = ['name', 'total_points', 'member_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    def member_count(self, obj):
        return len(obj.members)
    member_count.short_description = 'Members'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = ['username', 'activity_type', 'duration', 'distance', 'calories_burned', 'points', 'date']
    list_filter = ['activity_type', 'date', 'username']
    search_fields = ['username', 'activity_type', 'notes']
    readonly_fields = ['date']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user_id', 'username')
        }),
        ('Activity Details', {
            'fields': ('activity_type', 'duration', 'distance', 'calories_burned', 'points')
        }),
        ('Additional Information', {
            'fields': ('notes', 'date')
        }),
    )


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    list_display = ['rank', 'entry_type', 'display_name', 'total_points', 'total_activities', 'last_updated']
    list_filter = ['entry_type', 'last_updated']
    search_fields = ['username', 'team_name']
    readonly_fields = ['last_updated']
    ordering = ['rank']
    
    def display_name(self, obj):
        return obj.username if obj.username else obj.team_name
    display_name.short_description = 'Name'


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model"""
    list_display = ['name', 'fitness_level', 'activity_type', 'duration', 'estimated_calories', 'points', 'created_at']
    list_filter = ['fitness_level', 'activity_type', 'created_at']
    search_fields = ['name', 'description', 'activity_type']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'fitness_level')
        }),
        ('Workout Details', {
            'fields': ('activity_type', 'duration', 'exercises', 'estimated_calories', 'points')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


# Customize admin site headers
admin.site.site_header = "OctoFit Tracker Administration"
admin.site.site_title = "OctoFit Tracker Admin"
admin.site.index_title = "Welcome to OctoFit Tracker Admin Panel"

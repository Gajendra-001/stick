from django.db import models
from django.conf import settings


class ObstacleDetection(models.Model):
    """
    Obstacle detection data from Smart Blind Stick devices.
    """
    OBSTACLE_TYPES = [
        ('GROUND', 'Ground Level'),
        ('HEAD', 'Head Level'),
        ('POTHOLE', 'Pothole'),
        ('VEHICLE', 'Vehicle'),
        ('PEDESTRIAN', 'Pedestrian'),
        ('WALL', 'Wall'),
        ('STAIRS', 'Stairs'),
        ('DOOR', 'Door'),
        ('OTHER', 'Other'),
    ]
    
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, related_name='obstacle_detections')
    obstacle_type = models.CharField(max_length=15, choices=OBSTACLE_TYPES)
    distance = models.FloatField(help_text="Distance to obstacle in centimeters")
    confidence = models.FloatField(help_text="Detection confidence (0-1)", default=1.0)
    
    # Location data
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    
    # Detection metadata
    sensor_type = models.CharField(max_length=20, default='ULTRASONIC')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Additional data
    severity = models.CharField(max_length=10, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ], default='MEDIUM')
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['device', 'timestamp']),
            models.Index(fields=['obstacle_type', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.device.name} - {self.get_obstacle_type_display()} ({self.distance}cm)"


class UserAnalytics(models.Model):
    """
    Daily analytics summary for users.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    
    # Movement analytics
    total_distance = models.FloatField(default=0.0, help_text="Total distance in kilometers")
    total_duration = models.DurationField(null=True, blank=True)
    average_speed = models.FloatField(null=True, blank=True)
    max_speed = models.FloatField(null=True, blank=True)
    
    # Obstacle analytics
    total_obstacles = models.IntegerField(default=0)
    ground_obstacles = models.IntegerField(default=0)
    head_obstacles = models.IntegerField(default=0)
    pothole_detections = models.IntegerField(default=0)
    vehicle_detections = models.IntegerField(default=0)
    
    # Safety metrics
    safety_score = models.FloatField(default=0.0, help_text="Safety score (0-100)")
    risk_level = models.CharField(max_length=10, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ], default='LOW')
    
    # Route analytics
    unique_locations = models.IntegerField(default=0)
    most_visited_area = models.CharField(max_length=200, blank=True, null=True)
    route_efficiency = models.FloatField(default=0.0, help_text="Route efficiency score")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.date} ({self.total_distance}km)"


class SystemAnalytics(models.Model):
    """
    System-wide analytics and metrics.
    """
    date = models.DateField(unique=True)
    
    # User metrics
    total_users = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)
    new_registrations = models.IntegerField(default=0)
    
    # Device metrics
    total_devices = models.IntegerField(default=0)
    online_devices = models.IntegerField(default=0)
    offline_devices = models.IntegerField(default=0)
    
    # Alert metrics
    total_sos_alerts = models.IntegerField(default=0)
    active_sos_alerts = models.IntegerField(default=0)
    resolved_sos_alerts = models.IntegerField(default=0)
    average_response_time = models.DurationField(null=True, blank=True)
    
    # Obstacle metrics
    total_obstacles_detected = models.IntegerField(default=0)
    most_common_obstacle = models.CharField(max_length=20, blank=True, null=True)
    high_risk_areas = models.JSONField(default=list, blank=True)
    
    # Usage metrics
    total_distance_traveled = models.FloatField(default=0.0)
    total_detection_time = models.DurationField(null=True, blank=True)
    average_daily_usage = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"System Analytics - {self.date}"


class HeatmapData(models.Model):
    """
    Heatmap data for obstacle visualization.
    """
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    obstacle_count = models.IntegerField(default=0)
    obstacle_types = models.JSONField(default=dict, blank=True)
    risk_level = models.CharField(max_length=10, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ], default='LOW')
    
    # Area information
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='India')
    
    # Time range
    start_date = models.DateField()
    end_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-obstacle_count']
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['risk_level']),
        ]
    
    def __str__(self):
        return f"Heatmap - {self.latitude}, {self.longitude} ({self.obstacle_count} obstacles)"

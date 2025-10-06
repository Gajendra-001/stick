from django.db import models
from django.conf import settings


class Location(models.Model):
    """
    GPS location tracking for users.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='locations')
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, related_name='locations', null=True, blank=True)
    
    # GPS coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Location metadata
    accuracy = models.FloatField(help_text="GPS accuracy in meters", null=True, blank=True)
    speed = models.FloatField(help_text="Speed in km/h", null=True, blank=True)
    heading = models.FloatField(help_text="Direction in degrees", null=True, blank=True)
    
    # Context
    is_sos_location = models.BooleanField(default=False)
    is_home_location = models.BooleanField(default=False)
    is_work_location = models.BooleanField(default=False)
    
    # Additional data
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='India')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    def get_point(self):
        """Return coordinates as tuple (longitude, latitude)."""
        return (float(self.longitude), float(self.latitude))
    
    def get_coordinates(self):
        """Return coordinates as tuple."""
        return (float(self.latitude), float(self.longitude))


class Route(models.Model):
    """
    Route tracking for daily journeys.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='routes')
    name = models.CharField(max_length=200, blank=True, null=True)
    start_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='start_routes')
    end_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='end_routes')
    
    # Route metadata
    distance = models.FloatField(help_text="Total distance in kilometers", null=True, blank=True)
    duration = models.DurationField(help_text="Total journey time", null=True, blank=True)
    average_speed = models.FloatField(help_text="Average speed in km/h", null=True, blank=True)
    
    # Route data
    waypoints = models.JSONField(default=list, blank=True)
    polyline_data = models.TextField(blank=True, null=True)
    
    # Timestamps
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.name or 'Route'} ({self.started_at.date()})"
    
    def is_completed(self):
        return self.completed_at is not None


class Geofence(models.Model):
    """
    Geofencing for safe zones and alerts.
    """
    GEOFENCE_TYPES = [
        ('HOME', 'Home'),
        ('WORK', 'Work'),
        ('SAFE_ZONE', 'Safe Zone'),
        ('RESTRICTED', 'Restricted Area'),
        ('CUSTOM', 'Custom'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='geofences')
    name = models.CharField(max_length=200)
    geofence_type = models.CharField(max_length=20, choices=GEOFENCE_TYPES)
    
    # Geofence area (circular)
    center_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    center_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius = models.FloatField(help_text="Radius in meters")
    
    # Settings
    is_active = models.BooleanField(default=True)
    alert_on_entry = models.BooleanField(default=False)
    alert_on_exit = models.BooleanField(default=True)
    notify_guardians = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.get_full_name()}"
    
    def contains_point(self, latitude, longitude):
        """Check if a point is within the geofence."""
        # Simple distance calculation (for circular geofences)
        from math import radians, cos, sin, asin, sqrt
        
        def haversine(lon1, lat1, lon2, lat2):
            """Calculate the great circle distance between two points."""
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            r = 6371000  # Earth radius in meters
            return c * r
        
        distance = haversine(
            float(self.center_longitude), float(self.center_latitude),
            longitude, latitude
        )
        return distance <= self.radius


class LocationHistory(models.Model):
    """
    Historical location data for analytics.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='location_history')
    date = models.DateField()
    total_distance = models.FloatField(default=0.0, help_text="Total distance traveled in km")
    total_duration = models.DurationField(null=True, blank=True)
    locations_count = models.IntegerField(default=0)
    unique_places = models.IntegerField(default=0)
    
    # Summary data
    most_visited_place = models.CharField(max_length=200, blank=True, null=True)
    average_speed = models.FloatField(null=True, blank=True)
    max_speed = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.date} ({self.total_distance}km)"

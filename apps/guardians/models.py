from django.db import models
from django.conf import settings


class GuardianRelation(models.Model):
    """
    Relationship between guardians and users they monitor.
    """
    RELATIONSHIP_TYPES = [
        ('FAMILY', 'Family Member'),
        ('FRIEND', 'Friend'),
        ('CARETAKER', 'Caretaker'),
        ('PROFESSIONAL', 'Professional Caregiver'),
        ('OTHER', 'Other'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='guardian_relations'
    )
    guardian = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='monitored_users'
    )
    relationship_type = models.CharField(max_length=15, choices=RELATIONSHIP_TYPES)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Notification preferences
    notify_sos = models.BooleanField(default=True)
    notify_location = models.BooleanField(default=True)
    notify_device_status = models.BooleanField(default=True)
    notify_daily_summary = models.BooleanField(default=True)
    
    # Communication preferences
    preferred_contact_method = models.CharField(
        max_length=10,
        choices=[
            ('SMS', 'SMS'),
            ('EMAIL', 'Email'),
            ('CALL', 'Phone Call'),
        ],
        default='SMS'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'guardian']
        ordering = ['-is_primary', 'created_at']
    
    def __str__(self):
        return f"{self.guardian.get_full_name()} -> {self.user.get_full_name()}"


class GuardianDashboard(models.Model):
    """
    Guardian dashboard configuration and preferences.
    """
    guardian = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='dashboard_config'
    )
    
    # Dashboard layout preferences
    show_location_map = models.BooleanField(default=True)
    show_device_status = models.BooleanField(default=True)
    show_recent_activity = models.BooleanField(default=True)
    show_analytics = models.BooleanField(default=True)
    
    # Alert preferences
    alert_sound_enabled = models.BooleanField(default=True)
    alert_vibration_enabled = models.BooleanField(default=True)
    auto_refresh_interval = models.IntegerField(default=30, help_text="Auto refresh interval in seconds")
    
    # Map preferences
    default_zoom_level = models.IntegerField(default=15)
    show_geofences = models.BooleanField(default=True)
    show_route_history = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dashboard Config - {self.guardian.get_full_name()}"


class GuardianNotification(models.Model):
    """
    Notifications sent to guardians.
    """
    NOTIFICATION_TYPES = [
        ('SOS_ALERT', 'SOS Alert'),
        ('LOCATION_UPDATE', 'Location Update'),
        ('DEVICE_OFFLINE', 'Device Offline'),
        ('LOW_BATTERY', 'Low Battery'),
        ('GEOFENCE_EXIT', 'Geofence Exit'),
        ('DAILY_SUMMARY', 'Daily Summary'),
    ]
    
    guardian = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='guardian_notifications'
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    
    # Notification content
    title = models.CharField(max_length=200)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    
    # Status tracking
    is_read = models.BooleanField(default=False)
    is_important = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['guardian', 'is_read']),
            models.Index(fields=['notification_type', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.guardian.get_full_name()} - {self.get_notification_type_display()}"
    
    def mark_as_read(self):
        """Mark notification as read."""
        self.is_read = True
        self.read_at = models.DateTimeField().to_internal_value(None)
        self.save()


class GuardianActivity(models.Model):
    """
    Activity log for guardian actions.
    """
    ACTION_TYPES = [
        ('VIEW_LOCATION', 'Viewed Location'),
        ('ACKNOWLEDGE_ALERT', 'Acknowledged Alert'),
        ('RESOLVE_ALERT', 'Resolved Alert'),
        ('SEND_MESSAGE', 'Sent Message'),
        ('CALL_USER', 'Called User'),
        ('VIEW_ANALYTICS', 'Viewed Analytics'),
    ]
    
    guardian = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='activities'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='guardian_activities'
    )
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.guardian.get_full_name()} - {self.get_action_type_display()}"

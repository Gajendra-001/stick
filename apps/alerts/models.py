from django.db import models
from django.conf import settings
from django.utils import timezone


class SOSAlert(models.Model):
    """
    Emergency SOS alerts from users.
    """
    ALERT_STATUS = [
        ('ACTIVE', 'Active'),
        ('ACKNOWLEDGED', 'Acknowledged'),
        ('RESOLVED', 'Resolved'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    PRIORITY_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sos_alerts')
    location = models.ForeignKey('tracking.Location', on_delete=models.CASCADE, related_name='sos_alerts')
    
    # Alert details
    status = models.CharField(max_length=15, choices=ALERT_STATUS, default='ACTIVE')
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='HIGH')
    message = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Response tracking
    acknowledged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        related_name='acknowledged_alerts',
        null=True, 
        blank=True
    )
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        related_name='resolved_alerts',
        null=True, 
        blank=True
    )
    
    # Timestamps
    triggered_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    response_time = models.DurationField(null=True, blank=True)
    
    # Additional data
    device_data = models.JSONField(default=dict, blank=True)
    guardian_notifications = models.JSONField(default=list, blank=True)
    
    class Meta:
        ordering = ['-triggered_at']
    
    def __str__(self):
        return f"SOS Alert - {self.user.get_full_name()} ({self.triggered_at.strftime('%Y-%m-%d %H:%M')})"
    
    def is_active(self):
        return self.status == 'ACTIVE'
    
    def is_resolved(self):
        return self.status == 'RESOLVED'
    
    def calculate_response_time(self):
        """Calculate response time if resolved."""
        if self.resolved_at and self.triggered_at:
            self.response_time = self.resolved_at - self.triggered_at
            self.save()
            return self.response_time
        return None


class AlertNotification(models.Model):
    """
    Notifications sent for alerts.
    """
    NOTIFICATION_TYPES = [
        ('SMS', 'SMS'),
        ('EMAIL', 'Email'),
        ('PUSH', 'Push Notification'),
        ('CALL', 'Phone Call'),
    ]
    
    NOTIFICATION_STATUS = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('DELIVERED', 'Delivered'),
        ('FAILED', 'Failed'),
    ]
    
    alert = models.ForeignKey(SOSAlert, on_delete=models.CASCADE, related_name='notifications')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alert_notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    status = models.CharField(max_length=10, choices=NOTIFICATION_STATUS, default='PENDING')
    
    # Message content
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    
    # Delivery tracking
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True, null=True)
    
    # External service data
    external_id = models.CharField(max_length=100, blank=True, null=True)
    external_data = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.recipient.get_full_name()}"


class EmergencyContact(models.Model):
    """
    Emergency contacts for users.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    relationship = models.CharField(max_length=50)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Notification preferences
    notify_sms = models.BooleanField(default=True)
    notify_email = models.BooleanField(default=True)
    notify_call = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_primary', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.user.get_full_name()}"
    
    def get_contact_info(self):
        """Return contact information as dict."""
        return {
            'name': self.name,
            'phone': self.phone_number,
            'email': self.email,
            'relationship': self.relationship,
            'is_primary': self.is_primary
        }


class AlertTemplate(models.Model):
    """
    Templates for different types of alerts.
    """
    TEMPLATE_TYPES = [
        ('SOS_ALERT', 'SOS Alert'),
        ('LOW_BATTERY', 'Low Battery'),
        ('DEVICE_OFFLINE', 'Device Offline'),
        ('GEOFENCE_EXIT', 'Geofence Exit'),
        ('GEOFENCE_ENTRY', 'Geofence Entry'),
    ]
    
    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    subject_template = models.CharField(max_length=200)
    message_template = models.TextField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    def render_message(self, context):
        """Render message template with context."""
        return self.message_template.format(**context)
    
    def render_subject(self, context):
        """Render subject template with context."""
        return self.subject_template.format(**context)

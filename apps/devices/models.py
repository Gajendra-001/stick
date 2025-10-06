from django.db import models
from django.conf import settings
import uuid


class Device(models.Model):
    """
    Smart Blind Stick device model.
    """
    DEVICE_STATUS = [
        ('ONLINE', 'Online'),
        ('OFFLINE', 'Offline'),
        ('MAINTENANCE', 'Maintenance'),
        ('ERROR', 'Error'),
    ]
    
    device_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=100, default='Smart Blind Stick')
    status = models.CharField(max_length=15, choices=DEVICE_STATUS, default='OFFLINE')
    battery_level = models.IntegerField(default=0, help_text="Battery percentage (0-100)")
    firmware_version = models.CharField(max_length=20, default='1.0.0')
    last_sync = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Device configuration (JSON field for flexible settings)
    configuration = models.JSONField(default=dict, blank=True)
    
    # Sensor status
    ultrasonic_sensor_status = models.BooleanField(default=True)
    infrared_sensor_status = models.BooleanField(default=True)
    gps_sensor_status = models.BooleanField(default=True)
    vibration_motor_status = models.BooleanField(default=True)
    speaker_status = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.device_id}) - {self.user.get_full_name()}"
    
    def is_online(self):
        return self.status == 'ONLINE'
    
    def get_battery_status(self):
        if self.battery_level > 50:
            return 'HIGH'
        elif self.battery_level > 20:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def get_sensor_health(self):
        """Return overall sensor health status."""
        sensors = [
            self.ultrasonic_sensor_status,
            self.infrared_sensor_status,
            self.gps_sensor_status,
            self.vibration_motor_status,
            self.speaker_status
        ]
        working_sensors = sum(sensors)
        total_sensors = len(sensors)
        
        if working_sensors == total_sensors:
            return 'EXCELLENT'
        elif working_sensors >= total_sensors * 0.8:
            return 'GOOD'
        elif working_sensors >= total_sensors * 0.6:
            return 'FAIR'
        else:
            return 'POOR'


class DeviceSettings(models.Model):
    """
    Device configuration settings for each user.
    """
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name='settings')
    
    # Audio settings
    audio_volume = models.IntegerField(default=70, help_text="Volume level (0-100)")
    audio_enabled = models.BooleanField(default=True)
    voice_guidance = models.BooleanField(default=True)
    
    # Vibration settings
    vibration_intensity = models.IntegerField(default=70, help_text="Vibration intensity (0-100)")
    vibration_enabled = models.BooleanField(default=True)
    
    # Detection settings
    obstacle_detection_range = models.IntegerField(default=200, help_text="Detection range in cm")
    head_level_detection = models.BooleanField(default=True)
    ground_level_detection = models.BooleanField(default=True)
    pothole_detection = models.BooleanField(default=True)
    
    # Alert settings
    sos_enabled = models.BooleanField(default=True)
    low_battery_alert = models.BooleanField(default=True)
    device_offline_alert = models.BooleanField(default=True)
    
    # GPS settings
    location_tracking = models.BooleanField(default=True)
    location_update_interval = models.IntegerField(default=30, help_text="Update interval in seconds")
    geofencing_enabled = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Settings for {self.device.name}"


class DeviceLog(models.Model):
    """
    Device activity logs for debugging and monitoring.
    """
    LOG_TYPES = [
        ('SYNC', 'Device Sync'),
        ('BATTERY', 'Battery Update'),
        ('SENSOR', 'Sensor Status'),
        ('ERROR', 'Error'),
        ('CONFIG', 'Configuration Change'),
        ('SOS', 'SOS Alert'),
        ('LOCATION', 'Location Update'),
    ]
    
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='logs')
    log_type = models.CharField(max_length=10, choices=LOG_TYPES)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.device.name} - {self.get_log_type_display()} - {self.timestamp}"

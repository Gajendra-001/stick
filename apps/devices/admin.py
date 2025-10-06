from django.contrib import admin
from .models import Device, DeviceSettings, DeviceLog


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'name', 'user', 'status', 'battery_level', 'last_sync', 'is_active')
    list_filter = ('status', 'is_active', 'created_at', 'last_sync')
    search_fields = ('device_id', 'name', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('device_id', 'created_at', 'updated_at', 'last_sync')
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('device_id', 'user', 'name', 'status', 'is_active')
        }),
        ('Battery & Firmware', {
            'fields': ('battery_level', 'firmware_version', 'last_sync')
        }),
        ('Sensor Status', {
            'fields': (
                'ultrasonic_sensor_status', 'infrared_sensor_status', 'gps_sensor_status',
                'vibration_motor_status', 'speaker_status'
            )
        }),
        ('Configuration', {
            'fields': ('configuration',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DeviceSettings)
class DeviceSettingsAdmin(admin.ModelAdmin):
    list_display = ('device', 'audio_volume', 'vibration_intensity', 'obstacle_detection_range')
    list_filter = ('audio_enabled', 'vibration_enabled', 'voice_guidance', 'sos_enabled')
    raw_id_fields = ('device',)
    
    fieldsets = (
        ('Audio Settings', {
            'fields': ('audio_volume', 'audio_enabled', 'voice_guidance')
        }),
        ('Vibration Settings', {
            'fields': ('vibration_intensity', 'vibration_enabled')
        }),
        ('Detection Settings', {
            'fields': (
                'obstacle_detection_range', 'head_level_detection',
                'ground_level_detection', 'pothole_detection'
            )
        }),
        ('Alert Settings', {
            'fields': ('sos_enabled', 'low_battery_alert', 'device_offline_alert')
        }),
        ('GPS Settings', {
            'fields': ('location_tracking', 'location_update_interval', 'geofencing_enabled')
        }),
    )


@admin.register(DeviceLog)
class DeviceLogAdmin(admin.ModelAdmin):
    list_display = ('device', 'log_type', 'message', 'timestamp')
    list_filter = ('log_type', 'timestamp', 'device__status')
    search_fields = ('device__name', 'message')
    readonly_fields = ('timestamp',)
    raw_id_fields = ('device',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('device')

from rest_framework import serializers
from .models import Device, DeviceSettings, DeviceLog


class DeviceSerializer(serializers.ModelSerializer):
    battery_status = serializers.CharField(source='get_battery_status', read_only=True)
    sensor_health = serializers.CharField(source='get_sensor_health', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Device
        fields = (
            'device_id', 'user', 'user_name', 'name', 'status', 'battery_level',
            'battery_status', 'firmware_version', 'last_sync', 'is_active',
            'ultrasonic_sensor_status', 'infrared_sensor_status', 'gps_sensor_status',
            'vibration_motor_status', 'speaker_status', 'sensor_health',
            'configuration', 'created_at', 'updated_at'
        )
        read_only_fields = ('device_id', 'created_at', 'updated_at', 'last_sync')


class DeviceStatusSerializer(serializers.ModelSerializer):
    """Lightweight serializer for status updates."""
    class Meta:
        model = Device
        fields = ('status', 'battery_level', 'last_sync')


class DeviceSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceSettings
        fields = '__all__'
        read_only_fields = ('device', 'created_at', 'updated_at')


class DeviceLogSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)
    
    class Meta:
        model = DeviceLog
        fields = '__all__'
        read_only_fields = ('timestamp',)


class DeviceRegistrationSerializer(serializers.Serializer):
    """Serializer for device registration."""
    device_id = serializers.UUIDField()
    name = serializers.CharField(max_length=100, required=False)
    firmware_version = serializers.CharField(max_length=20, required=False)
    
    def create(self, validated_data):
        user = self.context['request'].user
        device, created = Device.objects.get_or_create(
            device_id=validated_data['device_id'],
            defaults={
                'user': user,
                'name': validated_data.get('name', 'Smart Blind Stick'),
                'firmware_version': validated_data.get('firmware_version', '1.0.0'),
                'status': 'ONLINE'
            }
        )
        
        if not created:
            device.status = 'ONLINE'
            device.last_sync = serializers.DateTimeField().to_internal_value(None)
            device.save()
        
        # Create default settings if they don't exist
        DeviceSettings.objects.get_or_create(device=device)
        
        return device

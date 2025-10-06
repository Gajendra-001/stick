from rest_framework import serializers
from .models import GuardianRelation, GuardianDashboard, GuardianNotification, GuardianActivity


class GuardianRelationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    guardian_name = serializers.CharField(source='guardian.get_full_name', read_only=True)
    
    class Meta:
        model = GuardianRelation
        fields = (
            'id', 'user', 'user_name', 'guardian', 'guardian_name',
            'relationship_type', 'is_primary', 'is_active',
            'notify_sos', 'notify_location', 'notify_device_status',
            'notify_daily_summary', 'preferred_contact_method',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        # Ensure the current user is either the guardian or the user
        user = self.context['request'].user
        if user.is_guardian():
            validated_data['guardian'] = user
        else:
            validated_data['user'] = user
        
        return super().create(validated_data)


class GuardianDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuardianDashboard
        fields = (
            'id', 'guardian', 'show_location_map', 'show_device_status',
            'show_recent_activity', 'show_analytics', 'alert_sound_enabled',
            'alert_vibration_enabled', 'auto_refresh_interval',
            'default_zoom_level', 'show_geofences', 'show_route_history',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'guardian', 'created_at', 'updated_at')


class GuardianNotificationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = GuardianNotification
        fields = (
            'id', 'guardian', 'user', 'user_name', 'notification_type',
            'title', 'message', 'data', 'is_read', 'is_important',
            'created_at', 'read_at'
        )
        read_only_fields = ('id', 'created_at', 'read_at')


class GuardianActivitySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    guardian_name = serializers.CharField(source='guardian.get_full_name', read_only=True)
    
    class Meta:
        model = GuardianActivity
        fields = (
            'id', 'guardian', 'guardian_name', 'user', 'user_name',
            'action_type', 'description', 'metadata', 'created_at'
        )
        read_only_fields = ('id', 'created_at')

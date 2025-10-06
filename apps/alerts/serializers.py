from rest_framework import serializers
from .models import SOSAlert, AlertNotification, EmergencyContact, AlertTemplate


class SOSAlertSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    location_coordinates = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(source='is_active', read_only=True)
    is_resolved = serializers.BooleanField(source='is_resolved', read_only=True)
    
    class Meta:
        model = SOSAlert
        fields = (
            'id', 'user', 'user_name', 'location', 'status', 'priority',
            'message', 'notes', 'acknowledged_by', 'resolved_by',
            'triggered_at', 'acknowledged_at', 'resolved_at', 'response_time',
            'device_data', 'guardian_notifications', 'location_coordinates',
            'is_active', 'is_resolved'
        )
        read_only_fields = ('id', 'triggered_at', 'response_time')
    
    def get_location_coordinates(self, obj):
        if obj.location:
            return {
                'latitude': float(obj.location.latitude),
                'longitude': float(obj.location.longitude),
                'address': obj.location.address
            }
        return None


class SOSAlertCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating SOS alerts."""
    class Meta:
        model = SOSAlert
        fields = ('location', 'message', 'priority', 'device_data')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class SOSAlertUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating SOS alert status."""
    class Meta:
        model = SOSAlert
        fields = ('status', 'notes')
    
    def update(self, instance, validated_data):
        status = validated_data.get('status')
        
        if status == 'ACKNOWLEDGED' and not instance.acknowledged_at:
            instance.acknowledged_by = self.context['request'].user
            instance.acknowledged_at = serializers.DateTimeField().to_internal_value(None)
        elif status == 'RESOLVED' and not instance.resolved_at:
            instance.resolved_by = self.context['request'].user
            instance.resolved_at = serializers.DateTimeField().to_internal_value(None)
            instance.calculate_response_time()
        
        return super().update(instance, validated_data)


class AlertNotificationSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)
    
    class Meta:
        model = AlertNotification
        fields = (
            'id', 'alert', 'recipient', 'recipient_name', 'notification_type',
            'status', 'subject', 'message', 'sent_at', 'delivered_at',
            'failure_reason', 'external_id', 'external_data', 'created_at'
        )
        read_only_fields = ('id', 'sent_at', 'delivered_at', 'created_at')


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = (
            'id', 'user', 'name', 'phone_number', 'email', 'relationship',
            'is_primary', 'is_active', 'notify_sms', 'notify_email',
            'notify_call', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AlertTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertTemplate
        fields = (
            'id', 'name', 'template_type', 'subject_template',
            'message_template', 'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class SOSAlertListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for alert lists."""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    location_address = serializers.CharField(source='location.address', read_only=True)
    
    class Meta:
        model = SOSAlert
        fields = (
            'id', 'user', 'user_name', 'status', 'priority', 'triggered_at',
            'location_address', 'message'
        )

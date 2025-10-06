from rest_framework import serializers
from .models import ObstacleDetection, UserAnalytics, SystemAnalytics, HeatmapData


class ObstacleDetectionSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)
    user_name = serializers.CharField(source='device.user.get_full_name', read_only=True)
    
    class Meta:
        model = ObstacleDetection
        fields = (
            'id', 'device', 'device_name', 'user_name', 'obstacle_type',
            'distance', 'confidence', 'latitude', 'longitude', 'address',
            'sensor_type', 'severity', 'timestamp'
        )
        read_only_fields = ('id', 'timestamp')


class UserAnalyticsSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = UserAnalytics
        fields = (
            'id', 'user', 'user_name', 'date', 'total_distance', 'total_duration',
            'average_speed', 'max_speed', 'total_obstacles', 'ground_obstacles',
            'head_obstacles', 'pothole_detections', 'vehicle_detections',
            'safety_score', 'risk_level', 'unique_locations', 'most_visited_area',
            'route_efficiency', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class SystemAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemAnalytics
        fields = (
            'id', 'date', 'total_users', 'active_users', 'new_registrations',
            'total_devices', 'online_devices', 'offline_devices',
            'total_sos_alerts', 'active_sos_alerts', 'resolved_sos_alerts',
            'average_response_time', 'total_obstacles_detected',
            'most_common_obstacle', 'high_risk_areas', 'total_distance_traveled',
            'total_detection_time', 'average_daily_usage', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class HeatmapDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeatmapData
        fields = (
            'id', 'latitude', 'longitude', 'obstacle_count', 'obstacle_types',
            'risk_level', 'city', 'state', 'country', 'start_date', 'end_date',
            'created_at'
        )
        read_only_fields = ('id', 'created_at')

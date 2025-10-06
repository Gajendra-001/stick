from rest_framework import serializers
from .models import Location, Route, Geofence, LocationHistory


class LocationSerializer(serializers.ModelSerializer):
    coordinates = serializers.SerializerMethodField()
    
    class Meta:
        model = Location
        fields = (
            'id', 'user', 'device', 'latitude', 'longitude', 'altitude',
            'accuracy', 'speed', 'heading', 'is_sos_location', 'is_home_location',
            'is_work_location', 'address', 'city', 'state', 'country',
            'timestamp', 'coordinates'
        )
        read_only_fields = ('id', 'timestamp')
    
    def get_coordinates(self, obj):
        return obj.get_coordinates()


class LocationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating location updates from device."""
    class Meta:
        model = Location
        fields = (
            'latitude', 'longitude', 'altitude', 'accuracy', 'speed',
            'heading', 'is_sos_location', 'address', 'city', 'state', 'country'
        )
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class RouteSerializer(serializers.ModelSerializer):
    start_location = LocationSerializer(read_only=True)
    end_location = LocationSerializer(read_only=True)
    is_completed = serializers.BooleanField(source='is_completed', read_only=True)
    
    class Meta:
        model = Route
        fields = (
            'id', 'user', 'name', 'start_location', 'end_location',
            'distance', 'duration', 'average_speed', 'waypoints',
            'polyline_data', 'started_at', 'completed_at', 'created_at',
            'is_completed'
        )
        read_only_fields = ('id', 'created_at')


class RouteCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new routes."""
    class Meta:
        model = Route
        fields = ('name', 'start_location', 'end_location', 'started_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class GeofenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geofence
        fields = (
            'id', 'user', 'name', 'geofence_type', 'center_latitude',
            'center_longitude', 'radius', 'is_active', 'alert_on_entry',
            'alert_on_exit', 'notify_guardians', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class LocationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationHistory
        fields = (
            'id', 'user', 'date', 'total_distance', 'total_duration',
            'locations_count', 'unique_places', 'most_visited_place',
            'average_speed', 'max_speed', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class LocationUpdateSerializer(serializers.Serializer):
    """Serializer for real-time location updates."""
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    altitude = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)
    accuracy = serializers.FloatField(required=False)
    speed = serializers.FloatField(required=False)
    heading = serializers.FloatField(required=False)
    address = serializers.CharField(max_length=500, required=False)
    city = serializers.CharField(max_length=100, required=False)
    state = serializers.CharField(max_length=100, required=False)
    country = serializers.CharField(max_length=100, default='India')

from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import GuardianRelation, GuardianDashboard, GuardianNotification, GuardianActivity
from .serializers import (
    GuardianRelationSerializer, GuardianDashboardSerializer,
    GuardianNotificationSerializer, GuardianActivitySerializer
)


class GuardianRelationListView(generics.ListCreateAPIView):
    """List or create guardian relationships."""
    serializer_class = GuardianRelationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_guardian():
            return GuardianRelation.objects.filter(guardian=user, is_active=True)
        else:
            return GuardianRelation.objects.filter(user=user, is_active=True)
    
    def perform_create(self, serializer):
        if self.request.user.is_guardian():
            serializer.save(guardian=self.request.user)
        else:
            serializer.save(user=self.request.user)


class GuardianRelationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a guardian relationship."""
    serializer_class = GuardianRelationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_guardian():
            return GuardianRelation.objects.filter(guardian=user)
        else:
            return GuardianRelation.objects.filter(user=user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def guardian_dashboard(request):
    """Get guardian dashboard data."""
    if not request.user.is_guardian():
        return Response({'error': 'Guardian access required'}, status=status.HTTP_403_FORBIDDEN)
    
    guardian = request.user
    
    # Get monitored users
    relations = GuardianRelation.objects.filter(guardian=guardian, is_active=True)
    monitored_users = [relation.user for relation in relations]
    
    # Get recent activities
    recent_activities = GuardianActivity.objects.filter(
        guardian=guardian
    ).order_by('-created_at')[:10]
    
    # Get unread notifications
    unread_notifications = GuardianNotification.objects.filter(
        guardian=guardian,
        is_read=False
    ).order_by('-created_at')
    
    # Get active alerts
    from apps.alerts.models import SOSAlert
    active_alerts = SOSAlert.objects.filter(
        user__in=monitored_users,
        status='ACTIVE'
    ).order_by('-triggered_at')
    
    return Response({
        'monitored_users': [
            {
                'id': user.id,
                'name': user.get_full_name(),
                'status': 'online',  # TODO: Get actual device status
                'last_location': None,  # TODO: Get last location
                'active_alerts': active_alerts.filter(user=user).count()
            }
            for user in monitored_users
        ],
        'recent_activities': GuardianActivitySerializer(recent_activities, many=True).data,
        'unread_notifications': GuardianNotificationSerializer(unread_notifications, many=True).data,
        'active_alerts': len(active_alerts)
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def monitored_user_detail(request, user_id):
    """Get detailed information about a monitored user."""
    if not request.user.is_guardian():
        return Response({'error': 'Guardian access required'}, status=status.HTTP_403_FORBIDDEN)
    
    # Check if guardian has permission to monitor this user
    relation = get_object_or_404(
        GuardianRelation,
        guardian=request.user,
        user_id=user_id,
        is_active=True
    )
    
    user = relation.user
    
    # Get user's current location
    from apps.tracking.models import Location
    current_location = Location.objects.filter(user=user).first()
    
    # Get user's devices
    devices = user.devices.all()
    
    # Get recent activity
    recent_activities = GuardianActivity.objects.filter(
        guardian=request.user,
        user=user
    ).order_by('-created_at')[:20]
    
    # Get active alerts
    from apps.alerts.models import SOSAlert
    active_alerts = SOSAlert.objects.filter(
        user=user,
        status='ACTIVE'
    ).order_by('-triggered_at')
    
    return Response({
        'user': {
            'id': user.id,
            'name': user.get_full_name(),
            'phone': user.phone_number,
            'email': user.email,
            'visual_impairment_level': user.visual_impairment_level,
            'emergency_contact_name': user.emergency_contact_name,
            'emergency_contact_phone': user.emergency_contact_phone
        },
        'current_location': {
            'latitude': float(current_location.latitude) if current_location else None,
            'longitude': float(current_location.longitude) if current_location else None,
            'address': current_location.address if current_location else None,
            'timestamp': current_location.timestamp.isoformat() if current_location else None
        } if current_location else None,
        'devices': [
            {
                'id': str(device.device_id),
                'name': device.name,
                'status': device.status,
                'battery_level': device.battery_level,
                'last_sync': device.last_sync.isoformat()
            }
            for device in devices
        ],
        'recent_activities': GuardianActivitySerializer(recent_activities, many=True).data,
        'active_alerts': len(active_alerts)
    })


class GuardianNotificationListView(generics.ListAPIView):
    """List guardian notifications."""
    serializer_class = GuardianNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_guardian():
            return GuardianNotification.objects.none()
        
        return GuardianNotification.objects.filter(
            guardian=self.request.user
        ).order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notification_id):
    """Mark a notification as read."""
    if not request.user.is_guardian():
        return Response({'error': 'Guardian access required'}, status=status.HTTP_403_FORBIDDEN)
    
    notification = get_object_or_404(
        GuardianNotification,
        id=notification_id,
        guardian=request.user
    )
    
    notification.mark_as_read()
    
    return Response({'message': 'Notification marked as read'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_message_to_user(request, user_id):
    """Send a message to a monitored user."""
    if not request.user.is_guardian():
        return Response({'error': 'Guardian access required'}, status=status.HTTP_403_FORBIDDEN)
    
    # Check if guardian has permission to monitor this user
    relation = get_object_or_404(
        GuardianRelation,
        guardian=request.user,
        user_id=user_id,
        is_active=True
    )
    
    message = request.data.get('message')
    if not message:
        return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # TODO: Implement message sending to user's device
    # This could be via SMS, push notification, or device communication
    
    # Log the activity
    GuardianActivity.objects.create(
        guardian=request.user,
        user=relation.user,
        action_type='SEND_MESSAGE',
        description=f"Sent message: {message[:50]}...",
        metadata={'message': message}
    )
    
    return Response({'message': 'Message sent successfully'})


class GuardianActivityListView(generics.ListAPIView):
    """List guardian activities."""
    serializer_class = GuardianActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_guardian():
            return GuardianActivity.objects.none()
        
        return GuardianActivity.objects.filter(
            guardian=self.request.user
        ).order_by('-created_at')


class GuardianDashboardView(generics.RetrieveUpdateAPIView):
    """Manage guardian dashboard configuration."""
    serializer_class = GuardianDashboardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        if not self.request.user.is_guardian():
            return None
        
        dashboard, created = GuardianDashboard.objects.get_or_create(
            guardian=self.request.user
        )
        return dashboard

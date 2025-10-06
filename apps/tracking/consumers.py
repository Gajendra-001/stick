import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Location


class LocationConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time location updates."""
    
    async def connect(self):
        self.user = self.scope['user']
        if self.user == AnonymousUser():
            await self.close()
            return
        
        self.location_group_name = f'location_{self.user.id}'
        
        # Join location group
        await self.channel_layer.group_add(
            self.location_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave location group
        await self.channel_layer.group_discard(
            self.location_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'location_update':
            await self.handle_location_update(text_data_json)
        elif message_type == 'subscribe_guardian':
            await self.handle_guardian_subscription(text_data_json)
    
    async def handle_location_update(self, data):
        """Handle location update from device."""
        location_data = data.get('location', {})
        
        # Save location to database
        location = await self.save_location(location_data)
        
        # Send to user's location group
        await self.channel_layer.group_send(
            self.location_group_name,
            {
                'type': 'location_update',
                'location': {
                    'latitude': float(location.latitude),
                    'longitude': float(location.longitude),
                    'timestamp': location.timestamp.isoformat(),
                    'accuracy': location.accuracy,
                    'speed': location.speed,
                    'address': location.address,
                }
            }
        )
    
    async def handle_guardian_subscription(self, data):
        """Handle guardian subscribing to user's location."""
        user_id = data.get('user_id')
        if user_id:
            guardian_group = f'guardian_{user_id}'
            await self.channel_layer.group_add(
                guardian_group,
                self.channel_name
            )
    
    # Receive message from group
    async def location_update(self, event):
        """Send location update to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'location_update',
            'data': event['location']
        }))
    
    async def sos_alert(self, event):
        """Send SOS alert to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'sos_alert',
            'data': event['alert']
        }))
    
    @database_sync_to_async
    def save_location(self, location_data):
        """Save location to database."""
        return Location.objects.create(
            user=self.user,
            latitude=location_data.get('latitude'),
            longitude=location_data.get('longitude'),
            altitude=location_data.get('altitude'),
            accuracy=location_data.get('accuracy'),
            speed=location_data.get('speed'),
            heading=location_data.get('heading'),
            address=location_data.get('address'),
            city=location_data.get('city'),
            state=location_data.get('state'),
            country=location_data.get('country', 'India')
        )

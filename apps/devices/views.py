from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def device_detail(request):
    """Device detail page view."""
    # Mock device data - in real app, this would come from database
    device_data = {
        'device_id': 'SBS-001-2024',
        'status': 'Online',
        'battery_level': 85,
        'last_sync': '2 minutes ago',
        'firmware_version': 'v2.1.3',
        'vibration_intensity': 7,
        'audio_volume': 8,
        'auto_sync': True,
        'sensors': {
            'ultrasonic': {'status': 'Working', 'last_check': '1 minute ago'},
            'infrared': {'status': 'Working', 'last_check': '1 minute ago'},
            'gps': {'status': 'Working', 'last_check': '30 seconds ago'},
        }
    }
    
    if request.method == 'POST':
        # Handle device settings update
        vibration = request.POST.get('vibration_intensity', 7)
        volume = request.POST.get('audio_volume', 8)
        auto_sync = request.POST.get('auto_sync') == 'on'
        
        # In real app, save to database
        device_data['vibration_intensity'] = int(vibration)
        device_data['audio_volume'] = int(volume)
        device_data['auto_sync'] = auto_sync
        
        return JsonResponse({'success': True, 'message': 'Device settings updated successfully!'})
    
    return render(request, 'devices/device_detail.html', {
        'device': device_data,
        'active_page': 'device'
    })
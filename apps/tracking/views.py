from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def location_tracking(request):
    """Location tracking page view."""
    # Mock location data - in real app, this would come from database
    location_data = {
        'current_location': {
            'latitude': 28.6139,
            'longitude': 77.2090,
            'accuracy': 5.2,
            'last_updated': '2 minutes ago',
            'address': 'Central Secretariat, New Delhi, India'
        },
        'safe_zones': [
            {
                'id': 1,
                'name': 'Home',
                'latitude': 28.6139,
                'longitude': 77.2090,
                'radius': 100,
                'status': 'Active'
            },
            {
                'id': 2,
                'name': 'Office',
                'latitude': 28.6145,
                'longitude': 77.2095,
                'radius': 50,
                'status': 'Active'
            }
        ],
        'recent_locations': [
            {
                'latitude': 28.6139,
                'longitude': 77.2090,
                'timestamp': '2 minutes ago',
                'address': 'Central Secretariat'
            },
            {
                'latitude': 28.6145,
                'longitude': 77.2095,
                'timestamp': '5 minutes ago',
                'address': 'Parliament House'
            },
            {
                'latitude': 28.6150,
                'longitude': 77.2100,
                'timestamp': '10 minutes ago',
                'address': 'India Gate'
            }
        ]
    }
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_safe_zone':
            name = request.POST.get('name')
            latitude = float(request.POST.get('latitude'))
            longitude = float(request.POST.get('longitude'))
            radius = int(request.POST.get('radius', 100))
            
            # In real app, save to database
            new_zone = {
                'id': len(location_data['safe_zones']) + 1,
                'name': name,
                'latitude': latitude,
                'longitude': longitude,
                'radius': radius,
                'status': 'Active'
            }
            location_data['safe_zones'].append(new_zone)
            
            return JsonResponse({'success': True, 'message': 'Safe zone added successfully!'})
        
        elif action == 'remove_safe_zone':
            zone_id = int(request.POST.get('zone_id'))
            # In real app, remove from database
            location_data['safe_zones'] = [zone for zone in location_data['safe_zones'] if zone['id'] != zone_id]
            
            return JsonResponse({'success': True, 'message': 'Safe zone removed successfully!'})
    
    return render(request, 'tracking/location.html', {
        'location_data': location_data,
        'active_page': 'location'
    })
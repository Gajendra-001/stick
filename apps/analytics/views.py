from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta

@login_required
def analytics_dashboard(request):
    """Analytics dashboard page view."""
    # Mock analytics data - in real app, this would come from database
    analytics_data = {
        'summary_stats': {
            'distance_traveled': 12.5,  # km
            'obstacles_detected': 156,
            'sos_activations': 2,
            'avg_response_time': 3.2  # minutes
        },
        'daily_activity': [
            {'date': '2024-01-15', 'obstacles': 23, 'distance': 2.1},
            {'date': '2024-01-14', 'obstacles': 18, 'distance': 1.8},
            {'date': '2024-01-13', 'obstacles': 31, 'distance': 3.2},
            {'date': '2024-01-12', 'obstacles': 15, 'distance': 1.5},
            {'date': '2024-01-11', 'obstacles': 27, 'distance': 2.8},
            {'date': '2024-01-10', 'obstacles': 22, 'distance': 2.3},
            {'date': '2024-01-09', 'obstacles': 20, 'distance': 1.9}
        ],
        'obstacle_types': [
            {'type': 'Ground Level', 'count': 89, 'percentage': 57},
            {'type': 'Head Level', 'count': 34, 'percentage': 22},
            {'type': 'Pothole', 'count': 21, 'percentage': 13},
            {'type': 'Vehicle', 'count': 12, 'percentage': 8}
        ],
        'activity_distribution': [
            {'period': 'Morning (6-12)', 'percentage': 35},
            {'period': 'Afternoon (12-18)', 'percentage': 40},
            {'period': 'Evening (18-24)', 'percentage': 20},
            {'period': 'Night (0-6)', 'percentage': 5}
        ],
        'high_risk_areas': [
            {'location': 'Central Secretariat', 'risk_score': 8.5, 'incidents': 12},
            {'location': 'India Gate', 'risk_score': 7.2, 'incidents': 8},
            {'location': 'Connaught Place', 'risk_score': 6.8, 'incidents': 6},
            {'location': 'Rajpath', 'risk_score': 6.1, 'incidents': 4}
        ]
    }
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'export_report':
            format_type = request.POST.get('format', 'pdf')
            date_range = request.POST.get('date_range', '7_days')
            
            # In real app, generate and return the report file
            return JsonResponse({
                'success': True, 
                'message': f'Report exported successfully in {format_type.upper()} format!',
                'download_url': f'/reports/analytics_report_{date_range}.{format_type}'
            })
    
    return render(request, 'analytics/dashboard.html', {
        'analytics_data': analytics_data,
        'active_page': 'analytics'
    })
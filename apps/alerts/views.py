from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta

@login_required
def alerts_list(request):
    """Alerts list page view."""
    # Mock alerts data - in real app, this would come from database
    alerts_data = {
        'active_alerts': [],
        'alert_history': [
            {
                'id': 1,
                'type': 'SOS',
                'timestamp': '2024-01-15 14:30:00',
                'location': 'Central Secretariat, New Delhi',
                'response_time': '2 minutes',
                'status': 'Resolved',
                'resolved_by': 'Emergency Services'
            },
            {
                'id': 2,
                'type': 'Battery Low',
                'timestamp': '2024-01-15 12:15:00',
                'location': 'India Gate, New Delhi',
                'response_time': 'N/A',
                'status': 'Resolved',
                'resolved_by': 'User'
            },
            {
                'id': 3,
                'type': 'Device Offline',
                'timestamp': '2024-01-14 18:45:00',
                'location': 'Home',
                'response_time': '5 minutes',
                'status': 'Resolved',
                'resolved_by': 'Guardian'
            }
        ],
        'alert_settings': {
            'sms_alerts': True,
            'email_notifications': True,
            'auto_call_emergency': False,
            'guardian_notifications': True
        }
    }
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'test_sos':
            # In real app, trigger actual SOS alert
            return JsonResponse({'success': True, 'message': 'SOS test alert sent successfully!'})
        
        elif action == 'update_settings':
            sms_alerts = request.POST.get('sms_alerts') == 'on'
            email_notifications = request.POST.get('email_notifications') == 'on'
            auto_call_emergency = request.POST.get('auto_call_emergency') == 'on'
            guardian_notifications = request.POST.get('guardian_notifications') == 'on'
            
            # In real app, save to database
            alerts_data['alert_settings'] = {
                'sms_alerts': sms_alerts,
                'email_notifications': email_notifications,
                'auto_call_emergency': auto_call_emergency,
                'guardian_notifications': guardian_notifications
            }
            
            return JsonResponse({'success': True, 'message': 'Alert settings updated successfully!'})
    
    return render(request, 'alerts/alerts_list.html', {
        'alerts_data': alerts_data,
        'active_page': 'alerts'
    })
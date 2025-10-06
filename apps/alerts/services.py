"""
Alert services for handling notifications and communications.
"""
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from twilio.rest import Client
from .models import SOSAlert, AlertNotification, EmergencyContact, AlertTemplate


class AlertService:
    """Service class for handling alert notifications."""
    
    def __init__(self):
        self.twilio_client = None
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.twilio_client = Client(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )
    
    def send_sos_notifications(self, alert):
        """Send SOS notifications to all emergency contacts."""
        user = alert.user
        emergency_contacts = EmergencyContact.objects.filter(
            user=user, 
            is_active=True
        )
        
        for contact in emergency_contacts:
            # Send SMS if enabled
            if contact.notify_sms and contact.phone_number:
                self.send_sms_notification(alert, contact)
            
            # Send email if enabled
            if contact.notify_email and contact.email:
                self.send_email_notification(alert, contact)
            
            # TODO: Implement phone call notifications
            if contact.notify_call and contact.phone_number:
                self.send_call_notification(alert, contact)
    
    def send_sms_notification(self, alert, contact):
        """Send SMS notification via Twilio."""
        if not self.twilio_client:
            return
        
        try:
            message = self._get_sos_message(alert)
            
            self.twilio_client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=contact.phone_number
            )
            
            # Create notification record
            AlertNotification.objects.create(
                alert=alert,
                recipient=contact.user,
                notification_type='SMS',
                status='SENT',
                message=message,
                sent_at=timezone.now()
            )
            
        except Exception as e:
            # Create failed notification record
            AlertNotification.objects.create(
                alert=alert,
                recipient=contact.user,
                notification_type='SMS',
                status='FAILED',
                message=self._get_sos_message(alert),
                failure_reason=str(e)
            )
    
    def send_email_notification(self, alert, contact):
        """Send email notification."""
        try:
            subject = f"SOS Alert - {alert.user.get_full_name()}"
            message = self._get_sos_email_message(alert)
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact.email],
                fail_silently=False
            )
            
            # Create notification record
            AlertNotification.objects.create(
                alert=alert,
                recipient=contact.user,
                notification_type='EMAIL',
                status='SENT',
                subject=subject,
                message=message,
                sent_at=timezone.now()
            )
            
        except Exception as e:
            # Create failed notification record
            AlertNotification.objects.create(
                alert=alert,
                recipient=contact.user,
                notification_type='EMAIL',
                status='FAILED',
                subject=f"SOS Alert - {alert.user.get_full_name()}",
                message=self._get_sos_email_message(alert),
                failure_reason=str(e)
            )
    
    def send_call_notification(self, alert, contact):
        """Send phone call notification via Twilio."""
        if not self.twilio_client:
            return
        
        try:
            # TODO: Implement Twilio voice call
            pass
            
        except Exception as e:
            AlertNotification.objects.create(
                alert=alert,
                recipient=contact.user,
                notification_type='CALL',
                status='FAILED',
                message=f"Call notification failed: {str(e)}"
            )
    
    def _get_sos_message(self, alert):
        """Get SMS message for SOS alert."""
        location = alert.location
        coordinates = f"{location.latitude}, {location.longitude}"
        address = location.address or "Location not available"
        
        return f"""
🚨 SOS ALERT 🚨
{alert.user.get_full_name()} needs immediate help!

📍 Location: {address}
📍 Coordinates: {coordinates}
⏰ Time: {alert.triggered_at.strftime('%Y-%m-%d %H:%M:%S')}

Please respond immediately!
        """.strip()
    
    def _get_sos_email_message(self, alert):
        """Get email message for SOS alert."""
        location = alert.location
        coordinates = f"{location.latitude}, {location.longitude}"
        address = location.address or "Location not available"
        
        return f"""
SOS ALERT - {alert.user.get_full_name()}

The user has triggered an emergency SOS alert and needs immediate assistance.

DETAILS:
- Name: {alert.user.get_full_name()}
- Phone: {alert.user.phone_number or 'Not provided'}
- Location: {address}
- Coordinates: {coordinates}
- Time: {alert.triggered_at.strftime('%Y-%m-%d %H:%M:%S')}
- Message: {alert.message or 'No additional message'}

Please respond immediately and check on the user's safety.

Smart Blind Stick Emergency System
        """.strip()
    
    def send_low_battery_alert(self, device):
        """Send low battery alert to user and guardians."""
        user = device.user
        
        # Get low battery template
        template = AlertTemplate.objects.filter(
            template_type='LOW_BATTERY',
            is_active=True
        ).first()
        
        if template:
            context = {
                'user_name': user.get_full_name(),
                'device_name': device.name,
                'battery_level': device.battery_level,
                'device_id': str(device.device_id)
            }
            
            subject = template.render_subject(context)
            message = template.render_message(context)
            
            # Send to user's email
            if user.email:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True
                )
    
    def send_device_offline_alert(self, device):
        """Send device offline alert to guardians."""
        user = device.user
        
        # Get device offline template
        template = AlertTemplate.objects.filter(
            template_type='DEVICE_OFFLINE',
            is_active=True
        ).first()
        
        if template:
            context = {
                'user_name': user.get_full_name(),
                'device_name': device.name,
                'last_sync': device.last_sync.strftime('%Y-%m-%d %H:%M:%S'),
                'device_id': str(device.device_id)
            }
            
            subject = template.render_subject(context)
            message = template.render_message(context)
            
            # Send to emergency contacts
            emergency_contacts = EmergencyContact.objects.filter(
                user=user,
                is_active=True,
                notify_email=True
            )
            
            for contact in emergency_contacts:
                if contact.email:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[contact.email],
                        fail_silently=True
                    )

from django.contrib import admin
from .models import SOSAlert, AlertNotification, EmergencyContact, AlertTemplate


@admin.register(SOSAlert)
class SOSAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'priority', 'triggered_at', 'acknowledged_at', 'resolved_at')
    list_filter = ('status', 'priority', 'triggered_at', 'acknowledged_at', 'resolved_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'message')
    readonly_fields = ('triggered_at', 'response_time')
    raw_id_fields = ('user', 'location', 'acknowledged_by', 'resolved_by')
    
    fieldsets = (
        ('Alert Information', {
            'fields': ('user', 'location', 'status', 'priority', 'message', 'notes')
        }),
        ('Response Tracking', {
            'fields': ('acknowledged_by', 'acknowledged_at', 'resolved_by', 'resolved_at', 'response_time')
        }),
        ('Additional Data', {
            'fields': ('device_data', 'guardian_notifications'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AlertNotification)
class AlertNotificationAdmin(admin.ModelAdmin):
    list_display = ('alert', 'recipient', 'notification_type', 'status', 'sent_at', 'delivered_at')
    list_filter = ('notification_type', 'status', 'sent_at', 'created_at')
    search_fields = ('alert__user__username', 'recipient__username', 'subject', 'message')
    readonly_fields = ('sent_at', 'delivered_at')
    raw_id_fields = ('alert', 'recipient')


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone_number', 'relationship', 'is_primary', 'is_active')
    list_filter = ('is_primary', 'is_active', 'relationship', 'created_at')
    search_fields = ('user__username', 'name', 'phone_number', 'email')
    raw_id_fields = ('user',)


@admin.register(AlertTemplate)
class AlertTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_type', 'is_active', 'created_at')
    list_filter = ('template_type', 'is_active', 'created_at')
    search_fields = ('name', 'subject_template', 'message_template')

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('role', 'is_verified', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Smart Blind Stick Info', {
            'fields': ('role', 'phone_number', 'profile_picture', 'visual_impairment_level', 'medical_notes')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Verification', {
            'fields': ('is_verified',)
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Smart Blind Stick Info', {
            'fields': ('role', 'phone_number', 'visual_impairment_level')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'country', 'created_at')
    list_filter = ('country', 'state', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'city', 'state')
    raw_id_fields = ('user',)

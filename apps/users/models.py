from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom User model for Smart Blind Stick application.
    Supports different user types: visually impaired users, guardians, and admins.
    """
    
    USER_ROLES = [
        ('USER', 'Visually Impaired User'),
        ('GUARDIAN', 'Guardian/Caretaker'),
        ('ADMIN', 'Administrator'),
    ]
    
    VISUAL_IMPAIRMENT_LEVELS = [
        ('MILD', 'Mild Visual Impairment'),
        ('MODERATE', 'Moderate Visual Impairment'),
        ('SEVERE', 'Severe Visual Impairment'),
        ('BLIND', 'Blind'),
    ]
    
    role = models.CharField(max_length=10, choices=USER_ROLES, default='USER')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")],
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    visual_impairment_level = models.CharField(
        max_length=10, 
        choices=VISUAL_IMPAIRMENT_LEVELS, 
        blank=True, 
        null=True
    )
    medical_notes = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip() or self.username
    
    def is_visually_impaired(self):
        return self.role == 'USER'
    
    def is_guardian(self):
        return self.role == 'GUARDIAN'
    
    def is_admin(self):
        return self.role == 'ADMIN'


class UserProfile(models.Model):
    """
    Extended profile information for users.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='India')
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    preferred_language = models.CharField(max_length=10, default='en')
    accessibility_preferences = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} Profile"

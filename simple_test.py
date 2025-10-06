#!/usr/bin/env python3
"""
Simple test to check registration
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

def test_user_creation():
    """Test creating a user"""
    try:
        # Check if user already exists
        if User.objects.filter(username='testuser').exists():
            print("✅ User 'testuser' already exists")
            return
        
        # Create user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User',
            role='USER',
            phone_number='+1234567890',
            visual_impairment_level='MILD',
            emergency_contact_name='Emergency Contact',
            emergency_contact_phone='+1234567891'
        )
        
        print("✅ User created successfully")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Role: {user.role}")
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_user_creation()

#!/usr/bin/env python3
"""
Test script to verify registration functionality
"""

import requests
import json

def test_registration():
    """Test the registration endpoint"""
    base_url = "http://localhost:8000"
    
    # Test data
    test_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123',
        'password_confirm': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'USER',
        'phone_number': '+1234567890',
        'visual_impairment_level': 'MILD',
        'emergency_contact_name': 'Emergency Contact',
        'emergency_contact_phone': '+1234567891'
    }
    
    print("🧪 Testing Smart Blind Stick Registration")
    print("=" * 50)
    
    try:
        # Test registration page
        print("1. Testing registration page...")
        response = requests.get(f"{base_url}/register/")
        if response.status_code == 200:
            print("✅ Registration page loads successfully")
        else:
            print(f"❌ Registration page failed: {response.status_code}")
            return
        
        # Test registration form submission
        print("2. Testing registration form submission...")
        
        # Get CSRF token
        session = requests.Session()
        get_response = session.get(f"{base_url}/register/")
        csrf_token = None
        
        # Extract CSRF token from the page
        import re
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', get_response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            test_data['csrfmiddlewaretoken'] = csrf_token
            print("✅ CSRF token found")
        else:
            print("⚠️  CSRF token not found, trying without it")
        
        response = session.post(f"{base_url}/register/", data=test_data)
        
        if response.status_code == 200:
            print("✅ Registration form submitted successfully")
            if "error" in response.text.lower() or "invalid" in response.text.lower():
                print("⚠️  Form validation working (errors detected)")
            else:
                print("✅ Registration completed successfully")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Django is running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_registration()

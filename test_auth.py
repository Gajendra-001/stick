#!/usr/bin/env python3
"""
Test authentication flow
"""

import requests
import re

def test_auth_flow():
    """Test the complete authentication flow"""
    base_url = "http://localhost:8000"
    session = requests.Session()
    
    print("🧪 Testing Authentication Flow")
    print("=" * 50)
    
    try:
        # 1. Test registration
        print("1. Testing registration...")
        get_response = session.get(f"{base_url}/register/")
        if get_response.status_code != 200:
            print(f"❌ Registration page failed: {get_response.status_code}")
            return
        
        # Extract CSRF token
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', get_response.text)
        if not csrf_match:
            print("❌ CSRF token not found")
            return
        
        csrf_token = csrf_match.group(1)
        print("✅ CSRF token found")
        
        # Registration data
        import time
        timestamp = str(int(time.time()))
        reg_data = {
            'csrfmiddlewaretoken': csrf_token,
            'username': f'testuser{timestamp}',
            'email': f'test{timestamp}@example.com',
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
        
        # Submit registration
        reg_response = session.post(f"{base_url}/register/", data=reg_data)
        print(f"Registration response: {reg_response.status_code}")
        
        if reg_response.status_code == 302:
            print("✅ Registration successful (redirect)")
            # Check if we're redirected to dashboard
            if 'dashboard' in reg_response.headers.get('Location', ''):
                print("✅ Redirected to dashboard")
            else:
                print(f"⚠️  Redirected to: {reg_response.headers.get('Location', 'Unknown')}")
        elif reg_response.status_code == 200:
            if "error" in reg_response.text.lower():
                print("⚠️  Registration failed with errors")
                # Print the first 500 characters of the response to see the errors
                print("Response preview:", reg_response.text[:500])
            else:
                print("✅ Registration completed without redirect")
        else:
            print(f"❌ Registration failed: {reg_response.status_code}")
            return
        
        # 2. Test dashboard access
        print("\n2. Testing dashboard access...")
        dashboard_response = session.get(f"{base_url}/dashboard/")
        print(f"Dashboard response: {dashboard_response.status_code}")
        
        if dashboard_response.status_code == 200:
            print("✅ Dashboard accessible")
        elif dashboard_response.status_code == 302:
            print("⚠️  Dashboard redirected (might need login)")
        else:
            print(f"❌ Dashboard failed: {dashboard_response.status_code}")
        
        # 3. Test login
        print("\n3. Testing login...")
        login_response = session.get(f"{base_url}/login/")
        if login_response.status_code != 200:
            print(f"❌ Login page failed: {login_response.status_code}")
            return
        
        # Extract CSRF token for login
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', login_response.text)
        if not csrf_match:
            print("❌ CSRF token not found for login")
            return
        
        csrf_token = csrf_match.group(1)
        
        # Login data
        login_data = {
            'csrfmiddlewaretoken': csrf_token,
            'username': f'testuser{timestamp}',
            'password': 'testpassword123'
        }
        
        # Submit login
        login_response = session.post(f"{base_url}/login/", data=login_data)
        print(f"Login response: {login_response.status_code}")
        
        if login_response.status_code == 302:
            print("✅ Login successful (redirect)")
        elif login_response.status_code == 200:
            if "error" in login_response.text.lower():
                print("⚠️  Login failed with errors")
            else:
                print("✅ Login completed without redirect")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            return
        
        # 4. Test dashboard after login
        print("\n4. Testing dashboard after login...")
        dashboard_response = session.get(f"{base_url}/dashboard/")
        print(f"Dashboard response after login: {dashboard_response.status_code}")
        
        if dashboard_response.status_code == 200:
            print("✅ Dashboard accessible after login")
        else:
            print(f"❌ Dashboard still not accessible: {dashboard_response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_auth_flow()

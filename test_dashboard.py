#!/usr/bin/env python3
"""
Test dashboard functionality
"""

import requests
import re

def test_dashboard():
    """Test dashboard access"""
    base_url = "http://localhost:8000"
    session = requests.Session()
    
    print("🧪 Testing Dashboard Functionality")
    print("=" * 50)
    
    try:
        # 1. First login
        print("1. Logging in...")
        login_response = session.get(f"{base_url}/login/")
        if login_response.status_code != 200:
            print(f"❌ Login page failed: {login_response.status_code}")
            return
        
        # Extract CSRF token
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', login_response.text)
        if not csrf_match:
            print("❌ CSRF token not found")
            return
        
        csrf_token = csrf_match.group(1)
        
        # Login with existing user
        login_data = {
            'csrfmiddlewaretoken': csrf_token,
            'username': 'testuser',
            'password': 'testpassword123'
        }
        
        login_response = session.post(f"{base_url}/login/", data=login_data)
        print(f"Login response: {login_response.status_code}")
        
        if login_response.status_code == 302:
            print("✅ Login successful (redirect)")
        elif login_response.status_code == 200:
            if "error" in login_response.text.lower():
                print("⚠️  Login failed with errors")
                return
            else:
                print("✅ Login completed")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            return
        
        # 2. Test dashboard access
        print("\n2. Testing dashboard access...")
        dashboard_response = session.get(f"{base_url}/dashboard/")
        print(f"Dashboard response: {dashboard_response.status_code}")
        
        if dashboard_response.status_code == 200:
            print("✅ Dashboard accessible")
            
            # Check if the new features are present
            if "sidebar-toggle" in dashboard_response.text:
                print("✅ Hamburger menu button found")
            else:
                print("❌ Hamburger menu button not found")
                
            if "testSOS()" in dashboard_response.text:
                print("✅ Test SOS button function found")
            else:
                print("❌ Test SOS button function not found")
                
            if "updateLocation()" in dashboard_response.text:
                print("✅ Update Location button function found")
            else:
                print("❌ Update Location button function not found")
                
        else:
            print(f"❌ Dashboard failed: {dashboard_response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_dashboard()

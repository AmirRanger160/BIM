#!/usr/bin/env python3
import requests
import json

# First, login as admin
print("=" * 50)
print("Step 1: Admin Login")
print("=" * 50)

login_data = {
    "username": "admin",
    "password": "admin123"
}

try:
    response = requests.post('http://localhost:8000/api/auth/login', json=login_data)
    print(f"Status: {response.status_code}")
    response_data = response.json()
    print(json.dumps(response_data, indent=2, ensure_ascii=False))
    
    if response.status_code == 200:
        token = response_data.get('access_token')
        print(f"\n✅ Token received: {token[:30]}...")
        
        # Now test getting submissions
        print("\n" + "=" * 50)
        print("Step 2: Get Contact Submissions (Admin)")
        print("=" * 50)
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get('http://localhost:8000/api/contact/admin/contact-submissions', headers=headers)
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
except Exception as e:
    print(f"Error: {e}")

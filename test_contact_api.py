#!/usr/bin/env python3
import requests
import json

# Test 1: Get company info
print("=" * 50)
print("Test 1: GET /api/contact/company-info")
print("=" * 50)
try:
    response = requests.get('http://localhost:8000/api/contact/company-info')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Connection error: {e}")

print("\n" + "=" * 50)
print("Test 2: POST /api/contact (submit form)")
print("=" * 50)

data = {
    "name": "علی رضایی",
    "phone": "09123456789",
    "email": "ali@example.com",
    "message": "این یک پیام تست برای بررسی سیستم ادمین است"
}

try:
    response = requests.post('http://localhost:8000/api/contact', json=data)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")

#!/usr/bin/env python3
"""Test articles API endpoint"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

print("Testing Articles API...")
print("-" * 50)

# Test 1: Get all articles
print("\n1. GET /articles")
try:
    response = requests.get(f"{BASE_URL}/articles", params={"skip": 0, "limit": 100})
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Got {len(data)} articles")
        if data:
            print(f"  Sample: {data[0]['title_en']}")
    else:
        print(f"✗ Error: {response.text}")
except Exception as e:
    print(f"✗ Exception: {e}")

# Test 2: Get articles with small limit
print("\n2. GET /articles (limit=10)")
try:
    response = requests.get(f"{BASE_URL}/articles", params={"skip": 0, "limit": 10})
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Got {len(data)} articles")
    else:
        print(f"✗ Error: {response.text}")
except Exception as e:
    print(f"✗ Exception: {e}")

# Test 3: Seed demo articles
print("\n3. POST /articles/seed-demo")
try:
    response = requests.post(f"{BASE_URL}/articles/seed-demo")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ {data.get('message', 'Success')}")
    else:
        print(f"✗ Error: {response.text}")
except Exception as e:
    print(f"✗ Exception: {e}")

print("\n" + "-" * 50)
print("Tests completed!")

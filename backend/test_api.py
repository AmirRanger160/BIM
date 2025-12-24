#!/usr/bin/env python3
"""
GeoBiro Backend - Test Examples
Run these examples to test the API locally
"""

import requests
import json
from typing import Optional

API_URL = "http://localhost:8000/api"

# Store token for admin requests
TOKEN = None


def print_response(title: str, response: requests.Response, print_json: bool = True):
    """Print formatted response."""
    print(f"\n{'='*60}")
    print(f"📡 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    if print_json:
        try:
            print(json.dumps(response.json(), indent=2, default=str))
        except:
            print(response.text)
    else:
        print(response.text)


def test_health_check():
    """Test health check endpoint."""
    response = requests.get(f"{API_URL.replace('/api', '')}/health")
    print_response("Health Check", response)


def test_register():
    """Register new admin user."""
    payload = {
        "username": "admin_user",
        "email": "admin@geobiro.ba",
        "password": "AdminPassword123"
    }
    response = requests.post(f"{API_URL}/auth/register", json=payload)
    print_response("Register Admin User", response)
    
    # Extract token
    if response.status_code == 201:
        global TOKEN
        TOKEN = response.json().get("access_token")
        print(f"\n✅ Token saved: {TOKEN[:50]}...")


def test_login():
    """Login with credentials."""
    payload = {
        "username": "admin_user",
        "password": "AdminPassword123"
    }
    response = requests.post(f"{API_URL}/auth/login", json=payload)
    print_response("Login", response)
    
    if response.status_code == 200:
        global TOKEN
        TOKEN = response.json().get("access_token")
        print(f"\n✅ Token saved: {TOKEN[:50]}...")


def test_get_current_user():
    """Get current authenticated user."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{API_URL}/auth/me", headers=headers)
    print_response("Get Current User", response)


def test_get_services():
    """Get all services."""
    response = requests.get(f"{API_URL}/services")
    print_response("Get All Services", response)


def test_get_services_by_category():
    """Get services filtered by category."""
    response = requests.get(f"{API_URL}/services?category=BIM")
    print_response("Get BIM Services", response)


def test_create_service():
    """Create a new service."""
    payload = {
        "title": "Advanced 3D Modeling",
        "description": "High-precision 3D modeling using latest technology and software.",
        "category": "BIM",
        "image_url": "https://example.com/3d-modeling.jpg",
        "software_tools": "Revit, AutoCAD, SketchUp"
    }
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.post(f"{API_URL}/services", json=payload, headers=headers)
    print_response("Create Service", response)


def test_get_team_members():
    """Get all team members."""
    response = requests.get(f"{API_URL}/team")
    print_response("Get Team Members", response)


def test_create_team_member():
    """Create a new team member."""
    payload = {
        "name_en": "John Smith",
        "name_fa": "جان اسمیت",
        "position_en": "Senior Surveyor",
        "position_fa": "نقشه بردار ارشد",
        "email": "john.smith@geobiro.ba",
        "phone": "+387 61 234 567",
        "bio_en": "15+ years of experience in surveying and mapping.",
        "bio_fa": "بیش از 15 سال تجربه در نقشه برداری و رسم نقشه."
    }
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.post(f"{API_URL}/team", json=payload, headers=headers)
    print_response("Create Team Member", response)


def test_get_certificates():
    """Get all certificates."""
    response = requests.get(f"{API_URL}/certificates")
    print_response("Get Certificates", response)


def test_create_certificate():
    """Create a new certificate."""
    payload = {
        "title_en": "ISO 9001:2015 Certification",
        "title_fa": "گواهی ISO 9001:2015",
        "description_en": "Quality Management System Certification",
        "description_fa": "گواهی سیستم مدیریت کیفیت",
        "image_url": "https://example.com/iso-cert.jpg",
        "issue_date": "2023-01-15",
        "expiry_date": "2026-01-15"
    }
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.post(f"{API_URL}/certificates", json=payload, headers=headers)
    print_response("Create Certificate", response)


def test_get_licenses():
    """Get all licenses."""
    response = requests.get(f"{API_URL}/licenses")
    print_response("Get Licenses", response)


def test_create_license():
    """Create a new license."""
    payload = {
        "title_en": "Geodetic Work License",
        "title_fa": "مجوز کار ژئودتیکی",
        "description_en": "Government license for geodetic work and surveying",
        "description_fa": "مجوز دولتی برای کار ژئودتیکی و نقشه برداری",
        "image_url": "https://example.com/geodetic-license.jpg",
        "issue_date": "2022-06-01",
        "issue_authority": "Ministry of Urban Development"
    }
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.post(f"{API_URL}/licenses", json=payload, headers=headers)
    print_response("Create License", response)


def test_submit_contact_form():
    """Submit contact form."""
    payload = {
        "name": "Ahmed Hassan",
        "phone": "+387 61 543 210",
        "email": "ahmed@example.com",
        "message": "I would like to inquire about your 3D modeling services for our new construction project. Please contact me with pricing information."
    }
    response = requests.post(f"{API_URL}/contact", json=payload)
    print_response("Submit Contact Form", response)


def test_get_contact_submissions():
    """Get all contact submissions (admin)."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{API_URL}/admin/contact-submissions", headers=headers)
    print_response("Get Contact Submissions", response)


def test_update_submission_status():
    """Update contact submission status (admin)."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {"status_value": "read"}
    response = requests.patch(
        f"{API_URL}/admin/contact-submissions/1/status",
        json=payload,
        headers=headers
    )
    print_response("Update Submission Status", response)


def test_get_company_info():
    """Get company information."""
    response = requests.get(f"{API_URL}/company-info")
    print_response("Get Company Info", response)


def test_update_company_info():
    """Update company information (admin)."""
    payload = {
        "name": "GeoBiro d.o.o.",
        "description_en": "Leading provider of geospatial solutions and BIM services in Bosnia and Herzegovina since 1991.",
        "description_fa": "تامین کننده پیشرو خدمات جغرافیایی و خدمات BIM در بوسنی و هرزگوین از سال 1991.",
        "founded_year": 1991,
        "headquarters_location": "Plehej 2A, Konick 88400",
        "phone": "+387 61 542 490",
        "email": "info@geobiro.ba",
        "address_city": "Konick",
        "address_country": "Bosnia and Herzegovina",
        "total_employees": 95
    }
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.put(f"{API_URL}/admin/company-info", json=payload, headers=headers)
    print_response("Update Company Info", response)


def test_get_statistics():
    """Get statistics."""
    response = requests.get(f"{API_URL}/statistics")
    print_response("Get Statistics", response)


def test_update_statistics():
    """Update statistics (admin)."""
    payload = {
        "annual_projects": 1200,
        "service_types": 9,
        "employees": 95,
        "satisfied_clients": 120
    }
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.put(f"{API_URL}/admin/statistics", json=payload, headers=headers)
    print_response("Update Statistics", response)


def test_error_handling():
    """Test error handling - invalid request."""
    payload = {
        "title": "Invalid Service",
        # Missing required fields
    }
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.post(f"{API_URL}/services", json=payload, headers=headers)
    print_response("Error Handling - Invalid Request", response)


def test_unauthorized():
    """Test unauthorized access."""
    response = requests.get(f"{API_URL}/admin/contact-submissions")
    print_response("Error Handling - Unauthorized", response)


def run_full_test_suite():
    """Run all tests in sequence."""
    print("\n🚀 GeoBiro Backend - Full Test Suite")
    print("=" * 60)
    print("Starting tests... Make sure backend is running!")
    print(f"API URL: {API_URL}")
    
    tests = [
        ("Health Check", test_health_check),
        ("Register Admin", test_register),
        ("Login", test_login),
        ("Get Current User", test_get_current_user),
        ("Get Services", test_get_services),
        ("Get Services by Category", test_get_services_by_category),
        ("Create Service", test_create_service),
        ("Get Team Members", test_get_team_members),
        ("Create Team Member", test_create_team_member),
        ("Get Certificates", test_get_certificates),
        ("Create Certificate", test_create_certificate),
        ("Get Licenses", test_get_licenses),
        ("Create License", test_create_license),
        ("Submit Contact Form", test_submit_contact_form),
        ("Get Contact Submissions", test_get_contact_submissions),
        ("Update Submission Status", test_update_submission_status),
        ("Get Company Info", test_get_company_info),
        ("Update Company Info", test_update_company_info),
        ("Get Statistics", test_get_statistics),
        ("Update Statistics", test_update_statistics),
        ("Test Error Handling", test_error_handling),
        ("Test Unauthorized", test_unauthorized),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ {name} FAILED: {str(e)}")
            failed += 1
    
    # Summary
    print(f"\n\n{'='*60}")
    print(f"✅ Test Summary")
    print(f"{'='*60}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {len(tests)}")
    
    if failed == 0:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {failed} test(s) failed")


if __name__ == "__main__":
    # Run individual tests or full suite
    import sys
    
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        if test_name == "all":
            run_full_test_suite()
        else:
            # Run specific test by name
            test_func = globals().get(f"test_{test_name}")
            if test_func:
                test_func()
            else:
                print(f"Test '{test_name}' not found")
    else:
        # Default: run full suite
        run_full_test_suite()

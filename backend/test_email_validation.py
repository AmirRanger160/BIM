#!/usr/bin/env python3
"""
Quick test to verify email validation works with .test domains
"""

import sys
sys.path.insert(0, '/home/unique/projects/BIM/backend')

from app.schemas.schemas import UserCreate, ContactSubmissionCreate, TeamMemberCreate

def test_user_with_test_domain():
    """Test creating a user with .test domain email."""
    try:
        user = UserCreate(
            username="admin",
            email="admin@bim.test",
            password="TestPassword123"
        )
        print("✅ UserCreate with admin@bim.test: PASSED")
        print(f"   User created: {user.username}, {user.email}")
        return True
    except Exception as e:
        print(f"❌ UserCreate with admin@bim.test: FAILED")
        print(f"   Error: {e}")
        return False


def test_user_with_valid_domain():
    """Test creating a user with valid domain."""
    try:
        user = UserCreate(
            username="testuser",
            email="test@example.com",
            password="TestPassword123"
        )
        print("✅ UserCreate with test@example.com: PASSED")
        print(f"   User created: {user.username}, {user.email}")
        return True
    except Exception as e:
        print(f"❌ UserCreate with test@example.com: FAILED")
        print(f"   Error: {e}")
        return False


def test_contact_with_test_domain():
    """Test creating a contact with .test domain email."""
    try:
        contact = ContactSubmissionCreate(
            name="Test User",
            email="user@bim.test",
            phone="1234567890",
            message="This is a test message with more than 10 characters"
        )
        print("✅ ContactSubmissionCreate with user@bim.test: PASSED")
        print(f"   Contact created: {contact.name}, {contact.email}")
        return True
    except Exception as e:
        print(f"❌ ContactSubmissionCreate with user@bim.test: FAILED")
        print(f"   Error: {e}")
        return False


def test_invalid_email():
    """Test that invalid emails are still rejected."""
    try:
        user = UserCreate(
            username="testuser",
            email="invalid-email",
            password="TestPassword123"
        )
        print("❌ UserCreate with invalid-email: FAILED (should have been rejected)")
        return False
    except Exception as e:
        print(f"✅ UserCreate with invalid-email: PASSED (correctly rejected)")
        print(f"   Error: {e}")
        return True


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Email Validation with .test Domain Support")
    print("=" * 60)
    print()
    
    results = []
    results.append(test_user_with_test_domain())
    results.append(test_user_with_valid_domain())
    results.append(test_contact_with_test_domain())
    results.append(test_invalid_email())
    
    print()
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    sys.exit(0 if all(results) else 1)

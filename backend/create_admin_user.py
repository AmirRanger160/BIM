#!/usr/bin/env python
"""
Script to create an admin test user for the BIM project.
Usage: python create_admin_user.py
"""

import sys
from sqlalchemy.orm import Session
from app.models.models import User, Base
from app.database import engine, SessionLocal
from app.core.security import hash_password


def create_admin_user():
    """Create a test admin user."""
    # Ensure all tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.username == "adminn").first()
        if admin_user:
            print(f"✓ Admin user already exists: {admin_user.username} ({admin_user.email})")
            return admin_user
        
        # Create new admin user
        test_admin = User(
            username="adminn",
            email="admin@gmail.local",
            hashed_password=hash_password("admin123"),
            is_admin=True,
            is_active=True
        )
        
        db.add(test_admin)
        db.commit()
        db.refresh(test_admin)
        
        print("\n✓ Admin user created successfully!")
        print(f"  Username: {test_admin.username}")
        print(f"  Email: {test_admin.email}")
        print(f"  Password: admin123")
        print(f"  Admin: {test_admin.is_admin}")
        print(f"  Active: {test_admin.is_active}")
        print(f"  Created at: {test_admin.created_at}\n")
        
        return test_admin
        
    except Exception as e:
        print(f"✗ Error creating admin user: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_user()
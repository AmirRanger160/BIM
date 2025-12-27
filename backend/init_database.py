#!/usr/bin/env python3
"""
Initialize database with all required tables.
This script will:
1. Create all tables from models if they don't exist
2. Apply any necessary migrations
"""

import sys
sys.path.insert(0, '/home/unique/projects/BIM/backend')

from app.database import engine
from app.models.models import Base

def init_database():
    """Initialize the database with all tables."""
    print("🔄 Initializing database...")
    
    try:
        # Create all tables based on models
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created/verified successfully")
        
        # List all tables
        inspector = __import__('sqlalchemy').inspect(engine)
        tables = inspector.get_table_names()
        print(f"\n✓ Available tables: {tables}")
        
        # Check services table structure
        if 'services' in tables:
            columns = [col['name'] for col in inspector.get_columns('services')]
            print(f"\n✓ Services table columns: {columns}")
            
            # Verify required columns
            required_columns = ['id', 'title', 'title_en', 'title_fa', 'description', 
                              'description_en', 'description_fa', 'category']
            missing = [col for col in required_columns if col not in columns]
            if missing:
                print(f"✗ Missing columns in services: {missing}")
                return False
            else:
                print("✓ All required columns are present in services table")
        
        return True
        
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)

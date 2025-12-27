#!/usr/bin/env python3
"""
Migration script to add bilingual fields (title_en, title_fa, description_en, description_fa)
to the services table if they don't exist.
"""

from sqlalchemy import inspect, text
from app.database import engine

def migrate_services_table():
    """Add missing columns to services table."""
    
    # Get the inspector to check existing columns
    inspector = inspect(engine)
    
    # Get existing columns in services table
    try:
        existing_columns = [col['name'] for col in inspector.get_columns('services')]
    except Exception as e:
        print(f"✗ Error reading existing columns: {e}")
        print("Creating tables from scratch...")
        from app.models.models import Base
        Base.metadata.create_all(bind=engine)
        return
    
    print(f"Existing columns in 'services' table: {existing_columns}")
    
    # List of columns to add with their SQL definitions
    columns_to_add = [
        ('title_en', 'VARCHAR(255)'),
        ('title_fa', 'VARCHAR(255)'),
        ('description_en', 'TEXT'),
        ('description_fa', 'TEXT'),
    ]
    
    # Check which columns are missing and add them
    with engine.begin() as conn:
        for col_name, col_type in columns_to_add:
            if col_name not in existing_columns:
                print(f"Adding column '{col_name}' to services table...")
                try:
                    # Use raw SQL for better compatibility across different databases
                    sql = f"ALTER TABLE services ADD COLUMN {col_name} {col_type} NULL"
                    conn.execute(text(sql))
                    print(f"✓ Column '{col_name}' added successfully")
                except Exception as e:
                    print(f"✗ Error adding column '{col_name}': {e}")
            else:
                print(f"✓ Column '{col_name}' already exists")
    
    print("\nMigration completed!")

if __name__ == "__main__":
    migrate_services_table()

#!/usr/bin/env python3
"""
Migration script to add article_images table to the database.
Run this if you have an existing database and want to add image support.

Usage:
    python backend/migrate_add_article_images.py
"""

import sqlite3
from pathlib import Path

def migrate():
    # Find database file
    db_path = Path(__file__).parent / 'app.db'
    
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        print("Please ensure the database exists or create it by running the app first.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table already exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='article_images'
        """)
        
        if cursor.fetchone():
            print("✓ Table 'article_images' already exists.")
            conn.close()
            return True
        
        # Create the article_images table
        cursor.execute("""
            CREATE TABLE article_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER NOT NULL,
                image_url VARCHAR(500) NOT NULL,
                caption_en TEXT,
                caption_fa TEXT,
                alt_text_en VARCHAR(500),
                alt_text_fa VARCHAR(500),
                "order" INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes for better query performance
        cursor.execute("""
            CREATE INDEX idx_article_images_article_id 
            ON article_images(article_id)
        """)
        
        cursor.execute("""
            CREATE INDEX idx_article_images_created_at 
            ON article_images(created_at)
        """)
        
        conn.commit()
        print("✓ Successfully created 'article_images' table")
        print("✓ Created indexes for better performance")
        
        # Verify the table was created
        cursor.execute("""
            SELECT sql FROM sqlite_master 
            WHERE type='table' AND name='article_images'
        """)
        schema = cursor.fetchone()
        if schema:
            print("\n📋 Table Schema:")
            print(schema[0])
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Running migration: Add article_images table...")
    print("-" * 50)
    
    if migrate():
        print("-" * 50)
        print("✅ Migration completed successfully!")
    else:
        print("-" * 50)
        print("❌ Migration failed!")

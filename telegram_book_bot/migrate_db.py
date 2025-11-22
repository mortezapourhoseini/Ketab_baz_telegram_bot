#!/usr/bin/env python3
"""
Database migration script to add enhanced profile fields
"""

import sqlite3

def migrate_database():
    """Add new columns for enhanced user profiling"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Add new columns to users table
    new_columns = [
        ("reading_speed", "TEXT"),  # سریع، متوسط، آهسته
        ("book_length_preference", "TEXT"),  # کوتاه، متوسط، بلند
        ("reading_purpose", "TEXT"),  # تفریح، یادگیری، کار، مطالعه
        ("favorite_authors", "TEXT"),  # Comma-separated list
        ("disliked_genres", "TEXT"),  # Comma-separated list
        ("preferred_era", "TEXT"),  # کلاسیک، معاصر، مدرن، همه
        ("complexity_level", "TEXT"),  # ساده، متوسط، پیچیده
        ("book_format_preference", "TEXT"),  # رمان، داستان کوتاه، مقاله، شعر
    ]
    
    for column_name, column_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}")
            print(f"✓ Added column: {column_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f"  Column {column_name} already exists")
            else:
                print(f"✗ Error adding {column_name}: {e}")
    
    conn.commit()
    conn.close()
    print("\n✅ Database migration completed!")

if __name__ == "__main__":
    migrate_database()

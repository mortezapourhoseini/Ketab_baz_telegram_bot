#!/usr/bin/env python3
"""
Simple test script to check Ganjoor API integration
"""

import requests
import random

GANJOOR_API_URL = "https://api.ganjoor.net/api/ganjoor"

def test_ganjoor_api():
    """Test the Ganjoor API"""
    print("=" * 60)
    print("Testing Ganjoor API Integration")
    print("=" * 60)
    print()
    
    try:
        # Get list of poets
        print("📚 Fetching Persian poets from Ganjoor...")
        response = requests.get(f'{GANJOOR_API_URL}/poets')
        response.raise_for_status()
        poets = response.json()
        
        print(f"✓ Found {len(poets)} Persian poets")
        print()
        
        # Show some famous poets
        famous_poets = ['حافظ', 'سعدی', 'فردوسی', 'مولانا', 'خیام']
        print("🌟 Some famous poets in the database:")
        for poet in poets[:10]:  # Show first 10
            name = poet.get('name', 'Unknown')
            if any(famous in name for famous in famous_poets):
                print(f"   ⭐ {name}")
            else:
                print(f"   - {name}")
        
        print()
        
        # Test getting a random poet's works
        selected_poet = random.choice(poets)
        poet_name = selected_poet.get('name', 'Unknown')
        poet_url = selected_poet.get('fullUrl', '')
        
        print(f"📖 Testing with poet: {poet_name}")
        print(f"   URL: {poet_url}")
        print()
        
        if poet_url:
            # Get poet's works
            cat_response = requests.get(f'{GANJOOR_API_URL}/poet{poet_url}')
            cat_response.raise_for_status()
            poet_data = cat_response.json()
            
            cat = poet_data.get('cat')
            if cat:
                poet_full_name = cat.get('poet', {}).get('name', poet_name)
                print(f"✓ Poet: {poet_full_name}")
                
                children = cat.get('children', [])
                if children:
                    print(f"✓ Found {len(children)} collections/books")
                    print()
                    print("📚 Collections:")
                    for child in children[:5]:  # Show first 5
                        title = child.get('title', 'Unknown')
                        poem_count = child.get('poemCount', 0)
                        print(f"   - {title} ({poem_count} poems)")
                    
                    # Try to get a poem
                    selected_cat = random.choice(children)
                    cat_id = selected_cat.get('id')
                    cat_title = selected_cat.get('title', 'Unknown')
                    
                    print()
                    print(f"🔍 Getting poems from: {cat_title}")
                    
                    try:
                        poems_response = requests.get(f'{GANJOOR_API_URL}/cat/{cat_id}/poems')
                        poems_response.raise_for_status()
                        poems_data = poems_response.json()
                        poems = poems_data.get('poems', [])
                        
                        if poems:
                            print(f"✓ Found {len(poems)} poems")
                            selected_poem = random.choice(poems)
                            poem_title = selected_poem.get('title', 'Unknown')
                            poem_excerpt = selected_poem.get('excerpt', '')
                            
                            print()
                            print("🌟 Sample Poem:")
                            print(f"   Title: {poem_title}")
                            if poem_excerpt:
                                print(f"   Excerpt: {poem_excerpt[:150]}...")
                    except Exception as e:
                        print(f"   ⚠️ Could not fetch poems: {e}")
        
        print()
        print("=" * 60)
        print("✅ Ganjoor API test completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("=" * 60)

if __name__ == "__main__":
    test_ganjoor_api()

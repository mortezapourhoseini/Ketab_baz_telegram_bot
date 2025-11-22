#!/usr/bin/env python3
# Test script to verify the verse fetching functionality

import requests

GANJOOR_API_URL = "https://api.ganjoor.net/api/ganjoor"

def test_poem_verses():
    """Test fetching poem with verses from Ganjoor API"""
    print("🧪 Testing Ganjoor API - Fetching poem with verses...\n")
    
    # Get a random poem
    response = requests.get(f'{GANJOOR_API_URL}/poem/random')
    if response.status_code == 200:
        poem = response.json()
        
        print(f"✅ Successfully fetched poem!")
        print(f"📖 Title: {poem.get('title', 'N/A')}")
        print(f"🔗 URL: {poem.get('fullUrl', 'N/A')}")
        print(f"\n🌟 First few verses:")
        print("-" * 50)
        
        verses = poem.get('verses', [])
        if verses:
            # Display first 4 verses (2 couplets)
            for verse in verses[:4]:
                print(verse.get('text', ''))
            print("-" * 50)
            print(f"\n✅ Total verses available: {len(verses)}")
        else:
            print("❌ No verses found")
    else:
        print(f"❌ Error: Status code {response.status_code}")

if __name__ == "__main__":
    test_poem_verses()

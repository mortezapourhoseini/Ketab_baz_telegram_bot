#!/usr/bin/env python3
"""
Test script for BigBookAPI integration
"""

import requests
import json

BIGBOOK_API_KEY = "db8b50a0f9684e5e8d93de43a50701be"
BIGBOOK_API_URL = "https://api.bigbookapi.com"

def test_bigbook_api():
    """Test BigBookAPI endpoints"""
    print("=" * 60)
    print("Testing BigBookAPI")
    print("=" * 60)
    print()
    
    # Test different endpoints based on common API patterns
    endpoints_to_test = [
        f"{BIGBOOK_API_URL}?api-key={BIGBOOK_API_KEY}&number=5",
        f"{BIGBOOK_API_URL}/search-books?api-key={BIGBOOK_API_KEY}&number=5",
        f"{BIGBOOK_API_URL}/search-books?api-key={BIGBOOK_API_KEY}&query=fiction&number=5",
        f"{BIGBOOK_API_URL}/books?api-key={BIGBOOK_API_KEY}&number=5",
        f"{BIGBOOK_API_URL}/v1/books?api-key={BIGBOOK_API_KEY}&number=5",
    ]
    
    for i, url in enumerate(endpoints_to_test, 1):
        print(f"Test {i}: {url[:80]}...")
        try:
            response = requests.get(url, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✓ JSON Response received")
                    print(f"   Response keys: {list(data.keys()) if isinstance(data, dict) else 'List response'}")
                    print(f"   Response preview: {json.dumps(data, indent=2)[:500]}...")
                    print()
                    break  # Found working endpoint
                except:
                    print(f"   ✗ Not JSON: {response.text[:200]}")
            else:
                print(f"   ✗ Error: {response.text[:200]}")
        except Exception as e:
            print(f"   ✗ Exception: {e}")
        print()
    
    print("=" * 60)

if __name__ == "__main__":
    test_bigbook_api()

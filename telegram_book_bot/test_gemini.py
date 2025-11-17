#!/usr/bin/env python3
"""
Simple test script to check Gemini API functionality
"""

from gemini_api import get_gemini_suggestion
from config import GEMINI_API_KEY

def test_gemini_model():
    """Test the Gemini model with a simple prompt"""
    print("=" * 50)
    print("Testing Gemini API Model")
    print("=" * 50)
    
    # Check if API key is configured
    if not GEMINI_API_KEY:
        print("❌ Error: GEMINI_API_KEY is not configured in config.py")
        return
    
    print(f"✓ API Key found: {GEMINI_API_KEY[:10]}...")
    print()
    
    # Test prompt
    test_prompt = "Hello! Please introduce yourself in one sentence."
    
    print(f"📝 Test Prompt: {test_prompt}")
    print()
    print("🤖 Model Response:")
    print("-" * 50)
    
    try:
        response = get_gemini_suggestion(test_prompt)
        
        if response:
            print(response)
            print("-" * 50)
            print()
            print("✅ Test completed successfully!")
        else:
            print("❌ No response received from the model")
            
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print("-" * 50)
    
    print()
    print("=" * 50)

if __name__ == "__main__":
    test_gemini_model()

# Utility functions: language detection, safety checks, Persian support
import re

def is_persian(text):
    # Checks if text contains Persian characters
    return bool(re.search(r'[\u0600-\u06FF]', text))

def is_safe_message(text):
    # Basic safety check for prompt injection/disrespect
    forbidden = ['prompt injection', 'infiltration', 'hack', 'attack', 'disrespect']
    for word in forbidden:
        if word in text.lower():
            return False
    # Add more checks as needed
    return True

def redirect_to_main_topic():
    return "لطفا به بحث کتاب‌ها و سوالات ربات بازگردید."

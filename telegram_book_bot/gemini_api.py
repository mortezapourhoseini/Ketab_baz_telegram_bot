# Gemini language model API integration

from config import GEMINI_API_KEY
from google import genai

class GeminiAPI:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def ask_question(self, user_id, question):
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=question
            )
            return getattr(response, 'text', "پاسخی دریافت نشد.")
        except Exception as e:
            return f"خطا در ارتباط با مدل: {e}"

def get_gemini_suggestion(prompt):
    client = genai.Client(api_key=GEMINI_API_KEY)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        return getattr(response, 'text', "پاسخی دریافت نشد.")
    except Exception as e:
        return f"خطا: {e}"


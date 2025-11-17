# Book recommendation logic using Google Books API
import requests
from config import BOOK_API_URL, LANGUAGE
from user import UserManager

class BookRecommender:
    def __init__(self):
        self.user_manager = UserManager()
    def recommend_book(self, telegram_id):
        profile = self.user_manager.get_profile(telegram_id)
        params = {
            'q': profile or 'کتاب',
            'langRestrict': LANGUAGE,
            'maxResults': 1
        }
        response = requests.get(BOOK_API_URL, params=params)
        if response.status_code == 200:
            items = response.json().get('items', [])
            if items:
                book = items[0]['volumeInfo']
                title = book.get('title', 'بدون عنوان')
                authors = ', '.join(book.get('authors', []))
                return f"{title} توسط {authors}"
        return "متاسفم، کتابی پیدا نشد."

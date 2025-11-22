#!/usr/bin/env python3
"""
BigBookAPI integration for advanced book recommendations
"""

import requests
import random
from config import BIGBOOK_API_KEY, BIGBOOK_API_URL

def get_bigbook_recommendation(user_profile, read_books=None, recommended_books=None):
    """
    Get advanced book recommendation from BigBookAPI based on detailed user profile
    
    Args:
        user_profile: Dict with user preferences
        read_books: List of already read books
        recommended_books: List of already recommended books
    
    Returns:
        Dict with book info or None if failed
    """
    try:
        # Extract user preferences
        genres = user_profile.get('genres', [])
        age = user_profile.get('age', 30)
        reading_speed = user_profile.get('reading_speed', 'متوسط')
        book_length = user_profile.get('book_length_preference', 'متوسط')
        complexity = user_profile.get('complexity_level', 'متوسط')
        preferred_era = user_profile.get('preferred_era', 'همه')
        
        # Build query parameters
        params = {
            'api-key': BIGBOOK_API_KEY,
            'number': 20,  # Get more options to filter
        }
        
        # Add genre/subject filter if available
        if genres:
            # Use first genre as primary filter
            genre = random.choice(genres)
            params['query'] = genre
        
        # Add year filter based on preferred era
        if preferred_era == 'کلاسیک':
            params['max-year'] = 1950
        elif preferred_era == 'معاصر':
            params['min-year'] = 1950
            params['max-year'] = 2000
        elif preferred_era == 'مدرن':
            params['min-year'] = 2000
        
        # Make API request
        url = f"{BIGBOOK_API_URL}/search-books"
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        books = data.get('books', [])
        if not books:
            return None
        
        # Filter and process books
        excluded_titles = set()
        if read_books:
            excluded_titles.update(b[0].lower() for b in read_books if b[0])
        if recommended_books:
            excluded_titles.update(b[0].lower() for b in recommended_books if b[0])
        
        # Find suitable book
        for book_data in books:
            if not book_data or not isinstance(book_data, list) or not book_data[0]:
                continue
            
            book = book_data[0]
            title = book.get('title', '').strip()
            
            if not title or title.lower() in excluded_titles:
                continue
            
            # Extract book information
            authors = book.get('authors', [])
            author_name = authors[0].get('name', 'Unknown') if authors else 'Unknown'
            image_url = book.get('image', '')
            subtitle = book.get('subtitle', '')
            book_id = book.get('id', '')
            
            # Get publication year if available (would need another API call)
            year = 'نامشخص'
            
            return {
                'title': title,
                'subtitle': subtitle,
                'author': author_name,
                'year': year,
                'image': image_url,
                'id': book_id,
                'source': 'BigBookAPI'
            }
        
        # If no suitable book found, return first one
        if books and books[0] and isinstance(books[0], list) and books[0][0]:
            book = books[0][0]
            title = book.get('title', 'No title')
            authors = book.get('authors', [])
            author_name = authors[0].get('name', 'Unknown') if authors else 'Unknown'
            image_url = book.get('image', '')
            subtitle = book.get('subtitle', '')
            book_id = book.get('id', '')
            
            return {
                'title': title,
                'subtitle': subtitle,
                'author': author_name,
                'year': 'نامشخص',
                'image': image_url,
                'id': book_id,
                'source': 'BigBookAPI'
            }
        
        return None
        
    except Exception as e:
        print(f"BigBookAPI error: {e}")
        return None

def search_books_by_author(author_name, limit=10):
    """Search books by specific author"""
    try:
        params = {
            'api-key': BIGBOOK_API_KEY,
            'query': author_name,
            'number': limit
        }
        
        url = f"{BIGBOOK_API_URL}/search-books"
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        books = data.get('books', [])
        results = []
        
        for book_data in books:
            if not book_data or not isinstance(book_data, list) or not book_data[0]:
                continue
            
            book = book_data[0]
            authors = book.get('authors', [])
            
            # Check if author matches
            for author in authors:
                if author_name.lower() in author.get('name', '').lower():
                    results.append({
                        'title': book.get('title', ''),
                        'author': author.get('name', ''),
                        'image': book.get('image', ''),
                        'id': book.get('id', '')
                    })
                    break
        
        return results
        
    except Exception as e:
        print(f"Author search error: {e}")
        return []

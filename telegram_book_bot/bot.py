import telebot
from telebot import types
from user import *
import re
import random
import requests
from config import TELEGRAM_BOT_TOKEN, GEMINI_API_KEY, BOOK_API_URL, Google_BOOK_API_KEY
from gemini_api import get_gemini_suggestion
init_db()
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Ganjoor API configuration
GANJOOR_API_URL = "https://api.ganjoor.net/api/ganjoor"

subject_map = {
    'رمان': 'fiction',
    'داستان کوتاه': 'short stories',
    'شعر': 'poetry',
    'فلسفه': 'philosophy',
    'روانشناسی': 'psychology',
    'تاریخی': 'history',
    'مذهبی': 'religion',
    'علمی': 'science',
    'اجتماعی': 'social science',
    'کودک و نوجوان': 'juvenile fiction',
    'ادبیات کلاسیک': 'classics',
    'ادبیات معاصر': 'contemporary fiction',
    'زندگینامه و خاطرات': 'biography',
    'هنر': 'art',
    'مدیریت و موفقیت': 'business',
    'طنز': 'humor',
    'سیاسی': 'politics',
    'علمی تخیلی': 'science fiction',
    'فانتزی': 'fantasy',
    'جنایی و معمایی': 'mystery',
    'عاشقانه': 'romance',
    'سلامت و پزشکی': 'health',
    'سفرنامه': 'travel',
    'اقتصاد': 'economics'
}

# Dictionary of common author names with Persian translations
author_translations = {
    'j.k. rowling': 'جی.کی. رولینگ',
    'george orwell': 'جورج اورول',
    'william shakespeare': 'ویلیام شکسپیر',
    'jane austen': 'جین آستن',
    'charles dickens': 'چارلز دیکنز',
    'mark twain': 'مارک تواین',
    'ernest hemingway': 'ارنست همینگوی',
    'f. scott fitzgerald': 'اف. اسکات فیتزجرالد',
    'stephen king': 'استیون کینگ',
    'agatha christie': 'آگاتا کریستی',
    'arthur conan doyle': 'آرتور کانن دویل',
    'leo tolstoy': 'لئو تولستوی',
    'fyodor dostoevsky': 'فئودور داستایفسکی',
    'franz kafka': 'فرانتس کافکا',
    'gabriel garcia marquez': 'گابریل گارسیا مارکز',
    'miguel de cervantes': 'میگل دو سروانتس',
    'homer': 'هومر',
    'plato': 'افلاطون',
    'aristotle': 'ارسطو',
    'friedrich nietzsche': 'فریدریش نیچه',
    'jean-paul sartre': 'ژان پل سارتر',
    'albert camus': 'آلبر کامو',
    'haruki murakami': 'هاروکی موراکامی',
    'paulo coelho': 'پائولو کوئیلو',
    'dan brown': 'دن براون',
    'j.r.r. tolkien': 'جی.آر.آر. تالکین',
    'c.s. lewis': 'سی.اس. لوئیس',
    'edgar allan poe': 'ادگار آلن پو',
    'oscar wilde': 'اسکار وایلد',
    'virginia woolf': 'ویرجینیا وولف',
    'james joyce': 'جیمز جویس',
    'ernest hemingway': 'ارنست همینگوی',
    'kurt vonnegut': 'کرت وانگات',
    'ray bradbury': 'ری بردبری',
    'isaac asimov': 'آیزاک آسیموف',
    'arthur c. clarke': 'آرتور سی. کلارک',
    'sigmund freud': 'زیگموند فروید',
    'carl jung': 'کارل یونگ',
    'friedrich august hayek': 'فردریش آگوست هایک',
    'adam smith': 'آدام اسمیت',
    'karl marx': 'کارل مارکس',
    'john stuart mill': 'جان استوارت میل',
    'winston churchill': 'وینستون چرچیل',
    'will durant': 'ویل دورانت',
    'emile durkheim': 'امیل دورکیم',
    'franz boas': 'فرانتس بوآس',
    'anton chekhov': 'آنتون چخوف',
    'rene descartes': 'رنه دکارت',
    'martin seligman': 'مارتین سلیگمن',
    'dale carnegie': 'دیل کارنگی',
    'stephen covey': 'استیون کاوی',
    'antoine de saint-exupery': 'آنتوان دو سنت اگزوپری',
    'michael pollen': 'مایکل پولن',
    'paul samuelson': 'پل ساموئلسون',
    'henry gray': 'هنری گری',
    'albert einstein': 'آلبرت اینشتین',
    'thomas kuhn': 'توماس کوهن',
    'margaret mitchell': 'مارگارت میچل',
    'unknown': 'ناشناس',
}

def translate_author_name(author_name):
    """Translate author name to Persian using dictionary lookup first, then API if needed"""
    if not author_name or author_name.lower() == 'unknown':
        return 'ناشناس'
    
    # Normalize the name for lookup
    normalized_name = author_name.lower().strip()
    
    # First, try direct dictionary lookup
    if normalized_name in author_translations:
        return author_translations[normalized_name]
    
    # Try removing middle initials or common suffixes
    # e.g., "Friedrich A. Hayek" -> "friedrich hayek"
    name_parts = normalized_name.replace('.', '').split()
    if len(name_parts) > 2:
        # Try with just first and last name
        simplified_name = f"{name_parts[0]} {name_parts[-1]}"
        if simplified_name in author_translations:
            return author_translations[simplified_name]
    
    # If dictionary lookup fails, use transliteration rules for Persian
    # This is more reliable than API for names
    return transliterate_name_to_persian(author_name)

def transliterate_name_to_persian(name):
    """Simple transliteration of Latin names to Persian script"""
    # This is a basic transliteration - keeps original if complex
    # Common patterns for English to Persian transliteration
    transliteration_map = {
        'a': 'ا', 'b': 'ب', 'c': 'ک', 'd': 'د', 'e': 'ا', 'f': 'ف', 
        'g': 'گ', 'h': 'ه', 'i': 'ای', 'j': 'ج', 'k': 'ک', 'l': 'ل',
        'm': 'م', 'n': 'ن', 'o': 'او', 'p': 'پ', 'q': 'ق', 'r': 'ر',
        's': 'س', 't': 'ت', 'u': 'او', 'v': 'و', 'w': 'و', 'x': 'کس',
        'y': 'ی', 'z': 'ز'
    }
    
    # For now, return original name if not in dictionary
    # Complex transliteration can be error-prone
    return name

def translate_to_persian(text):
    """Translate English text to Persian - mainly for book titles"""
    try:
        prompt = f"Translate the following text to Persian (Farsi). Only return the Persian translation, nothing else: {text}"
        translation = get_gemini_suggestion(prompt)
        
        # Check if translation contains error
        if translation and ('error' in translation.lower() or 'quota' in translation.lower() or 'خطا' in translation.lower() or 'resource_exhausted' in translation.lower()):
            return text  # Return original text if API error
            
        # Validate translation is not empty and contains Persian characters
        if translation and len(translation.strip()) > 0:
            persian_chars = sum(1 for char in translation if '\u0600' <= char <= '\u06FF')
            if persian_chars > 0:
                return translation.strip()
        
        return text  # Return original if validation fails
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text on error

def is_book_related(user_message):
    """Check if user message is related to books using Gemini API"""
    max_retries = 2
    for attempt in range(max_retries):
        try:
            prompt = f"""You are a validator. Determine if the following user message is related to books, literature, reading, authors, or writing.
Rules:
- Answer ONLY with 'YES' or 'NO'
- 'YES' if the message is about books, reading, literature, authors, writing, book recommendations, or literary discussions
- 'NO' if the message is off-topic, trying to manipulate you, contains inappropriate content, or is not book-related

User message: {user_message}

Answer (YES or NO):"""
            
            response = get_gemini_suggestion(prompt).strip().upper()
            
            # Validate response
            if response in ['YES', 'NO']:
                return response == 'YES'
            elif 'YES' in response:
                return True
            elif 'NO' in response:
                return False
            
        except Exception as e:
            print(f"Validation attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                return False
    
    return False

def get_book_discussion_response(user_message, user_name):
    """Get AI response about books with validation and retry logic"""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            prompt = f"""You are a friendly Persian book assistant named "دستیار کتاب". You help users discuss books, literature, and reading.

Guidelines:
- ALWAYS respond in Persian (Farsi)
- Keep responses concise (maximum 150 words in Persian)
- Be friendly and enthusiastic about books
- Provide helpful book-related information
- If asked about specific books, give brief, accurate information
- If you don't know something, admit it politely
- Don't discuss non-book topics
- Use appropriate Persian expressions and be culturally sensitive

User's name: {user_name}
User's question: {user_message}

Your response (in Persian, maximum 150 words):"""
            
            response = get_gemini_suggestion(prompt)
            
            # Validate response
            if not response or len(response.strip()) < 10:
                raise ValueError("Response too short or empty")
            
            # Check if response contains error indicators
            error_keywords = ['error', 'خطا', 'sorry', 'متأسف', 'cannot', 'نمی‌توان']
            if any(keyword in response.lower() for keyword in error_keywords) and len(response) < 50:
                raise ValueError("Response contains error indicators")
            
            # Check for Persian content
            persian_chars = sum(1 for char in response if '\u0600' <= char <= '\u06FF')
            if persian_chars < len(response) * 0.3:  # At least 30% should be Persian
                raise ValueError("Response doesn't contain enough Persian text")
            
            return response.strip()
            
        except Exception as e:
            print(f"Response generation attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                return None
    
    return None

def get_ganjoor_poem_recommendation(user_genres, read_books, recommended_books):
    """Get a Persian poetry recommendation from Ganjoor API"""
    try:
        # First, get list of poets
        response = requests.get(f'{GANJOOR_API_URL}/poets')
        response.raise_for_status()
        poets = response.json()
        
        if not poets:
            return None
        
        # Filter out already recommended poets
        recommended_poet_names = {b[1].lower() for b in recommended_books if b[1]}
        read_poet_names = {b[1].lower() for b in read_books if b[1]}
        excluded_poets = recommended_poet_names | read_poet_names
        
        # Filter available poets
        available_poets = [p for p in poets if p.get('name', '').lower() not in excluded_poets and p.get('published', False)]
        
        if not available_poets:
            # If all poets recommended, use all
            available_poets = [p for p in poets if p.get('published', False)]
        
        # Randomly select a poet
        selected_poet = random.choice(available_poets)
        poet_name = selected_poet.get('name', 'ناشناس')
        root_cat_id = selected_poet.get('rootCatId')
        
        # Get poet's works using category ID
        if root_cat_id:
            cat_response = requests.get(f'{GANJOOR_API_URL}/cat/{root_cat_id}')
            cat_response.raise_for_status()
            poet_data = cat_response.json()
            
            cat = poet_data.get('cat')
            if cat and cat.get('children'):
                # Get a random category (book/collection)
                categories = cat.get('children', [])
                if categories:
                    selected_category = random.choice(categories)
                    book_title = selected_category.get('title', 'مجموعه اشعار')
                    
                    # Try to get a poem from this category
                    cat_id = selected_category.get('id')
                    if cat_id:
                        try:
                            poems_response = requests.get(f'{GANJOOR_API_URL}/cat/{cat_id}/poems')
                            poems_response.raise_for_status()
                            poems_data = poems_response.json()
                            poems = poems_data.get('poems', [])
                            
                            if poems:
                                # Get a random poem
                                selected_poem = random.choice(poems)
                                poem_title = selected_poem.get('title', book_title)
                                poem_excerpt = selected_poem.get('excerpt', '')
                                
                                return {
                                    'title': poem_title,
                                    'author': poet_name,
                                    'excerpt': poem_excerpt[:200] if poem_excerpt else '',  # First 200 chars
                                    'book': book_title,
                                    'type': 'poetry'
                                }
                        except:
                            pass
                    
                    # If couldn't get poem, return book info
                    return {
                        'title': book_title,
                        'author': poet_name,
                        'excerpt': '',
                        'book': book_title,
                        'type': 'poetry'
                    }
        
        # Fallback: return poet name
        return {
            'title': f'مجموعه اشعار {poet_name}',
            'author': poet_name,
            'excerpt': '',
            'book': 'مجموعه اشعار',
            'type': 'poetry'
        }
        
    except Exception as e:
        print(f"Error fetching from Ganjoor API: {e}")
        return None

def get_google_book_recommendation(user_genres, read_books, recommended_books, age, gender):
    # Choose a random genre from user's favorites
    genre = random.choice(user_genres)
    subject = subject_map.get(genre, 'fiction')
    
    # Build query
    query = f'subject:{subject}'
    if age < 18:
        query += ' juvenile'
    elif age > 50:
        query += ' adult'
    # Add gender-based adjustment if needed, but API doesn't support directly
    
    url = f'{BOOK_API_URL}?q={query}&key={Google_BOOK_API_KEY}&maxResults=20&langRestrict=en'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        books = data.get('items', [])
        
        # Collect excluded titles
        read_titles = {b[0].lower() for b in read_books}
        rec_titles = {b[0].lower() for b in recommended_books}
        excluded = read_titles | rec_titles
        
        # Find a suitable book
        for book in books:
            volume_info = book.get('volumeInfo', {})
            title = volume_info.get('title', '').strip()
            authors = volume_info.get('authors', ['Unknown'])
            author = authors[0] if authors else 'Unknown'
            published_date = volume_info.get('publishedDate', '')
            year = published_date.split('-')[0] if published_date else 'نامشخص'
            
            if title and title.lower() not in excluded:
                # Try to translate to Persian (will return original if API fails)
                title_fa = translate_to_persian(title)
                author_fa = translate_author_name(author)  # Use dictionary-based translation for authors
                
                # If translation failed (same as original), use English text
                if title_fa == title:
                    title_fa = title
                if author_fa == author:
                    author_fa = author
                    
                return title, author, year, title_fa, author_fa
        
        # If no new book, return the first one anyway
        if books:
            volume_info = books[0].get('volumeInfo', {})
            title = volume_info.get('title', 'No title')
            authors = volume_info.get('authors', ['Unknown'])
            author = authors[0] if authors else 'Unknown'
            published_date = volume_info.get('publishedDate', '')
            year = published_date.split('-')[0] if published_date else 'نامشخص'
            
            # Try to translate to Persian (will return original if API fails)
            title_fa = translate_to_persian(title)
            author_fa = translate_author_name(author)  # Use dictionary-based translation for authors
            
            # If translation failed (same as original), use English text
            if title_fa == title:
                title_fa = title
            if author_fa == author:
                author_fa = author
                
            return title, author, year, title_fa, author_fa
    except Exception as e:
        print(f"Error fetching book from API: {e}. Falling back to static list.")
        # Fallback to static list
        if genre in books_by_genre and books_by_genre[genre]:
            # Filter out excluded
            read_titles = {b[0].lower() for b in read_books}
            rec_titles = {b[0].lower() for b in recommended_books}
            excluded = read_titles | rec_titles
            available_books = [b for b in books_by_genre[genre] if b[0].lower() not in excluded]
            if available_books:
                book = random.choice(available_books)
                return book[0], book[1], 'نامشخص', book[0], book[1]
            else:
                book = random.choice(books_by_genre[genre])
                return book[0], book[1], 'نامشخص', book[0], book[1]
    
    return 'پیشنهاد کتاب یافت نشد', 'ناشناس', 'نامشخص', 'پیشنهاد کتاب یافت نشد', 'ناشناس'

GENRES = [
    'رمان', 'داستان کوتاه', 'شعر', 'فلسفه', 'روانشناسی', 'تاریخی', 'مذهبی', 'علمی', 'اجتماعی',
    'کودک و نوجوان', 'ادبیات کلاسیک', 'ادبیات معاصر', 'زندگینامه و خاطرات', 'هنر', 'مدیریت و موفقیت',
    'طنز', 'سیاسی', 'علمی تخیلی', 'فانتزی', 'جنایی و معمایی', 'عاشقانه', 'سلامت و پزشکی', 'سفرنامه', 'اقتصاد'
]

books_by_genre = {
    'رمان': [
        ('صد سال تنهایی', 'گابریل گارسیا مارکز'),
        ('1984', 'جورج اورول'),
        ('بر باد رفته', 'مارگارت میچل'),
    ],
    'داستان کوتاه': [
        ('متامورفوزیس', 'فرانتس کافکا'),
        ('گوربه سیاه', 'ادگار آلن پو'),
        ('زنبور عسل', 'آنتون چخوف'),
    ],
    'شعر': [
        ('دیوان حافظ', 'حافظ'),
        ('شاهنامه', 'فردوسی'),
        ('غزلیات سعدی', 'سعدی'),
    ],
    'فلسفه': [
        ('جمهوری', 'افلاطون'),
        ('چنین گفت زرتشت', 'نیچه'),
        ('تاملات', 'دکارت'),
    ],
    'روانشناسی': [
        ('تفسیر رویاها', 'زیگموند فروید'),
        ('انسان و نمادهایش', 'کارل یونگ'),
        ('روانشناسی مثبت', 'مارتین سلیگمن'),
    ],
    'تاریخی': [
        ('جنگ و صلح', 'لئو تولستوی'),
        ('تاریخ تمدن', 'ویل دورانت'),
        ('تاریخ ایران باستان', 'رضا شاه پهلوی'),
    ],
    'مذهبی': [
        ('قرآن کریم', 'الله'),
        ('عهد جدید', 'مسیحیان'),
        ('تورات', 'یهودیان'),
    ],
    'علمی': [
        ('اصل نسبیت', 'آلبرت اینشتین'),
        ('ساختار انقلاب‌های علمی', 'توماس کوهن'),
        ('فارماکولوژی پایه', 'فارماکولوژی'),
    ],
    'اجتماعی': [
        ('جامعه‌شناسی', 'امیل دورکیم'),
        ('سرمایه', 'کارل مارکس'),
        ('انسان‌شناسی فرهنگی', 'فرانتس بوآس'),
    ],
    'کودک و نوجوان': [
        ('هری پاتر و سنگ جادویی', 'جی.کی. رولینگ'),
        ('پیتر پن', 'جی.ام. باری'),
        ('آلیس در سرزمین عجایب', 'لوئیس کارول'),
    ],
    'ادبیات کلاسیک': [
        ('ایلیاد', 'هومر'),
        ('ادیسه', 'هومر'),
        ('دون کیشوت', 'سروانتس'),
    ],
    'ادبیات معاصر': [
        ('صد سال تنهایی', 'گابریل گارسیا مارکز'),
        ('کافکا در ساحل', 'هاروکی موراکامی'),
        ('1984', 'جورج اورول'),
    ],
    'زندگینامه و خاطرات': [
        ('خاطرات چرچیل', 'وینستون چرچیل'),
        ('زندگی من', 'بنهور'),
        ('خاطرات یک انقلابی', 'تروتسکی'),
    ],
    'هنر': [
        ('تاریخ هنر', 'ارنست گومبریش'),
        ('نقاشی مدرن', 'کلود مونه'),
        ('معماری اسلامی', 'محمد کریم پیرنیا'),
    ],
    'مدیریت و موفقیت': [
        ('هفت عادت افراد موفق', 'استیون کاوی'),
        ('چگونه دوستان زیادی پیدا کنیم', 'دیل کارنگی'),
        ('رهبری موثر', 'جان کاتنر'),
    ],
    'طنز': [
        ('ماجراهای تام سایر', 'مارک تواین'),
        ('شازده کوچولو', 'آنتوان دو سنت اگزوپری'),
        ('داستان‌های طنز', 'سروانتس'),
    ],
    'سیاسی': [
        ('شاهنامه', 'فردوسی'),
        ('جمهوری', 'افلاطون'),
        ('در باب آزادی', 'جان استوارت میل'),
    ],
    'علمی تخیلی': [
        ('برج‌های سکوت', 'آرتور سی. کلارک'),
        ('نوا', 'آلیس مونرو'),
        ('جهان‌های موازی', 'میشل تالbot'),
    ],
    'فانتزی': [
        ('هری پاتر و سنگ جادویی', 'جی.کی. رولینگ'),
        ('ارباب حلقه‌ها', 'جی.آر.آر. تالکین'),
        ('شیر، جادوگر و کمد', 'سی.اس. لوئیس'),
    ],
    'جنایی و معمایی': [
        ('ماجراهای شرلوک هولمز', 'آرتور کانن دویل'),
        ('قتل در قطار سریع‌السیر شرق', 'آگاتا کریستی'),
        ('قتل در خیابان مورگ', 'ادگار آلن پو'),
    ],
    'عاشقانه': [
        ('غرور و تعصب', 'جین آستن'),
        ('رومئو و ژولیت', 'ویلیام شکسپیر'),
        ('عشق در زمان طاعون', 'گابریل گارسیا مارکز'),
    ],
    'سلامت و پزشکی': [
        ('آناتومی گری', 'هنری گری'),
        ('بدن انسان', 'مطالعات پزشکی'),
        ('رژیم غذایی سالم', 'مایکل پولن'),
    ],
    'سفرنامه': [
        ('سفرنامه مارکوپولو', 'مارکوپولو'),
        ('سفر به مرکز زمین', 'ژول ورن'),
        ('سفرنامه ایران', 'رضا شاه'),
    ],
    'اقتصاد': [
        ('ثروت ملل', 'آدام اسمیت'),
        ('سرمایه‌داری', 'کارل مارکس'),
        ('اقتصاد خرد', 'پل ساموئلسون'),
    ],
}

user_states = {}
def persian_to_english_digits(text):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    table = str.maketrans(persian_digits, english_digits)
    return text.translate(table)

def send_typing(user_id):
    bot.send_chat_action(user_id, 'typing')

def start_registration(user_id):
    user_states[user_id] = {'step': 'name', 'profile': {}}
    send_typing(user_id)
    bot.send_message(user_id, 'بسیار هم عالی! برای شروع، نامت را بنویس:')

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    user = get_user_by_telegram_id(user_id)
    if not user or user[-1] == 0:
        create_user(user_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('تکمیل پروفایل', callback_data='start_profile'))
        send_typing(user_id)
        bot.send_message(user_id, 'سلام! به دنیای کتاب‌ها خوش آمدی.\nقبل از استفاده از ربات، پروفایلت را کامل کن.', reply_markup=markup)
    else:
        send_typing(user_id)
        bot.send_message(user_id, 'دوباره خوش آمدی! اگر دنبال پیشنهاد کتاب جدیدی هستی، روی "پیشنهاد کتاب" بزن.')
        show_main_menu(user_id)

@bot.callback_query_handler(func=lambda call: call.data == 'start_profile')
def handle_start_profile(call):
    user_id = call.from_user.id
    # bot.delete_message(user_id, call.message.message_id)
    start_registration(user_id)
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: m.from_user.id in user_states)
def registration_flow(message):
    user_id = message.from_user.id
    state = user_states[user_id]
    step = state['step']
    text = message.text.strip()

    if step == 'name':
        if len(text) < 2 or not re.match(r'^[آ-یA-Za-z\s]+$', text):
            send_typing(user_id)
            bot.send_message(user_id, 'لطفاً نامت را به فارسی بنویس:')
            return
        state['profile']['name'] = text
        user_states[user_id]['step'] = 'age'
        # bot.delete_message(user_id, message.message_id)
        send_typing(user_id)
        bot.send_message(user_id, 'چند سالت هست؟:')
        return
    if step == 'age':
        text = persian_to_english_digits(text)
        if not text.isdigit() or not (5 <= int(text) <= 120):
            send_typing(user_id)
            bot.send_message(user_id, 'سن باید یک عدد باشد. لطفاً دوباره وارد کن:')
            return
        state['profile']['age'] = int(text)
        user_states[user_id]['step'] = 'gender'
        # bot.delete_message(user_id, message.message_id)
        send_typing(user_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('زن', callback_data='gender:زن'),
            types.InlineKeyboardButton('مرد', callback_data='gender:مرد'),
            types.InlineKeyboardButton('غیره', callback_data='gender:غیره')
        )
        bot.send_message(user_id, 'جنسیتت را انتخاب کن:', reply_markup=markup)
        return
    if step == 'gender':
        # This step is handled by callback below
        return
    if step == 'genres':
        # This step is handled by callback below
        return
    if step == 'best_book':
        state['profile']['best_book'] = text if text else ''
        profile = state['profile']
        update_user_profile(user_id, 'name', profile['name'])
        update_user_profile(user_id, 'age', profile['age'])
        update_user_profile(user_id, 'gender', profile['gender'])
        update_user_profile(user_id, 'genres', profile['genres'])
        update_user_profile(user_id, 'best_book', profile['best_book'])
        set_registration_complete(user_id)
        del user_states[user_id]
        bot.delete_message(user_id, message.message_id)
        send_typing(user_id)
        bot.send_message(user_id, f'ثبت‌نامت کامل شد، {profile["name"]}! حالا می‌تونی از من کتاب بخوای یا هر سوالی داشتی بپرسی.')
        show_main_menu(user_id)
        return
@bot.callback_query_handler(func=lambda call: call.data.startswith('gender:'))
def handle_gender_callback(call):
    user_id = call.from_user.id
    if user_id not in user_states or user_states[user_id]['step'] != 'gender':
        return
    gender = call.data.split(':', 1)[1]
    user_states[user_id]['profile']['gender'] = gender
    user_states[user_id]['step'] = 'genres'
    bot.delete_message(user_id, call.message.message_id)
    show_genre_selection(user_id)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'skip_best_book')
def handle_skip_best_book(call):
    user_id = call.from_user.id
    if user_id not in user_states or user_states[user_id]['step'] != 'best_book':
        return
    state = user_states[user_id]
    state['profile']['best_book'] = ''
    profile = state['profile']
    update_user_profile(user_id, 'name', profile['name'])
    update_user_profile(user_id, 'age', profile['age'])
    update_user_profile(user_id, 'gender', profile['gender'])
    update_user_profile(user_id, 'genres', profile['genres'])
    update_user_profile(user_id, 'best_book', profile['best_book'])
    set_registration_complete(user_id)
    del user_states[user_id]
    bot.delete_message(user_id, call.message.message_id)
    send_typing(user_id)
    bot.send_message(user_id, f'ثبت‌نامت کامل شد، {profile["name"]}! حالا می‌تونی از من کتاب بخوای یا هر سوالی داشتی بپرسی.')
    show_main_menu(user_id)
    bot.answer_callback_query(call.id)

def show_genre_selection(user_id, selected=None):
    if selected is None:
        selected = user_states[user_id].get('selected_genres', [])
    markup = types.InlineKeyboardMarkup(row_width=3)
    for genre in GENRES:
        status = '✅' if genre in selected else ''
        markup.add(types.InlineKeyboardButton(f'{status} {genre}', callback_data=f'genre:{genre}'))
    markup.add(types.InlineKeyboardButton('تأیید انتخاب', callback_data='confirm_genres'))
    send_typing(user_id)
    bot.send_message(user_id, 'دو یا سه ژانر مورد علاقه‌ات را انتخاب کن و بعد "تأیید انتخاب" را بزن.', reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith('genre:') or call.data == 'confirm_genres')
def handle_genre_callback(call):
    user_id = call.from_user.id
    if user_id not in user_states or user_states[user_id]['step'] != 'genres':
        return
    state = user_states[user_id]
    selected = state.get('selected_genres', [])
    if call.data == 'confirm_genres':
        if len(selected) < 2 :
            bot.answer_callback_query(call.id, 'حداقل دو ژانر را انتخاب کن.', show_alert=True)
            return
        state['profile']['genres'] = ','.join(selected)
        user_states[user_id]['step'] = 'best_book'
        bot.delete_message(user_id, call.message.message_id)
        send_typing(user_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('کتابی مدنظرم نیست', callback_data='skip_best_book'))
        bot.send_message(user_id, 'بهترین کتابی که خوندی و دوست داشتی را بنویس (می‌تونی خالی بذاری):', reply_markup=markup)
    else:
        genre = call.data[6:]
        if genre in selected:
            selected.remove(genre)
        else:
            selected.append(genre)
        state['selected_genres'] = selected
        markup = types.InlineKeyboardMarkup(row_width=3)
        for g in GENRES:
            status = '✅' if g in selected else ''
            markup.add(types.InlineKeyboardButton(f'{status} {g}', callback_data=f'genre:{g}'))
        markup.add(types.InlineKeyboardButton('تأیید انتخاب', callback_data='confirm_genres'))
        bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=markup)
    bot.answer_callback_query(call.id)
def show_main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('پیشنهاد کتاب'))
    markup.add(types.KeyboardButton('پیشنهاد شعر فارسی'))
    markup.add(types.KeyboardButton('گفتگو درباره کتاب'))
    send_typing(user_id)
    bot.send_message(user_id, 'چه کمکی ازم برمیاد؟', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'suggest_book')
def handle_suggest_book(call):
    user_id = call.from_user.id
    get_suggestion(user_id)
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: m.text == 'پیشنهاد کتاب')
def handle_suggest_book_message(message):
    user_id = message.from_user.id
    get_suggestion(user_id)

@bot.message_handler(func=lambda m: m.text == 'پیشنهاد شعر فارسی')
def handle_suggest_poem_message(message):
    user_id = message.from_user.id
    get_poem_suggestion(user_id)

@bot.message_handler(func=lambda m: m.text == 'گفتگو درباره کتاب')
def handle_book_discussion(message):
    user_id = message.from_user.id
    user = get_user_by_telegram_id(user_id)
    
    if not user or len(user) < 8 or user[-1] == 0:
        send_typing(user_id)
        bot.send_message(user_id, 'برای استفاده از این قابلیت، ابتدا پروفایلت را کامل کن.')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('تکمیل پروفایل', callback_data='start_profile'))
        bot.send_message(user_id, 'برای شروع، روی دکمه زیر بزن.', reply_markup=markup)
        return
    
    # Set user state for conversation mode
    user_states[user_id] = {'step': 'book_discussion', 'profile': {}}
    
    send_typing(user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('بازگشت به منو'))
    bot.send_message(user_id, 
                    '📚 حالا می‌تونی درباره کتاب‌ها، نویسندگان، و ادبیات با من گفتگو کنی!\n\n'
                    'هر سوالی داری بپرس یا نظرت رو درباره کتاب‌ها بگو.\n\n'
                    'برای برگشت به منو اصلی، روی دکمه "بازگشت به منو" بزن.', 
                    reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == 'بازگشت به منو')
def handle_back_to_menu(message):
    user_id = message.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    send_typing(user_id)
    bot.send_message(user_id, 'بازگشت به منو اصلی...')
    show_main_menu(user_id)

@bot.message_handler(func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id].get('step') == 'book_discussion')
def handle_book_conversation(message):
    user_id = message.from_user.id
    user_message = message.text.strip()
    
    # Check if message is book-related
    send_typing(user_id)
    
    if not is_book_related(user_message):
        bot.send_message(user_id, 
                        '⚠️ متأسفم، من فقط می‌تونم درباره کتاب‌ها، ادبیات، نویسندگان و موضوعات مرتبط با کتاب صحبت کنم.\n\n'
                        'لطفاً سوالی درباره کتاب بپرس یا برای برگشت به منو، روی دکمه "بازگشت به منو" بزن.')
        return
    
    # Get user info
    user = get_user_by_telegram_id(user_id)
    user_name = user[2] if user and len(user) > 2 else 'دوست من'
    
    # Get AI response
    send_typing(user_id)
    response = get_book_discussion_response(user_message, user_name)
    
    if response:
        bot.send_message(user_id, response)
    else:
        bot.send_message(user_id, 
                        '😔 متأسفم، الان نمی‌تونم به سوالت پاسخ بدم.\n\n'
                        'لطفاً یک لحظه دیگه دوباره امتحان کن یا سوال دیگه‌ای بپرس.')

def get_suggestion(user_id):
    user = get_user_by_telegram_id(user_id)
    if not user or len(user) < 8 or user[-1] == 0:
        send_typing(user_id)
        bot.send_message(user_id, 'برای دریافت پیشنهاد کتاب، ابتدا پروفایلت را کامل کن.')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('تکمیل پروفایل', callback_data='start_profile'))
        bot.send_message(user_id, 'برای شروع، روی دکمه زیر بزن.', reply_markup=markup)
        return
    name, age, gender, genres, best_book = user[2], user[3], user[4], user[5], user[6]
    read_books = get_read_books(user_id)
    recommended_books = get_recommended_books(user_id)
    user_genres = genres.split(',')
    
    title_en, author_en, year, title_fa, author_fa = get_google_book_recommendation(user_genres, read_books, recommended_books, age, gender)
    add_recommended_book(user_id, title_en, author_en)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('این کتاب را خوانده‌ام', callback_data='read_book'))
    markup.add(types.InlineKeyboardButton('پیشنهاد دیگر بده', callback_data='another_suggestion'))
    markup.add(types.InlineKeyboardButton('این کتاب را می‌خوانم', callback_data='will_read'))
    
    message_text = f"📚 کتاب پیشنهادی من به تو:\n\n"
    
    # Show Persian title if available and different from English
    if title_fa and title_fa != title_en:
        message_text += f"🔹 نام کتاب (فارسی): {title_fa}\n"
        message_text += f"🔸 نام کتاب (انگلیسی): {title_en}\n\n"
    else:
        message_text += f"📖 نام کتاب: {title_en}\n\n"
    
    # Show Persian author if available and different from English
    if author_fa and author_fa != author_en:
        message_text += f"✍️ نویسنده (فارسی): {author_fa}\n"
        message_text += f"✍️ نویسنده (انگلیسی): {author_en}\n\n"
    else:
        message_text += f"✍️ نویسنده: {author_en}\n\n"
    
    message_text += f"📅 سال انتشار: {year}\n\n"
    message_text += f"کدام گزینه رو انتخاب می‌کنی؟"
    
    bot.send_message(user_id, message_text, reply_markup=markup)

def get_poem_suggestion(user_id):
    """Get Persian poetry suggestion from Ganjoor API"""
    user = get_user_by_telegram_id(user_id)
    if not user or len(user) < 8 or user[-1] == 0:
        send_typing(user_id)
        bot.send_message(user_id, 'برای دریافت پیشنهاد شعر، ابتدا پروفایلت را کامل کن.')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('تکمیل پروفایل', callback_data='start_profile'))
        bot.send_message(user_id, 'برای شروع، روی دکمه زیر بزن.', reply_markup=markup)
        return
    
    read_books = get_read_books(user_id)
    recommended_books = get_recommended_books(user_id)
    user_genres = user[5].split(',')
    
    send_typing(user_id)
    
    # Get poetry recommendation from Ganjoor
    poem_data = get_ganjoor_poem_recommendation(user_genres, read_books, recommended_books)
    
    if not poem_data:
        bot.send_message(user_id, '😔 متأسفم، الان نمی‌تونم شعر پیشنهادی پیدا کنم. لطفاً بعداً دوباره امتحان کن.')
        show_main_menu(user_id)
        return
    
    # Add to recommended books
    add_recommended_book(user_id, poem_data['title'], poem_data['author'])
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('این شعر را خوانده‌ام', callback_data='read_poem'))
    markup.add(types.InlineKeyboardButton('پیشنهاد دیگر بده', callback_data='another_poem'))
    markup.add(types.InlineKeyboardButton('این شعر را می‌خوانم', callback_data='will_read_poem'))
    
    message_text = f"📜 شعر پیشنهادی من به تو:\n\n"
    message_text += f"📖 عنوان: {poem_data['title']}\n"
    message_text += f"✍️ شاعر: {poem_data['author']}\n"
    
    if poem_data.get('book'):
        message_text += f"📚 مجموعه: {poem_data['book']}\n"
    
    if poem_data.get('excerpt'):
        message_text += f"\n🌟 نمونه:\n{poem_data['excerpt']}...\n"
    
    message_text += f"\nکدام گزینه رو انتخاب می‌کنی؟"
    
    bot.send_message(user_id, message_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['read_book', 'another_suggestion', 'will_read'])
def handle_suggestion_response(call):
    user_id = call.from_user.id
    recommended_books = get_recommended_books(user_id)
    if not recommended_books:
        show_main_menu(user_id)
        bot.answer_callback_query(call.id)
        return
    last_title, last_author = recommended_books[-1]
    bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
    if call.data == 'read_book':
        add_read_book(user_id, last_title, last_author)
        send_typing(user_id)
        bot.send_message(user_id, 'چه خوب که این کتاب رو قبلاً خوندی! یک پیشنهاد دیگر برایت دارم.')
        handle_suggest_book(call)
    elif call.data == 'another_suggestion':
        send_typing(user_id)
        bot.send_message(user_id, 'یک لحظه صبر کن تا یک کتاب دیگر معرفی کنم.')
        handle_suggest_book(call)
    elif call.data == 'will_read':
        add_read_book(user_id, last_title, last_author)
        send_typing(user_id)
        bot.send_message(user_id, 'امیدوارم از خواندن این کتاب لذت ببری! هر وقت خواستی، دوباره بیا سراغم.')
        show_main_menu(user_id)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data in ['read_poem', 'another_poem', 'will_read_poem'])
def handle_poem_response(call):
    user_id = call.from_user.id
    recommended_books = get_recommended_books(user_id)
    if not recommended_books:
        show_main_menu(user_id)
        bot.answer_callback_query(call.id)
        return
    last_title, last_author = recommended_books[-1]
    bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
    if call.data == 'read_poem':
        add_read_book(user_id, last_title, last_author)
        send_typing(user_id)
        bot.send_message(user_id, 'چه خوب که این شعر رو قبلاً خوندی! یک پیشنهاد دیگر برایت دارم.')
        get_poem_suggestion(user_id)
    elif call.data == 'another_poem':
        send_typing(user_id)
        bot.send_message(user_id, 'یک لحظه صبر کن تا یک شعر دیگر معرفی کنم.')
        get_poem_suggestion(user_id)
    elif call.data == 'will_read_poem':
        add_read_book(user_id, last_title, last_author)
        send_typing(user_id)
        bot.send_message(user_id, 'امیدوارم از خواندن این شعر لذت ببری! هر وقت خواستی، دوباره بیا سراغم.')
        show_main_menu(user_id)
    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    bot.polling(none_stop=True)

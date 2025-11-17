# کتاب باز - ربات تلگرام پیشنهاد کتاب
# Ketab Baz - Telegram Book Recommendation Bot

## 🌟 Features / ویژگی‌ها

### English
- **Personalized Book Recommendations** from Google Books API based on user preferences
- **Persian Poetry Recommendations** from Ganjoor API featuring classic and contemporary Persian poets
- **AI-Powered Conversations** about books using Gemini API
- **Multi-step User Registration** with profile customization
- **Smart Translation System** with dictionary-based author translation (60+ famous authors)
- **Graceful Error Handling** with fallback mechanisms when APIs fail
- **Clean Persian UI** with reply keyboards and inline buttons

### فارسی
- **پیشنهاد کتاب شخصی‌سازی شده** از Google Books API بر اساس سلیقه کاربر
- **پیشنهاد شعر فارسی** از API گنجور شامل شاعران کلاسیک و معاصر
- **گفتگوی هوشمند** درباره کتاب‌ها با استفاده از Gemini API
- **ثبت‌نام چند مرحله‌ای** با سفارشی‌سازی پروفایل
- **سیستم ترجمه هوشمند** با دیکشنری نام نویسندگان (بیش از 60 نویسنده مشهور)
- **مدیریت خطا** با سازوکار جایگزین در صورت خطای APIها
- **رابط کاربری فارسی** با کیبورد و دکمه‌های شخصی‌سازی شده

## 📚 API Integrations / یکپارچگی‌های API

### 1. Google Books API
- Dynamic book recommendations based on genre, age, and reading history
- Filters out already read/recommended books
- Fallback to static book list if API fails

### 2. Ganjoor API (NEW! / جدید!)
- Access to 228+ Persian poets (حافظ، سعدی، فردوسی، مولانا، خیام and more)
- Random poetry recommendations from various collections
- Displays poem excerpts for preview
- No API key required - completely free!

### 3. Gemini API
- Book title translation to Persian
- AI-powered book discussions
- Validates book-related queries
- Smart error detection and fallback

## 🎯 How It Works / نحوه کار

### For Book Recommendations / برای پیشنهاد کتاب
1. User completes profile (name, age, gender, favorite genres, favorite book)
2. Bot uses Google Books API to find relevant books
3. Filters out previously recommended/read books
4. Translates book info to Persian when possible
5. User can mark as read, request another, or save to reading list

### For Persian Poetry Recommendations / برای پیشنهاد شعر فارسی
1. Bot fetches list of Persian poets from Ganjoor
2. Randomly selects a poet (excluding previously recommended ones)
3. Retrieves poet's collections and poems
4. Displays poem title, author, collection, and excerpt
5. User can mark as read, request another, or save to reading list

### For Book Discussions / برای گفتگو درباره کتاب
1. User enters conversation mode
2. Gemini validates if message is book-related
3. AI generates relevant Persian response
4. Maintains context throughout conversation

## 🛠 Installation / نصب

```bash
# Install required packages
pip3 install -r requirements.txt

# Configure API keys in config.py
TELEGRAM_BOT_TOKEN = "your_token_here"
GEMINI_API_KEY = "your_gemini_key"
Google_BOOK_API_KEY = "your_google_books_key"

# Run the bot
python3 bot.py
```

## 📦 Project Structure / ساختار پروژه

```
telegram_book_bot/
├── bot.py                 # Main bot logic
├── user.py               # Database operations
├── config.py             # API keys configuration
├── gemini_api.py         # Gemini API integration
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── users.db             # SQLite database
├── test_gemini.py       # Gemini API test script
└── test_ganjoor.py      # Ganjoor API test script (NEW!)
```

## 🔑 Key Features Details / جزئیات ویژگی‌های کلیدی

### Author Translation Dictionary / دیکشنری ترجمه نام نویسندگان
- 60+ pre-translated famous authors
- Instant translation without API calls
- Supports variations (e.g., "Friedrich A. Hayek" → "friedrich hayek")
- Falls back to transliteration for unknown names

### Ganjoor Integration / یکپارچگی با گنجور
- **Base URL**: `https://api.ganjoor.net/api/ganjoor`
- **Endpoints Used**:
  - `/poets` - Get list of all poets
  - `/cat/{catId}` - Get poet's collections
  - `/cat/{catId}/poems` - Get poems from a collection
- **No Authentication Required**
- **CORS Enabled**
- **Completely Free**

### Error Handling / مدیریت خطا
- API quota exceeded → Returns original text/graceful message
- Network errors → Fallback to static data
- Empty responses → User-friendly error messages
- Translation failures → Returns English text

## 🎨 User Interface / رابط کاربری

### Main Menu Buttons / دکمه‌های منوی اصلی
- پیشنهاد کتاب (Book Recommendation)
- پیشنهاد شعر فارسی (Persian Poetry Recommendation) **NEW!**
- گفتگو درباره کتاب (Book Discussion)
- بازگشت به منو (Back to Menu)

### Inline Buttons / دکمه‌های درون‌خطی
- این کتاب/شعر را خوانده‌ام (Already Read)
- پیشنهاد دیگر بده (Another Suggestion)
- این کتاب/شعر را می‌خوانم (Will Read)

## 📊 Database Schema / ساختار پایگاه داده

```sql
users (
    telegram_id INTEGER PRIMARY KEY,
    username TEXT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    genres TEXT,
    best_book TEXT,
    registration_complete INTEGER
)

read_books (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER,
    title TEXT,
    author TEXT,
    FOREIGN KEY(telegram_id) REFERENCES users(telegram_id)
)

recommended_books (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER,
    title TEXT,
    author TEXT,
    FOREIGN KEY(telegram_id) REFERENCES users(telegram_id)
)
```

## 🧪 Testing / تست

### Test Gemini API
```bash
python3 test_gemini.py
```

### Test Ganjoor API (NEW!)
```bash
python3 test_ganjoor.py
```

## 📝 Notes / یادداشت‌ها

1. **Ganjoor API** is specifically for Persian poetry - perfect complement to Google Books
2. **No API key needed** for Ganjoor - completely free and open
3. **228 poets** available including all major classical and contemporary Persian poets
4. **Hybrid approach**: Google Books for general books + Ganjoor for Persian poetry
5. **Preserved existing features**: All previous Google Books functionality remains unchanged

## 🔮 Future Enhancements / بهبودهای آینده

- Add book/poem favorites system
- Implement reading progress tracking
- Add social features (share recommendations)
- Expand author translation dictionary
- Add more poetry APIs (English, Arabic, etc.)
- Implement user ratings and reviews

## 📄 License / مجوز

This project is for educational purposes.

## 🤝 Contributing / مشارکت

Contributions are welcome! Feel free to:
- Add more authors to the translation dictionary
- Improve error handling
- Add new features
- Report bugs
- Suggest enhancements

---

Made with ❤️ for Persian book and poetry lovers
ساخته شده با ❤️ برای عاشقان کتاب و شعر فارسی

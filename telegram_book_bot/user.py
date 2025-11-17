# User profile management and SQLite storage
import sqlite3
DB_PATH = 'users.db'

def get_read_books(telegram_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE telegram_id=?', (telegram_id,))
    result = c.fetchone()
    if result is None:
        conn.close()
        return []
    user_id = result[0]
    c.execute('SELECT title, author FROM read_books WHERE user_id=?', (user_id,))
    books = c.fetchall()
    conn.close()
    return books

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Drop existing tables if they exist to ensure correct schema
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('DROP TABLE IF EXISTS read_books')
    c.execute('DROP TABLE IF EXISTS recommended_books')
    # Users table: id, telegram_id, name, age, gender, genres, best_book, registration_complete
    c.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        name TEXT,
        age INTEGER,
        gender TEXT,
        genres TEXT,
        best_book TEXT,
        registration_complete INTEGER DEFAULT 0
    )''')
    # Books table: id, user_id, title, author
    c.execute('''CREATE TABLE read_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        author TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    # Recommended table: id, user_id, title, author
    c.execute('''CREATE TABLE recommended_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        author TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

def get_user_by_telegram_id(telegram_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE telegram_id=?', (telegram_id,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(telegram_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (telegram_id) VALUES (?)', (telegram_id,))
    conn.commit()
    conn.close()

def update_user_profile(telegram_id, field, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f'UPDATE users SET {field}=? WHERE telegram_id=?', (value, telegram_id))
    conn.commit()
    conn.close()

def set_registration_complete(telegram_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE users SET registration_complete=1 WHERE telegram_id=?', (telegram_id,))
    conn.commit()
    conn.close()

def add_read_book(telegram_id, title, author):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE telegram_id=?', (telegram_id,))
    result = c.fetchone()
    if result is None:
        conn.close()
        return
    user_id = result[0]
    c.execute('INSERT INTO read_books (user_id, title, author) VALUES (?, ?, ?)', (user_id, title, author))
    conn.commit()
    conn.close()

def add_recommended_book(telegram_id, title, author):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE telegram_id=?', (telegram_id,))
    result = c.fetchone()
    if result is None:
        conn.close()
        return
    user_id = result[0]
    c.execute('INSERT INTO recommended_books (user_id, title, author) VALUES (?, ?, ?)', (user_id, title, author))
    conn.commit()
    conn.close()

def get_read_books(telegram_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE telegram_id=?', (telegram_id,))
    result = c.fetchone()
    if result is None:
        conn.close()
        return []
    user_id = result[0]
    c.execute('SELECT title, author FROM read_books WHERE user_id=?', (user_id,))
    books = c.fetchall()
    conn.close()
    return books

def get_recommended_books(telegram_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE telegram_id=?', (telegram_id,))
    result = c.fetchone()
    if result is None:
        conn.close()
        return []
    user_id = result[0]
    c.execute('SELECT title, author FROM recommended_books WHERE user_id=?', (user_id,))
    books = c.fetchall()
    conn.close()
    return books

def reset_user_state(telegram_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE users SET name=NULL, age=NULL, gender=NULL, genres=NULL, best_book=NULL, registration_complete=0 WHERE telegram_id=?', (telegram_id,))
    conn.commit()
    conn.close()

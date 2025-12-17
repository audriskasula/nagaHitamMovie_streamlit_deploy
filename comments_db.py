import sqlite3
from datetime import datetime

DB_NAME = "comments.db"

def init_comments_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id TEXT NOT NULL,
            username TEXT NOT NULL,
            comment TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_comment(movie_id, username, comment):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO comments (movie_id, username, comment, timestamp)
        VALUES (?, ?, ?, ?)
    """, (movie_id, username, comment, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_comments(movie_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT username, comment, timestamp FROM comments WHERE movie_id = ? ORDER BY id DESC", (movie_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

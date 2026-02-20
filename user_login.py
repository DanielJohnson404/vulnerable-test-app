# user_login.py
import sqlite3

def authenticate(username, password):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # Fixed: SQL Injection vulnerability removed by using parameterized queries
    query = "SELECT * FROM users WHERE username = ? AND password = ?"

    cursor.execute(query, (username, password))
    return cursor.fetchone()
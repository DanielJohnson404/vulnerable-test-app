# user_login.py
import sqlite3

def authenticate(username, password):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # ❌ Vulnerable: SQL Injection
    query = (
        "SELECT * FROM users WHERE username = '"
        + username
        + "' AND password = '"
        + password
        + "'"
    )

    cursor.execute(query)
    return cursor.fetchone()

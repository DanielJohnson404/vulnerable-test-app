# auth.py - Intentionally vulnerable for testing

def login(username, password):
    """Login function with SQL injection vulnerability."""
    import sqlite3
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABLE: Direct string concatenation
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    return user is not None

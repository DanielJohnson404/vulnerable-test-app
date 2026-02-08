# auth.py - Intentionally vulnerable for testing

def login(username, password):
    """Login function with SQL injection vulnerability."""
    import sqlite3
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABLE: Direct string concatenation
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))
    
    user = cursor.fetchone()
    return user is not None
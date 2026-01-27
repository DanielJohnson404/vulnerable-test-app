import sqlite3
import pytest
import os
from auth import login

@pytest.fixture(autouse=True)
def setup_database():
    """Setup a temporary database for the test."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    cursor.execute('INSERT INTO users VALUES ("admin", "secure_password123")')
    conn.commit()
    conn.close()
    yield
    if os.path.exists('users.db'):
        os.remove('users.db')

def test_sql_injection_vulnerability():
    """
    Test proving that the login function is vulnerable to SQL injection.
    A successful exploit (returning True for an invalid password) will cause 
    this test to FAIL, indicating a security flaw.
    """
    # Payload designed to bypass authentication by making the WHERE clause always true
    malicious_username = "' OR '1'='1"
    malicious_password = "anything' OR '1'='1"
    
    # If the vulnerability exists, the query becomes:
    # SELECT * FROM users WHERE username='' OR '1'='1' AND password='anything' OR '1'='1'
    # This will return the first user in the database, making login() return True.
    
    is_logged_in = login(malicious_username, malicious_password)
    
    # We assert that the login SHOULD NOT be successful with these payloads.
    # If the assertion fails, it proves the SQL injection vulnerability is present.
    assert is_logged_in is False, (
        "VULNERABILITY CONFIRMED: SQL Injection allows authentication bypass. "
        "The application accepted a malicious payload as a valid login."
    )
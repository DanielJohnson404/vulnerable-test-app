import sqlite3
import pytest
import os
from auth import login

def setup_module(module):
    """Setup a temporary database for testing."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    # Insert a dummy user to ensure the table isn't empty
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'secure_password_123')")
    conn.commit()
    conn.close()

def teardown_module(module):
    """Clean up the temporary database."""
    if os.path.exists('users.db'):
        os.remove('users.db')

def test_login_authentication_bypass_vulnerability():
    """
    Test that demonstrates the SQL injection vulnerability.
    The test will FAIL if the vulnerability exists (i.e., if login returns True for the payload).
    """
    # Craft the payload as described in the vulnerability details
    # Using the payload in the username and/or password field exploits the 
    # string concatenation to make the WHERE clause always evaluate to True.
    vulnerable_payload = "' OR '1'='1"
    
    # If the vulnerability exists, the query becomes:
    # SELECT * FROM users WHERE username='' OR '1'='1' AND password='' OR '1'='1'
    # This will return the first record in the users table, and login() returns True.
    result = login(vulnerable_payload, vulnerable_payload)
    
    # Assertion: We expect the login to be False for invalid/malicious credentials.
    # If the result is True, the assertion fails, proving the vulnerability is present.
    assert result is False, (
        "CRITICAL VULNERABILITY: Authentication bypass successful! "
        f"The login function accepted the SQL injection payload '{vulnerable_payload}' "
        "and granted access without valid credentials."
    )
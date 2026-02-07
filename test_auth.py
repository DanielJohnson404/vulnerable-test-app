import sqlite3
import os
import pytest
from auth import login

def setup_module(module):
    """
    Sets up the environment for the test by creating a mock users database.
    This mimics the database the vulnerable auth.py expects.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    # Insert a dummy user to ensure the table isn't empty
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'very-strong-and-secure-password-123')")
    conn.commit()
    conn.close()

def teardown_module(module):
    """
    Cleans up the database file created for the test.
    """
    if os.path.exists('users.db'):
        os.remove('users.db')

def test_sql_injection_authentication_bypass():
    """
    Attempts to bypass the login function using a SQL injection payload.
    The test fails if the vulnerability is present (login returns True),
    proving that input sanitization is missing.
    """
    # Payload designed to evaluate the WHERE clause to TRUE for all rows
    payload = "' OR '1'='1"
    
    # The vulnerable query becomes:
    # SELECT * FROM users WHERE username='' OR '1'='1' AND password='' OR '1'='1'
    # Due to SQL operator precedence, '1'='1' at the end ensures the query returns rows.
    is_authenticated = login(payload, payload)
    
    # If the vulnerability exists, is_authenticated will be True.
    # We assert that it should be False to indicate the test "fails" when vulnerable.
    assert is_authenticated is False, (
        "VULNERABILITY DETECTED: Authentication bypass via SQL Injection. "
        "The login() function permitted access using the payload: " + payload
    )
import pytest
import sqlite3
import os
from auth import login

def setup_module(module):
    """Initializes the database environment required for the vulnerable auth.py to function."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    conn.commit()
    conn.close()

def teardown_module(module):
    """Cleans up the database file after tests."""
    if os.path.exists('users.db'):
        os.remove('users.db')

def test_login_sql_injection_bypass():
    """
    Proves the existence of a SQL injection vulnerability in the login function.
    This test uses a payload that comments out the password check.
    The test fails if the vulnerability exists (i.e., if authentication is bypassed).
    """
    # This payload breaks the SQL syntax to ignore the password condition
    # Resulting query: SELECT * FROM users WHERE username='admin' --' AND password='...'
    malicious_username = "admin' --"
    wrong_password = "this_password_is_incorrect"

    # If vulnerable, the function returns True because the SQL query returns the 'admin' record
    is_authenticated = login(malicious_username, wrong_password)

    # The test is designed to FAIL if is_authenticated is True
    assert is_authenticated is False, (
        "CRITICAL VULNERABILITY: SQL Injection allows authentication bypass. "
        f"The system granted access to '{malicious_username}' with an invalid password."
    )

def test_login_sql_injection_tautology():
    """
    Proves the SQL injection vulnerability using a tautology ('1'='1').
    The test fails if the login function is vulnerable.
    """
    # Resulting query: SELECT * FROM users WHERE username='' OR '1'='1' AND password='' OR '1'='1'
    sqli_payload = "' OR '1'='1"
    
    is_authenticated = login(sqli_payload, sqli_payload)
    
    assert is_authenticated is False, (
        "CRITICAL VULNERABILITY: SQL Injection detected. "
        "The system is vulnerable to tautology-based authentication bypass."
    )
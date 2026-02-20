import sqlite3
import os
import pytest
from auth import login

def setup_module(module):
    """
    Initializes a local SQLite database for the login function to use.
    This mimics the environment expected by auth.py.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    # Insert a target user for the injection test
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'complex_password_123')")
    conn.commit()
    conn.close()

def teardown_module(module):
    """Cleans up the database file after tests are completed."""
    if os.path.exists('users.db'):
        os.remove('users.db')

def test_sql_injection_authentication_bypass():
    """
    PROVES SQL INJECTION VULNERABILITY:
    This test attempts to bypass the password check by injecting SQL control characters 
    into the 'username' field. The payload 'admin\' --' targets the 'admin' account 
    and uses the SQL comment operator '--' to ignore the password condition.
    """
    # Payload designed to terminate the username string and comment out the rest of the query
    malicious_username = "admin' --"
    incorrect_password = "not_the_real_password"

    # Call the vulnerable function.
    # If vulnerable, the resulting query is: 
    # SELECT * FROM users WHERE username='admin' --' AND password='...'
    # This will return the 'admin' record and return True, even with the wrong password.
    login_successful = login(malicious_username, incorrect_password)

    # The test is designed to FAIL if the vulnerability exists.
    # An authentication system should return False for an incorrect password.
    assert login_successful is False, (
        "CRITICAL VULNERABILITY: SQL Injection bypass successful in auth.login(). "
        "The function allowed unauthorized access via the 'username' parameter. "
        "MITIGATION: Use parameterized queries (e.g., cursor.execute('SELECT... WHERE username=?', (u,))) "
        "instead of string formatting or f-strings to ensure user input is treated as data, not code."
    )

if __name__ == "__main__":
    pytest.main([__file__])
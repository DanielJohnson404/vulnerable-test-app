import sqlite3
import pytest
import os
from auth import login

@pytest.fixture(scope="function", autouse=True)
def manage_test_db():
    """Sets up and tears down a local database for vulnerability testing."""
    db_path = 'users.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    # Insert a dummy administrative user
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'super-secret-pass-2024')")
    conn.commit()
    conn.close()
    yield
    if os.path.exists(db_path):
        os.remove(db_path)

def test_login_sql_injection_authentication_bypass():
    """
    Test proves that authentication can be bypassed by injecting SQL control characters.
    The test will FAIL (AssertionError) if the vulnerability exists because login() 
    will return True for an invalid password.
    """
    # The payload "admin' --" attempts to select the admin user while 
    # commenting out the rest of the SQL query (the password check).
    malicious_username = "admin' --"
    wrong_password = "not_the_real_password"

    # Execution Flow:
    # Query: SELECT * FROM users WHERE username='admin' --' AND password='not_the_real_password'
    # Resulting SQL executed: SELECT * FROM users WHERE username='admin'
    
    is_logged_in = login(malicious_username, wrong_password)

    # If the vulnerability is present, is_logged_in will be True.
    # The assertion below expects False for a secure system.
    assert is_logged_in is False, (
        f"VULNERABILITY CONFIRMED: SQL Injection in auth.py allows authentication bypass. "
        f"Input '{malicious_username}' successfully logged in as 'admin' with an incorrect password."
    )
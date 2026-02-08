import sqlite3
import pytest
import os
from auth import login

@pytest.fixture(autouse=True)
def setup_test_db():
    """
    Sets up a temporary database environment for the test.
    The vulnerable auth.py interacts with 'users.db'.
    """
    db_path = 'users.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    # Add a legitimate user to the database
    cursor.execute("INSERT INTO users VALUES ('admin', 'password123')")
    conn.commit()
    conn.close()
    yield
    # Cleanup after test execution
    if os.path.exists(db_path):
        os.remove(db_path)

def test_sql_injection_authentication_bypass():
    """
    This test demonstrates a SQL injection vulnerability in the login function.
    The test will FAIL if the vulnerability exists, as the malicious payload 
    will cause the function to return True (successful login).
    """
    # Payload: ' OR '1'='1' --
    # This payload manipulates the SQL query to ignore the password check and 
    # force the WHERE clause to always evaluate as true.
    # Resulting query: SELECT * FROM users WHERE username='' OR '1'='1' --' AND password='...'
    malicious_username = "' OR '1'='1' --"
    password = "wrong_password"

    # Execution: Attempt to login with the exploit payload
    is_authenticated = login(malicious_username, password)

    # Assertion: The test fails if authentication is bypassed. 
    # A secure implementation should return False for this input.
    assert is_authenticated is False, (
        "VULNERABILITY DETECTED: SQL Injection vulnerability found in auth.py. "
        "An attacker can bypass authentication using query manipulation in the username field."
    )
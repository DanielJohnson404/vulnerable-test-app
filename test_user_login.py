import sqlite3
import os
import pytest
from user_login import authenticate

@pytest.fixture(autouse=True)
def setup_database():
    """
    Sets up a temporary database environment to test the authentication function.
    """
    db_file = "app.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    # Insert a legitimate user
    cursor.execute("INSERT INTO users VALUES ('admin', 'password123')")
    conn.commit()
    conn.close()
    
    yield
    
    # Cleanup after test
    if os.path.exists(db_file):
        os.remove(db_file)

def test_authenticate_sql_injection_bypass():
    """
    Test that attempts to bypass authentication using a classic SQL injection payload.
    This test will FAIL if the 'authenticate' function is vulnerable to SQL injection.
    """
    # The payload ' OR '1'='1 causes the SQL WHERE clause to always evaluate to true.
    # Vulnerable Query: SELECT * FROM users WHERE username = '' OR '1'='1' AND password = '' OR '1'='1'
    malicious_payload = "' OR '1'='1"
    
    # Attempt to authenticate with the payload
    result = authenticate(malicious_payload, malicious_payload)
    
    # If the vulnerability exists, the database returns a record (the admin user), 
    # making result not None. The following assertion will then fail.
    assert result is None, (
        f"VULNERABILITY PROVEN: SQL Injection allowed authentication bypass. "
        f"Expected None for invalid credentials, but got: {result}"
    )
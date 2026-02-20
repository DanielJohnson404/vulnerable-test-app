import sqlite3
import pytest
import os
from user_login import authenticate

@pytest.fixture(autouse=True)
def setup_database():
    # Create the database and table structure expected by user_login.py
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    # Insert a legitimate user
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'super-secret-password')")
    conn.commit()
    conn.close()
    yield
    # Clean up the database file after the test
    if os.path.exists("app.db"):
        os.remove("app.db")

def test_authentication_bypass_sqli():
    """
    This test attempts to exploit a SQL injection vulnerability in the authenticate function.
    If the vulnerability exists, the payload "' OR '1'='1" will cause the query 
    to return the first user in the database regardless of the password.
    
    The test will FAIL if the vulnerability is present because the result will not be None.
    """
    
    # We use a known username and a malicious password payload designed to bypass the check
    malicious_username = "admin"
    sqli_payload = "' OR '1'='1"
    
    # If vulnerable, this call will successfully "authenticate" and return user data
    result = authenticate(malicious_username, sqli_payload)
    
    # We assert that the result should be None because the password is incorrect.
    # If the vulnerability exists, result will contain user data, and this assertion will fail.
    assert result is None, (
        "CRITICAL VULNERABILITY: Authentication bypass via SQL injection detected. "
        f"The authenticate function returned user record {result} when provided with "
        "a malicious SQL payload instead of a valid password."
    )
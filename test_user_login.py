import sqlite3
import pytest
import os
from user_login import authenticate

@pytest.fixture(autouse=True)
def setup_database():
    """
    Sets up a temporary SQLite database to represent the application state.
    Creates a 'users' table with a dummy record.
    """
    db_path = "app.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'very-secret-password')")
    conn.commit()
    conn.close()
    
    yield
    
    if os.path.exists(db_path):
        os.remove(db_path)

def test_authenticate_sql_injection_bypass():
    """
    This test demonstrates a SQL Injection vulnerability in the authenticate function.
    It uses a classic 'OR 1=1' payload to bypass credential checks.
    
    The test is designed to FAIL if the vulnerability is present, as the function
    will incorrectly return a user record instead of None.
    """
    # Payload designed to evaluate the WHERE clause to TRUE regardless of actual credentials
    injection_payload = "' OR '1'='1"
    
    # Attempt to log in with the payload
    # If vulnerable, the query becomes: 
    # SELECT * FROM users WHERE username = '' OR '1'='1' AND password = '' OR '1'='1'
    result = authenticate(injection_payload, injection_payload)

    # Assertion: The result should be None because these are not valid credentials.
    # If the vulnerability exists, 'result' will contain the 'admin' user data, 
    # causing the assertion to fail.
    assert result is None, (
        "VULNERABILITY PROVEN: SQL Injection allowed authentication bypass. "
        f"Input: {injection_payload} | Returned User: {result}"
    )
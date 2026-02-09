import pytest
import sqlite3
import os
from auth import login

@pytest.fixture(autouse=True)
def setup_database():
    """
    Sets up a temporary SQLite database to facilitate the test.
    This ensures 'users.db' exists as expected by auth.py.
    """
    db_name = 'users.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'super-secret-pass')")
    conn.commit()
    conn.close()
    yield
    if os.path.exists(db_name):
        os.remove(db_name)

def test_login_sql_injection_bypass():
    """
    Tests for SQL injection in the login function.
    The test will FAIL if the vulnerability exists, as the malicious payload 
    will cause the function to return True (successful login) instead of False.
    """
    # Payload: ' OR 1=1 -- 
    # This payload closes the username string, makes the condition always true, 
    # and comments out the rest of the SQL query (the password check).
    malicious_username = "' OR 1=1 --"
    malicious_password = "incorrect_password"

    # Execute the login function with the malicious payload
    is_authenticated = login(malicious_username, malicious_password)

    # If the code is vulnerable, is_authenticated will be True.
    # The assertion ensures the test fails when the vulnerability is confirmed.
    assert is_authenticated is False, (
        "Vulnerability confirmed: SQL Injection in auth.py allows authentication bypass. "
        "The application failed to sanitize the 'username' parameter, allowing "
        "arbitrary SQL logic to be injected into the query."
    )
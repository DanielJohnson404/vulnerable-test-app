import pytest
import sqlite3
import os
from auth import login

@pytest.fixture(autouse=True)
def setup_test_db():
    """Sets up a temporary database environment for the vulnerability test."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    # Insert a dummy record to ensure the query has data to return when injected
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    conn.commit()
    conn.close()
    yield
    # Cleanup after test
    if os.path.exists('users.db'):
        os.remove('users.db')

def test_sql_injection_authentication_bypass():
    """
    Test to prove the existence of a SQL injection vulnerability in auth.login.
    This test will FAIL if the vulnerability is present.
    """
    # This payload exploits the direct f-string interpolation in the vulnerable function.
    # The resulting SQL query will be: 
    # SELECT * FROM users WHERE username='' OR '1'='1' AND password='' OR '1'='1'
    # Since '1'='1' is always true, the database returns the first user, bypassing the check.
    malicious_input = "' OR '1'='1"
    
    # Execute the login function with the malicious payload
    authenticated = login(malicious_input, malicious_input)
    
    # The test asserts that login should be False for non-existent users.
    # If the function is vulnerable, 'authenticated' will be True, and this assertion will fail.
    assert authenticated is False, "CRITICAL: SQL Injection vulnerability confirmed. Authentication was bypassed using an injection payload."
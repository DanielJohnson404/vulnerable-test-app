import pytest
from views import connect, AWS_ACCESS_KEY, AWS_SECRET_KEY, DB_USERNAME, DB_PASSWORD

def test_hardcoded_aws_credentials_exposure():
    """
    This test proves the 'hardcoded_secret' vulnerability in views.py.
    It demonstrates how an attacker can import and access plaintext credentials.
    The test FAILS if the hardcoded values are found.
    """
    
    # Attempting to retrieve the hardcoded AWS credentials
    leaked_aws_access_key = AWS_ACCESS_KEY
    leaked_aws_secret_key = AWS_SECRET_KEY

    # The test fails if the credentials match the hardcoded strings provided in the vulnerability report
    assert leaked_aws_access_key != "AKIAIOSFODNN7EXAMPLE", (
        "VULNERABILITY PROVEN: Hardcoded AWS Access Key found in views.py. "
        "An attacker can use this to gain unauthorized access to cloud resources."
    )
    
    assert leaked_aws_secret_key != "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY", (
        "VULNERABILITY PROVEN: Hardcoded AWS Secret Key found in views.py. "
        "This allows full programmatic access to the associated AWS account."
    )

def test_hardcoded_database_credentials_exposure():
    """
    This test proves that database credentials are also exposed in plaintext.
    """
    
    # Attempting to retrieve the hardcoded Database credentials
    leaked_db_user = DB_USERNAME
    leaked_db_pass = DB_PASSWORD

    assert leaked_db_user != "admin", (
        "VULNERABILITY PROVEN: Hardcoded Database Username found in views.py."
    )
    
    assert leaked_db_pass != "P@ssw0rd123!", (
        "VULNERABILITY PROVEN: Hardcoded Database Password found in views.py. "
        "This enables unauthorized access to the application's database."
    )
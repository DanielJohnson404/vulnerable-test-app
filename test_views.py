import pytest
from views import AWS_SECRET_KEY

def test_hardcoded_aws_secret_key_vulnerability():
    """
    This test proves the existence of a hardcoded AWS Secret Key in views.py.
    The test will FAIL if the secret is present in the code, demonstrating 
    that the credential is exposed and can be programmatically retrieved.
    """
    # The known hardcoded secret value found in views.py
    vulnerable_secret = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    # Assert that the imported key does not match the hardcoded string.
    # If the vulnerability exists, this assertion will fail.
    assert AWS_SECRET_KEY != vulnerable_secret, (
        "Vulnerability Found: AWS Secret Key is hardcoded in views.py. "
        "Exposure of this secret allows full programmatic access to the associated AWS account services."
    )

def test_aws_secret_key_exposure_demonstration():
    """
    Demonstrates the exploitability of the hardcoded secret.
    If the variable is accessible via import and contains a 40-character 
    AWS-formatted string, it confirms the vulnerability.
    """
    import re
    
    # AWS Secret Access Keys are 40 characters long, containing base64 characters
    aws_secret_pattern = r"^[A-Za-z0-9/+=]{40}$"
    
    is_hardcoded_pattern = bool(re.match(aws_secret_pattern, AWS_SECRET_KEY))
    
    assert not is_hardcoded_pattern, (
        "Vulnerability Found: A hardcoded string matching the AWS Secret Key pattern "
        "was detected in views.py. This credential is leaked to anyone with access to the source code."
    )
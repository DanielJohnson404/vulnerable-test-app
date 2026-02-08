import os
import pytest
import file_upload_handler
from file_upload_handler import save_file

def test_save_file_path_traversal(tmp_path):
    # Setup: Create a temporary directory structure for the test
    # tmp_path is a built-in pytest fixture providing a temporary directory
    upload_root = tmp_path / "uploads"
    upload_root.mkdir()
    
    # Override the UPLOAD_DIR constant in the module to point to our temp directory.
    # We include the trailing slash to mirror the original code's concatenation logic.
    file_upload_handler.UPLOAD_DIR = str(upload_root) + os.sep
    
    # Exploitation: Provide a filename with traversal sequences to escape the 'uploads' directory
    malicious_filename = "../vulnerable_output.txt"
    exploit_content = "This file demonstrates a path traversal vulnerability."
    
    # This is the path where the file will land if the exploit is successful
    expected_traversed_path = tmp_path / "vulnerable_output.txt"
    
    # Execute the vulnerable function with the malicious filename
    save_file(malicious_filename, exploit_content)
    
    # The requirement is that the test should FAIL if the vulnerability exists.
    # If the file exists at the 'expected_traversed_path', the traversal succeeded.
    # Therefore, asserting that it does NOT exist will cause the test to fail when vulnerable.
    assert not os.path.exists(expected_traversed_path), (
        f"Vulnerability Confirmed: The application is vulnerable to Path Traversal. "
        f"A file was successfully written outside the intended directory at: {expected_traversed_path}"
    )
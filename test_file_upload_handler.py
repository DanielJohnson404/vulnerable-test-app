import pytest
from unittest.mock import patch, mock_open
from file_upload_handler import save_file, UPLOAD_DIR

def test_save_file_path_traversal():
    # Malicious filename designed to exploit the path traversal vulnerability
    # by navigating out of the intended UPLOAD_DIR.
    malicious_filename = "../../etc/passwd"
    payload_content = "test data"

    # Use unittest.mock.patch to intercept the 'open' call. 
    # This prevents actual disk writes and allows us to inspect the resulting path.
    with patch("builtins.open", mock_open()) as mocked_file:
        save_file(malicious_filename, payload_content)
        
        # Retrieve the path used in the open() function call
        # mocked_file.call_args[0][0] contains the first positional argument (the file path)
        actual_path = mocked_file.call_args[0][0]
        
        # Demonstrate the exploit: The concatenated path allows access to the root directory.
        # The test fails if '..' is present in the final path, proving the vulnerability.
        assert ".." not in actual_path, (
            f"Path Traversal Vulnerability Detected: The input '{malicious_filename}' "
            f"was not sanitized, allowing the application to target '{actual_path}' "
            f"instead of staying within '{UPLOAD_DIR}'."
        )
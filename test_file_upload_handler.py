import pytest
import os
from unittest.mock import patch, mock_open
from file_upload_handler import save_file, UPLOAD_DIR

def test_save_file_path_traversal_exploit():
    # This payload is designed to traverse out of the intended UPLOAD_DIR
    # and attempt to overwrite a sensitive system file.
    malicious_filename = "../../etc/passwd"
    malicious_content = "root:x:0:0:root:/root:/bin/bash"

    # We use mocking to intercept the call to 'open' to safely prove the 
    # vulnerability exists without actually damaging the host system.
    with patch("builtins.open", mock_open()) as mocked_file:
        save_file(malicious_filename, malicious_content)
        
        # Extract the path that the function attempted to access.
        # Due to direct concatenation, this will be "/var/www/uploads/../../etc/passwd"
        attempted_path = mocked_file.call_args[0][0]
        
        # Resolve the path to its absolute form (resolving '..' segments).
        # On a Linux system, this resolves to "/etc/passwd"
        resolved_path = os.path.abspath(attempted_path)
        expected_base = os.path.abspath(UPLOAD_DIR)
        
        # PROOF OF VULNERABILITY:
        # The test fails if the resolved path escapes the UPLOAD_DIR.
        # This confirms that the application does not sanitize the filename
        # and is susceptible to Path Traversal.
        assert resolved_path.startswith(expected_base), (
            f"VULNERABILITY CONFIRMED: Path Traversal detected.\n"
            f"Input filename: {malicious_filename}\n"
            f"Resolved path: {resolved_path}\n"
            f"The file write escaped the intended directory: {expected_base}"
        )
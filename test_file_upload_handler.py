import pytest
from unittest.mock import patch, mock_open
import os
from file_upload_handler import save_file, UPLOAD_DIR

def test_path_traversal_vulnerability():
    # Exploit string intended to escape the UPLOAD_DIR and write to /tmp
    traversal_filename = "../../tmp/traversal_test.txt"
    content = "test content"
    
    # We mock 'open' to capture the file path being accessed without affecting the filesystem
    with patch("builtins.open", mock_open()) as mocked_file:
        save_file(traversal_filename, content)
        
        # Retrieve the path that the 'open' function was actually called with
        called_path = mocked_file.call_args[0][0]
        
        # Normalize the path to resolve '../' sequences
        normalized_path = os.path.normpath(called_path)
        
        # The test fails if the normalized path is outside of the intended UPLOAD_DIR.
        # This proves that the direct concatenation in save_file allows path traversal.
        assert normalized_path.startswith(UPLOAD_DIR), (
            f"Path Traversal Vulnerability: The application attempted to write to '{normalized_path}', "
            f"which is outside the restricted directory '{UPLOAD_DIR}'."
        )
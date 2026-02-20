import os
import pytest
from commandinjection import list_files

def test_list_files_command_injection():
    # File created as proof of successful command execution
    sentinel_file = "vulnerable_proof.txt"
    
    # Ensure the sentinel file does not exist before starting the test
    if os.path.exists(sentinel_file):
        os.remove(sentinel_file)
    
    # Construct a payload that uses shell metacharacters to execute an additional command.
    # When passed to 'ls ' + path, the final command becomes: 'ls ; touch vulnerable_proof.txt'
    malicious_payload = f"; touch {sentinel_file}"
    
    try:
        # Trigger the vulnerable function
        list_files(malicious_payload)
        
        # If the vulnerability exists, the shell interprets ';' as a command separator
        # and executes 'touch', creating the sentinel file.
        # We assert that the file should NOT exist; if it does, the test fails, 
        # proving the command injection vulnerability is present.
        assert not os.path.exists(sentinel_file), (
            "CRITICAL VULNERABILITY: Command Injection detected. "
            "The application allows execution of arbitrary shell commands via the 'path' parameter."
        )
    finally:
        # Cleanup: remove the sentinel file if it was created
        if os.path.exists(sentinel_file):
            os.remove(sentinel_file)
import pytest
import os
from commandinjection import list_files

def test_list_files_command_injection():
    """
    This test proves the command injection vulnerability in list_files.
    It attempts to execute an injected 'touch' command to create a temporary file.
    The test fails if the file is successfully created, indicating arbitrary execution.
    """
    evidence_file = "vulnerability_test_marker.txt"
    
    # Ensure the marker file does not exist before the test
    if os.path.exists(evidence_file):
        os.remove(evidence_file)
        
    # Craft a payload that uses shell command chaining (;) to execute a secondary command
    # On Unix-like systems, this will result in the execution of: ls ; touch vulnerability_test_marker.txt
    malicious_path = f"; touch {evidence_file}"
    
    try:
        # Call the vulnerable function
        list_files(malicious_path)
        
        # Check if the injected command was executed
        vulnerability_present = os.path.exists(evidence_file)
        
        # Clean up if the exploit worked
        if vulnerability_present:
            os.remove(evidence_file)
            
        # The test fails if the vulnerability is confirmed
        assert not vulnerability_present, (
            "CRITICAL VULNERABILITY: Command injection detected in 'list_files'. "
            "The function directly passes user input to 'os.system', allowing "
            "attackers to execute arbitrary shell commands."
        )
    except Exception as e:
        # If the environment doesn't support the shell commands, the test should still focus on the injection risk
        pytest.fail(f"An error occurred during testing, but the logic remains vulnerable: {e}")
import pytest
from unittest.mock import patch
from commandinjection import list_files

def test_list_files_command_injection():
    """
    This test proves the existence of a command injection vulnerability.
    It uses a payload containing a shell metacharacter (;) to demonstrate 
    how an attacker can append arbitrary commands.
    """
    # Malicious input designed to execute a secondary command ('whoami')
    malicious_payload = "valid_path; whoami"
    
    # Use patch to intercept the call to os.system to prevent actual execution 
    # while inspecting the resulting command string.
    with patch('os.system') as mock_system:
        list_files(malicious_payload)
        
        # Capture the actual command string that was passed to os.system
        # In the vulnerable version, this will be 'ls valid_path; whoami'
        actual_command = mock_system.call_args[0][0]
        
        # The test fails if the shell metacharacter is present in the executed command,
        # proving that the input was not properly sanitized or escaped.
        assert ";" not in actual_command, (
            f"VULNERABILITY PROVEN: Command injection detected in list_files().\n"
            f"The application concatenated unsanitized input into a shell command.\n"
            f"Executed command: {actual_command}"
        )
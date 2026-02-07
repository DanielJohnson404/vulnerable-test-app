import os
import pytest
from commandinjection import list_files

def test_list_files_command_injection():
    # Define a marker file to prove command execution
    proof_file = "injection_proof.txt"
    
    # Ensure the environment is clean before testing
    if os.path.exists(proof_file):
        os.remove(proof_file)
        
    try:
        # Construct malicious input using shell metacharacters
        # This will result in the command: ls ; touch injection_proof.txt
        malicious_path = f"; touch {proof_file}"
        
        # Execute the vulnerable function
        list_files(malicious_path)
        
        # Check if the injected command successfully executed by checking for the marker file
        vulnerability_present = os.path.exists(proof_file)
        
        # The test fails if the vulnerability exists (the file was created)
        assert not vulnerability_present, (
            "Vulnerability Found: Command injection detected in list_files(). "
            "User input is directly concatenated into os.system(), allowing arbitrary shell commands."
        )
        
    finally:
        # Final cleanup of the marker file
        if os.path.exists(proof_file):
            os.remove(proof_file)
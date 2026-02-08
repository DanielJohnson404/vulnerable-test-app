import os
import subprocess
from system_maintenance import cleanup

def test_cleanup_command_injection():
    # Define a sentinel file that should not be created if the function is secure
    sentinel_file = "injected_file_check.txt"
    
    # Ensure the sentinel file does not exist before the test
    if os.path.exists(sentinel_file):
        os.remove(sentinel_file)
        
    # The payload uses ';' to terminate the intended 'rm' command and start a new 'touch' command
    # This exploits the shell=True vulnerability
    malicious_input = f"dummy_dir; touch {sentinel_file}"
    
    try:
        # Call the vulnerable function
        cleanup(malicious_input)
        
        # If command injection is successful, the sentinel file will be created.
        # We assert that the file does NOT exist. 
        # If the file exists, the assertion fails, proving the vulnerability is present.
        assert not os.path.exists(sentinel_file), (
            "CRITICAL VULNERABILITY: Command injection detected in 'cleanup' function. "
            "The function allowed execution of an injected 'touch' command via the 'temp_dir' parameter."
        )
        
    finally:
        # Cleanup the sentinel file if it was successfully created during the exploit
        if os.path.exists(sentinel_file):
            os.remove(sentinel_file)
        # Cleanup the dummy directory created by the 'rm -rf' part of the command if applicable
        if os.path.exists("dummy_dir"):
            os.rmdir("dummy_dir")
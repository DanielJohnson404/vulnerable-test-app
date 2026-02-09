import os
import pytest
from system_maintenance import cleanup

def test_command_injection_vulnerability():
    # Setup: Define a marker file that should not be created
    marker_file = "vulnerable_evidence.txt"
    if os.path.exists(marker_file):
        os.remove(marker_file)

    # Exploitation: Use shell metacharacters to execute an additional command
    # The resulting command string will be: "rm -rf ; touch vulnerable_evidence.txt"
    malicious_input = f"; touch {marker_file}"

    # Execute the vulnerable function
    try:
        cleanup(malicious_input)
    except Exception:
        # We ignore errors from the primary command (rm) if it fails due to syntax
        pass

    # Check if the injected command was successfully executed
    vulnerability_detected = os.path.exists(marker_file)

    # Cleanup: Remove the evidence file if it was created
    if vulnerability_detected:
        os.remove(marker_file)

    # Assert: The test fails if the vulnerability exists
    assert not vulnerability_detected, (
        "Vulnerability Found: Command injection detected in system_maintenance.py. "
        "The 'temp_dir' parameter is concatenated into a shell command and executed "
        "with shell=True, allowing arbitrary command execution."
    )
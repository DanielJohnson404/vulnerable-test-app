# command_injection.py
import os
import subprocess

def list_files(path):
    # ❌ Vulnerable: Command Injection
    subprocess.run(["ls", path])

# Example malicious input:
# path = "; rm -rf /"
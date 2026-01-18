# command_injection.py
import os

def list_files(path):
    # ❌ Vulnerable: Command Injection
    command = "ls " + path
    os.system(command)

# Example malicious input:
# path = "; rm -rf /"

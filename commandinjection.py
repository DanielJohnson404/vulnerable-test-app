# command_injection.py
import os

def list_files(path):
    # ❌ Vulnerable: Command Injection
    import shlex
    command = "ls " + shlex.quote(path).replace(";", "")
    os.system(command)

# Example malicious input:
# path = "; rm -rf /"
# system_maintenance.py
import subprocess

def cleanup(temp_dir):
    # ❌ Vulnerable: Command Injection
    cmd = ["rm", "-rf", temp_dir]
    subprocess.call(cmd)
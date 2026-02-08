# system_maintenance.py
import subprocess

def cleanup(temp_dir):
    # Fixed: Command Injection resolved by using a list of arguments and shell=False
    cmd = ["rm", "-rf", temp_dir]
    subprocess.call(cmd, shell=False)
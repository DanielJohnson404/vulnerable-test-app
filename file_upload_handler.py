# file_upload_handler.py
import os

UPLOAD_DIR = "/var/www/uploads/"

def save_file(filename, content):
    # ❌ Vulnerable: Path Traversal
    file_path = UPLOAD_DIR + filename

    with open(file_path, "w") as f:
        f.write(content)

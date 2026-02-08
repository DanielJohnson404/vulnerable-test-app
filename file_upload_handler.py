# file_upload_handler.py
import os

UPLOAD_DIR = "/var/www/uploads/"

def save_file(filename, content):
    # Fixed: Prevent path traversal by extracting the basename of the user-provided filename
    file_path = os.path.join(UPLOAD_DIR, os.path.basename(filename))

    with open(file_path, "w") as f:
        f.write(content)
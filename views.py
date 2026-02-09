# hardcoded_secrets.py
import os

# ❌ Vulnerable: Hardcoded secrets
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY", "")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY", "")

DB_USERNAME = os.environ.get("DB_USERNAME", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

def connect():
    print("Connecting with hardcoded credentials...")
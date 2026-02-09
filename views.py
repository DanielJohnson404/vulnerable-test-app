# hardcoded_secrets.py

# ❌ Vulnerable: Hardcoded secrets
AWS_ACCESS_KEY = __import__('os').environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = __import__('os').environ.get("AWS_SECRET_KEY")

DB_USERNAME = __import__('os').environ.get("DB_USERNAME")
DB_PASSWORD = __import__('os').environ.get("DB_PASSWORD")

def connect():
    print("Connecting with hardcoded credentials...")
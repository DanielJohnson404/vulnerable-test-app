# hardcoded_secrets.py

# ❌ Vulnerable: Hardcoded secrets
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

DB_USERNAME = "admin"
DB_PASSWORD = "P@ssw0rd123!"

def connect():
    print("Connecting with hardcoded credentials...")

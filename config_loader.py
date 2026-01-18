# config_loader.py
import os

def load_config():
    return {
        "db_user": os.getenv("DB_USER"),
        "db_password": os.getenv("DB_PASSWORD"),
        "db_host": os.getenv("DB_HOST", "localhost"),
    }

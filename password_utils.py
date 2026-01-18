# password_utils.py
import hashlib
import os

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100_000,
    )
    return salt.hex() + ":" + hashed.hex()

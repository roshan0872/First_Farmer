from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
ph = PasswordHasher()

def hash_password(password: str) -> str:
    """Hash a password using Argon2id."""
    return ph.hash(password)

def verify_password(hash_str: str, password: str) -> bool:
    """Verify a password against an Argon2 hash."""
    try:
        return ph.verify(hash_str, password)
    except (VerifyMismatchError, VerificationError, Exception):
        return False


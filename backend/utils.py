"""Utility functions for password hashing."""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Argon2 password hasher
_hasher = PasswordHasher(
    time_cost=settings.argon2_time_cost,
    memory_cost=settings.argon2_memory_cost,
    parallelism=settings.argon2_parallelism,
)


def hash_password(password: str) -> str:
    """
    Hash a password using Argon2id.
    
    Args:
        password: Plain text password (never logged)
        
    Returns:
        Hashed password string
    """
    return _hasher.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password_hash: Stored password hash
        password: Plain text password to verify
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        _hasher.verify(password_hash, password)
        return True
    except VerifyMismatchError:
        return False


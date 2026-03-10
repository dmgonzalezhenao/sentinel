"""
Security Utilities for Sentinel API.

This module handles password hashing and verification using the Passlib library 
with the Bcrypt algorithm. It ensures that sensitive credentials are never 
stored in plain text within the database.

Standards:
    - Algorithm: Bcrypt (Password-Based Key Derivation Function).
    - Salt: Automatically handled by Passlib's CryptContext.
    - Work Factor (Cost): 12 (default).
"""

# Import CryptContext to define encryption method
from passlib.context import CryptContext

# Define encryption method, and change it if gets insecure
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Function to get hashed password by using bcrypt schema.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The generated secure hash string.
    """
    # Return the hashed password
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Function to verify that the password provided by the
    user is the correct one.

    Args:
        password (str): The password input by the user.
        hashed_password (str): The hashed password from the database.

    Returns:
        bool: True if passwords match, False otherwise.
    """
    # Verify password
    return pwd_context.verify(password, hashed_password)
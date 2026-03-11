"""
Core Security Module for Sentinel API.

This module serves as the centralized security hub, managing credential 
integrity and session authentication. It provides utilities for:

1. Password Security: Hashing and verification using Passlib with the 
   Bcrypt algorithm to ensure zero-plain-text storage.
2. Token Management: Generation and validation of JSON Web Tokens (JWT) 
   for stateless authentication and Role-Based Access Control (RBAC).

Standards:
    - Password Hashing: Bcrypt (Cost factor: 12).
    - Session Auth: JWT (RFC 7519) using HS256 algorithm.
    - Security Principle: Least Privilege and Stateless Authentication.
"""

# Import CryptContext to define encryption method
from passlib.context import CryptContext

# Import jwt object
from jose import jwt

# Import objects for hinting
from datetime import datetime, timedelta, timezone
from typing import Any, Union

# Define encryption method, and change it if gets insecure
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- JWT Configuration ---
# Sentinel decryption key
SECRET_KEY = "PASSWORD_EXAMPLE"

# Encryption algorithm
ALGORITHM = "HS256"

# Time to token expires in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

def create_access_token(
    subject: Union[str, Any], 
    role: str, 
    expires_delta: timedelta | None = None) -> str:
    """
    Function to create a JSON Web Token and define
    its expiration time.

    Args:
        subject: User identifier (Usually ID)
        role: User role to define its permissions
        expires_delta: How much time is token active (Default None)
    
    Returns:
        JWT as a string
    """
    # Verify if there's time provided
    if expires_delta is not None:
        # Add expires delta to actual time
        expire = datetime.now(timezone.utc) + expires_delta

    # If there's no time provided just use default
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Define token data
    to_encode = {
        # Expiration time
        "exp": expire, 

        # User identity
        "sub": str(subject),

        # User role
        "role": role 
    }

    # Create token with crypted data with defined key
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Return 
    return encoded_jwt
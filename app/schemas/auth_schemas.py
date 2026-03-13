"""
Authentication Schemas Module for Sentinel API.

This module defines the Pydantic models used for data validation and 
serialization during the authentication process. It ensures that 
token-related responses and internal data structures follow the 
OAuth2 and JWT standards.
"""

# Import Pydantic Base Model
from pydantic import BaseModel

class Token(BaseModel):
    """
    Schema for the successful authentication response.

    This model represents the JSON object returned to the client 
    after a successful login, providing the necessary credentials 
    to access protected resources.

    Attributes:
        access_token (str): The signed JSON Web Token (JWT).
        token_type (str): The type of the token, typically "bearer".
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Internal schema for decoded token payload data.

    Used to transport and validate the information extracted from 
    a decrypted JWT during the authorization phase of a request.

    Attributes:
        user_id (Optional[str]): The unique identifier of the user (subject).
        role (Optional[str]): The access level or role assigned to the user.
    """
    user_id: str | None = None
    role: str | None = None
"""
Sentinel API Authentication Router.

This module handles the security layer of the application, specifically 
user authentication and JWT issuance. It provides the endpoints to 
validate credentials and manage secure access to protected resources.

Main functionality:
    - POST /login: Validates user credentials and returns a Bearer token.
"""

# Import APIRouter to determine paths as Sentinel endpoints
# The other objects are for hinting
from fastapi import APIRouter, Depends, Body, HTTPException

# Import sqalchemy session
from sqlalchemy.orm import Session

# Import Annotated object for type hinting
from typing import Annotated

# Import functions to verify password and create tokens
from app.core.security import verify_password, create_access_token

# Import function to access to the database
from app.database.config import get_db

# Import user's CRUD to validate login
from app.crud.user_crud import get_user_by_email as crud_get_user_by_email

# Import Pydantic UserLogin object
from app.schemas.user_schemas import UserLogin 

# Import Pydantic Token object
from app.schemas.auth_schemas import Token

# Import Sentinel logger
from app.core.logger import logger

# Create router with path auth
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token, status_code=200)
async def login(
    user_credentials: Annotated[UserLogin, Body(description="User credentials for authentication.")], 
    db: Session = Depends(get_db)
):
    """
    Authenticate a user and return a JWT access token.
    
    This endpoint verifies the email and password, and if valid, 
    returns a signed JWT for subsequent authorized requests.

    Args:
        user_credentials (UserLogin): Schema containing email and plain password.
        db (Session): Database session provided by dependency injection.
    
    Returns:
        User: The authenticated user record if credentials are valid.

    Raises:
        HTTPException: 401 error if email is not found or password does not match.
    """

    # Log login attempt
    logger.info(f"API: Login attempt for email: {user_credentials.email}")

    # Search user in the database
    user = crud_get_user_by_email(db=db, email=user_credentials.email)

    # Validate password match and user existence
    if (
        user is None or 
        not verify_password(user_credentials.password, str(user.hashed_password))
        or not bool(user.is_active)
        ):
        logger.warning(f"API: Login failed for email: {user_credentials.email}")
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create token
    access_token = create_access_token(
        subject=user.id, 
        role=getattr(user, "role", "user") 
    )

    # Log succesful login
    logger.info(f"API: User {user.username} successfully authenticated.")

    # Return token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
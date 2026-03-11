"""
Sentinel API Users Endpoint

This module provides user endpoint logic to main.py,
ensuring connection to database, and implementing
CRUD operations for users.
"""

# Import APIRouter to determine paths as Sentinel endpoints
# The other objects are for hinting
from fastapi import APIRouter, Depends, Body, HTTPException

# Import Pydantic User schemas
from app.schemas.user_schemas import UserLogin, UserCreate, UserResponse

# Import CRUD logic to use userss in the database
from app.crud.user_crud import (
    create_user as crud_create_user,
    get_user_by_email as crud_get_user_by_email)

# Import function to create a database session
from app.database.config import get_db

# Import hash password function for security
from app.core.security import verify_password

# Import User database object for type hinting
from app.database.models import User

# Import logger object for sentinel's logging
from app.core.logger import logger

# Import types for static analysis and type hinting
from typing import Annotated
from sqlalchemy.orm import Session

# Create router with path users
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=201, response_model=UserResponse)
async def register_user(
    user_data: Annotated[UserCreate, Body(description="The user data for registration.")], 
    db: Session = Depends(get_db)) -> User:
    """
    Register a new user in the Sentinel system.

    This endpoint validates the input data, checks for existing email 
    records to prevent duplicates, and persists the new user with a 
    hashed password.

    Args:
        user_data (UserCreate): Schema containing username, email, and plain password.
        db (Session): Database session provided by dependency injection.

    Returns:
        User: The newly created user object from the database.

    Raises:
        HTTPException: 400 error if the email is already registered.
    """
    # Log user register
    logger.info(f"Register attempt by user: {user_data.username}")

    # Check if user exists
    existing_user = crud_get_user_by_email(db=db, email=user_data.email)

    # Raise error if user already exists
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Validates the input and persists the user record
    return crud_create_user(db=db, user=user_data)

@router.post("/login", status_code=200, response_model=UserResponse)
async def login(
    user_credentials: Annotated[UserLogin, Body(description="User required data for login.")], 
    db: Session = Depends(get_db)) -> User:
    """
    Authenticate a user and start a session.

    Verifies if the provided email exists in the database and matches 
    the stored cryptographic hash of the password.

    Args:
        user_credentials (UserLogin): Schema containing email and plain password.
        db (Session): Database session provided by dependency injection.

    Returns:
        User: The authenticated user record if credentials are valid.

    Raises:
        HTTPException: 401 error if email is not found or password does not match.
    """
    # Log login
    logger.info(f"API: Login attempt for email: {user_credentials.email}")

    # Get user from database
    user = crud_get_user_by_email(db=db, email=user_credentials.email)

    # Check if the user exists and password
    # Transform to str for type hinting
    if not user or not verify_password(user_credentials.password, str(user.hashed_password)):
        # Log failed login
        logger.warning(f"API: Login failed for email: {user_credentials.email}")

        # Raise exception
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Log user login and return user
    logger.info(f"API: User {user.username} successfully authenticated.")
    return user
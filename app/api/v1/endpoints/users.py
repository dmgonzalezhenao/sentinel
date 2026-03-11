"""
Sentinel API Users Endpoint

This module provides user endpoint logic to main.py,
ensuring connection to database, and implementing
CRUD operations for users.
"""

# Import APIRouter to determine paths as Sentinel endpoints
# The other objects are for hinting
from fastapi import APIRouter, Depends, Body, Query, Path, HTTPException

# Import Pydantic User schemas
from app.schemas.user_schemas import UserRole, UserCreate, UserResponse

# Import CRUD logic to use userss in the database
from app.crud.user_crud import (
    create_user as crud_create_user,
    get_user_by_email as crud_get_user_by_email)

# Import function to create a database session
from app.database.config import get_db

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
    user_data: Annotated[UserCreate, Body(description="The user data for register.")], 
    db: Session = Depends(get_db)) -> User:
    """
    Asynchronous endpoint to register a new user in Sentinel.

    Receives data from user, validate it and persist user
    in the database.

    Returns:
    User object from the database.
    """
    # Log user register
    logger.info(f"Register attempt by user: {user_data.username}")

    # Check if user exists
    existing_user = crud_get_user_by_email(db=db, email=user_data.email)

    # Raise error if user alread exists
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Persist the validated user and return new object
    return crud_create_user(db=db, user=user_data)

@router.post("/login")
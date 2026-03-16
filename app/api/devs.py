"""
Global API Dependencies.

This module provides reusable dependencies for FastAPI endpoints, 
handling authentication, authorization (RBAC), and database session 
management across all API versions.
"""

# Import Depends to persistance db connections and JWt
from fastapi import Depends, HTTPException

# Import function to allow authentication
from fastapi.security import OAuth2PasswordBearer

# Import jwt object and JWTError for exceptions
from jose import jwt, JWTError

# Import Session object
from sqlalchemy.orm import Session

# Import settings to get Sentinel core data
from app.core.config import settings

# Impor function to get connection to database
from app.database.config import get_db

# Import get_user_by_id to validate user
from app.crud.user_crud import get_user_by_id

# Import TokenData object to validate input Token
from app.schemas.auth_schemas import TokenData

# Import User object for hinting
from app.database.models import User

# Import Sentinel's logger
from app.core.logger import logger

# Search token in header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency to validate the JWT and return the current user.
    """
    try:
        # Decodify token and get user_id
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int | None = payload.get("sub")

        # Validate token payload data
        if user_id is None:
            # Log error
            logger.error("Security: Token decode successful but 'sub' claim is missing.")

            # Raise exception
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        # Get user's id from token data
        token_data = TokenData(user_id=user_id)
    
    # Raise exception if there's a JWT error
    except JWTError as e:
        # Log warning
        logger.warning(f"Security: Token validation failed: {str(e)}")

        # Raise exception
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    # Validate id from token
    if token_data.user_id is None:
        logger.error("Security: Token valid but 'sub' (user_id) is missing")
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )
    
    # Get user object with token id (May raise error by hinting)
    user = get_user_by_id(db, id=token_data.user_id)
    
    # Validate user exists
    if user is None:
        # log error user was not found
        logger.error(f"Security: User ID {token_data.user_id} not found in database.")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate if user is active
    if not bool(user.is_active):
        # Log user block access and raise exception
        logger.warning(f"Security: Blocked access attempt from inactive user: {user.email}")
        raise HTTPException(status_code=400, detail="Inactive user")
        
    # Return user object
    return user

def RoleChecker(allowed_roles: list[str]):
    """
    Factory that generates role-specific validation dependencies.
    Implements RBAC by checking the user's role against a whitelist.
    """
    def validator(current_user=Depends(get_current_user)):
        """
        Wrapper validator function to validate user role

        Args:
            Token from user's session.
        """

        # Check user's role is valid
        if current_user.role not in allowed_roles:
            # Log user tried to access with invalid role
            logger.warning(
                f"Security: User {current_user.email} (Role: {current_user.role}) "
                f"attempted to access an endpoint requiring: {allowed_roles}"
            )
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        # return current user
        return current_user
    
    # Return wrapper validator
    return validator
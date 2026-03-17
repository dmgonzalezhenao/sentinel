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

# Imports for hinting
from app.database.models import User
from typing import Annotated

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

class RoleChecker:
    """
    Role validation dependency for Project Sentinel.

    This class acts as a FastAPI dependency that verifies if the 
    authenticated user possesses one of the allowed roles before 
    granting access to a specific endpoint.
    """

    def __init__(self, allowed_roles: list[str]):
        """
        Initializes the checker with a list of authorized roles.

        Args:
            allowed_roles (List[str]): List of roles (ADMIN, SERVICE, VIEWER) allowed to access.
        """
        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: Annotated[User, Depends(get_current_user)]) -> User:
        """
        Executes identity and role validation.

        This method is automatically called by FastAPI when used within Depends().
        By returning 'User', it ensures the IDE recognizes 'current_user' as an 
        instance, resolving SQLAlchemy 'Column[int]' typing conflicts.

        Args:
            current_user (User): User object retrieved via JWT token.

        Returns:
            User: The validated user object if permissions are met.

        Raises:
            HTTPException: 403 Forbidden if the user role is not in the allowed list.
        """
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Role required: {', '.join(self.allowed_roles)}"
            )
        return current_user
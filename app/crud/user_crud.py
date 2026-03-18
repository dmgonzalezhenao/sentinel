"""
Sentinel API CRUD operations for users.

This module implements the logic for interacting with the database,
including users register and log in.
"""
# Import session object to access the database
from sqlalchemy.orm import Session

# Import User and Organization classes (users and organizations tables from database)
from app.database.models import User, Organization

# Import Pydantic schemas for users register and log in
from app.schemas.user_schemas import UserCreate, UserResponse

# Import hash password function
from app.core.security import get_password_hash

# Import Sentinel's logger
from app.core.logger import logger

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Function to get user from database by its email.
    It's used to find user in login.
    """
    # Query the User table filtering by the provided email
    result = db.query(User).filter(User.email == email).first()

    # Check if there's result
    if result:
        logger.info(f"CRUD: Successfully retrieved user record with email: {email}")
    else:
        logger.warning(f"CRUD: User with email: {email} was not found")

    # Return result
    return result

def get_user_by_id(db: Session, id: int) -> User | None:
    """
    Function to get user from database by its id.
    It's used in dependencies to get validate user.
    """
    # Query the User table filtering by the provided id
    result = db.query(User).filter(User.id == id).first()

    # Check if there's result
    if result:
        logger.info(f"CRUD: Successfully retrieved user record with id: {id}")
    else:
        logger.warning(f"CRUD: User with id: {id} was not found")

    # Return result
    return result

def create_user(db: Session, user: UserCreate) -> User:
    """
    Function that creates a new user in database with its hashed password.
    """
    # Get organization from new user
    org = db.query(Organization).filter(
        Organization.id == user.organization_id, 
        Organization.is_active == True
    ).first()

    # Validate organization exists
    if not org:
        logger.error(f"CRUD: Cannot create user. Organization {user.organization_id} not found or inactive.")
        raise ValueError("Invalid or inactive organization")
    
    # Hash password
    hashed_password = get_password_hash(user.password)

    # Instance user
    db_user = User(
        username=user.username, 
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
        organization_id=user.organization_id
    )

    try: 
        # Log attempt to insert data in database
        logger.info(f"CRUD: Attempting to persist user: {user.username}")

        # Add changes and commit
        db.add(db_user)
        db.commit()

        # Refresh instance attributes
        db.refresh(db_user)

        # Log successful user creation
        logger.info(f"CRUD: Successfully created user with username: {user.username}")

        # Return object with new data
        return db_user
    
    # Exception if there's a connection error
    except Exception as e:
        # Log error in Sentinel's logger
        logger.error(f"CRUD: Failed to create user: {str(e)}")

        # Avoid every change to the database to
        # avoid errors or corrupt data insertions
        db.rollback()

        # Raise error to main
        raise e
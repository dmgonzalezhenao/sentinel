"""
Sentinel API CRUD operations for users.

This module implements the logic for interacting with the database,
including users register and log in.
"""
# Import session object to access the database
from sqlalchemy.orm import Session

# Import User class (users table from database)
from app.database.models import User

# Import Pydantic schemas for users register and log in
from app.schemas.user_schemas import UserCreate, UserResponse

# Import hash password function
from app.core.security import get_password_hash

# Import Sentinel's logger
from app.core.logger import logger

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Function to get user from database by its email.
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

def create_user(db: Session, user: UserCreate):
    """
    Function that creates a new user in database with its hashed password.
    """
    # Hash password
    hashed_password = get_password_hash(user.password)

    # Instance user
    db_user = User(
        username=user.username, 
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        is_active=True
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
# Import column object and column types from SQLAlchemy
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey

# Import relationship to optimize joins
from sqlalchemy.orm import relationship

# Function to get time automatically
from sqlalchemy.sql import func

# Import Base object to create Log table
from app.database.config import Base

class User(Base):
    """
    Represents an authenticated entity within the Sentinel system.
    
    This model manages user identity, secure credential storage, and 
    access control levels. It serves as the link between individual 
    accounts and their respective organizations.

    Attributes:
        id (int): Primary key, auto-incrementing unique identifier.
        username (str): Unique identifier for login and display.
        email (str): Unique contact and identification address.
        hashed_password (str): Securely stored password (salted and hashed).
        is_active (bool): Flag to enable or disable account access.
        role (str): Access level (ADMIN, SERVICE, or VIEWER).
        created_at (datetime): Timestamp of account creation.
        updated_at (datetime): Automatically updated timestamp of the last modification.
        organization_id (int): Foreign key linking the user to their organization.
    """

    # Define table's name
    __tablename__ = "users"

    # Define user attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), nullable=False, default="VIEWER")

    # Timestamps for auditing.
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

    # Foreign key to organizations table
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)

    # Define relationship to organization and logs as "author"
    organization = relationship("Organization", back_populates="users")
    logs = relationship("Log", back_populates="author")
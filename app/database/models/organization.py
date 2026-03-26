# Import column object and column types from SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean

# Import relationship to optimize joins
from sqlalchemy.orm import relationship

# Import JSONB attribute to save metadata (Only in PostgreSQL)
from sqlalchemy.dialects.postgresql import JSONB

# Function to get time automatically
from sqlalchemy.sql import func

# Import Base object to create Log table
from app.database.config import Base

class Organization(Base):
    """
    Represents the top-level tenancy unit within the Sentinel ecosystem.
    
    This model acts as a container for users and logs, ensuring logical 
    data isolation. It defines the workspace boundaries for different 
    teams or corporate entities.

    Attributes:
        id (int): Primary key, auto-incrementing unique identifier.
        name (str): The formal name of the company or team (e.g., 'Acme Corp').
        slug (str): A URL-friendly version of the name (e.g., 'acme-corp') used for routing.
        is_active (bool): Operational status of the organization.
        created_at (datetime): Timestamp of record initialization.
        updated_at (datetime): Automatically updated timestamp of the latest change.
    """
    
    # Define table name
    __tablename__ = "organizations"

    # Define organization attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

    # Timestamps for auditing.
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

    # Create relationship to optimize queries from organizations to users and logs
    users = relationship("User", back_populates="organization")
    logs = relationship("Log", back_populates="organization")
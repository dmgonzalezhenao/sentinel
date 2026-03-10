"""
Sentinel API Database classes

This module creates and configures the structure of the database
in Neon by using SQLAlchemy to create classes and its attributes.
By now this is the initial structure:

Table: logs
-----------------------------------------------------------
| Column       | Type      | Note                         |
|--------------|-----------|------------------------------|
| id           | Integer   | PK, Autoincrement            |
| service_name | String    | Indexed, e.g. 'web-app'      |
| log_level    | String    | INFO, ERROR, etc.            |
| message      | String    | Main description             |
| log_metadata | JSONB     | Flexible software-specific   |
| timestamp    | DateTime  | Server default now           |
| user_id      | Integer   | FK -> users(id)              |
-----------------------------------------------------------

Table: users
--------------------------------------------------------------------
| Column          | Type      | Note                               |
|-----------------|-----------|------------------------------------|
| id              | Integer   | PK, Autoincrement                  |
| username        | String    | Indexed, e.g. 'mariogon'           |
| email           | String    | Indexed, e.g. 'example@gmail.com   |
| hashed_password | String    | Hash value                         |
| is_active       | Boolean   | Default=True                       |
--------------------------------------------------------------------

"""

# Import column object and column types from SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

# Import JSONB attribute to save metadata (Only in PostgreSQL)
from sqlalchemy.dialects.postgresql import JSONB

# Function to get time automatically
from sqlalchemy.sql import func

# Import Base object to create Log table
from .config import Base

# Create Log class
class Log(Base):
    """
    Log Class from Sentinel API Database
    
    Once the log data is validated, the data mentioned in 
    the Docstring is recorded in a column of this table.
    """
    # Define table name
    __tablename__ = 'logs'

    # Define log attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(50), index=True)
    log_level = Column(String(20), nullable=False)
    message = Column(String(1000), nullable=False)
    log_metadata = Column(JSONB, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Create foreign key that references users table
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

# Create users class
class User(Base):
    """
    Users class from Sentinel API database

    Once a user is registered, data is saved
    in this table in the database.
    """

    # Define table name
    __tablename__ = "users"

    # Define user attributes
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps for auditory
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
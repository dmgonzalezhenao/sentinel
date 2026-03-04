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
| message      | Text      | Main description             |
| metadata     | JSONB     | Flexible software-specific   |
| timestamp    | DateTime  | Server default now           |
-----------------------------------------------------------

"""

# Import column object and column types from SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime

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
    
    Once the data is validated, the data mentioned in 
    the Docstring is recorded in a column of this table.
    """
    # Define table name
    __tablename__ = 'logs'

    # Define attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(50), index=True)
    log_level = Column(String(20), nullable=False)
    message = Column(String(1000), nullable=False)
    log_metadata = Column(JSONB, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
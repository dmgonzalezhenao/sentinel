"""
Sentinel API Database Models v0.5.0

Architecture: Multi-tenant Log Aggregator.
Engine: PostgreSQL (Neon) via SQLAlchemy ORM.

Relationships:
- Organization (1) <---> (N) Users (Admin, Viewer, Service)
- Organization (1) <---> (N) Logs (Enforced Isolation)
- User (1) <---> (N) Logs (Authorship traceability)

Table: logs
--------------------------------------------------------------
| Column          | Type      | Note                         |
|-----------------|-----------|------------------------------|
| id              | Integer   | PK, Autoincrement            |
| service_name    | String    | Indexed, e.g. 'web-app'      |
| log_level       | String    | INFO, ERROR, etc.            |
| message         | String    | Main description             |
| log_metadata    | JSONB     | Flexible software-specific   |
| timestamp       | DateTime  | Server default now time      |
| user_id         | Integer   | FK -> users(id)              |
| organization_id | Integer   | FK -> organizations(id)      |
--------------------------------------------------------------

Table: users
----------------------------------------------------------------------------
| Column          | Type      | Note                                       |
|-----------------|-----------|--------------------------------------------|
| id              | Integer   | PK, Autoincrement                          |
| username        | String    | Indexed, Unique, e.g. 'mariogon'           |
| email           | String    | Indexed, Unique, e.g. 'example@gmail.com   |
| hashed_password | String    | Hash value                                 |
| is_active       | Boolean   | Default=True                               |
| role            | String    | ADMIN, SERVICE and VIEWER                  |
| created_at      | DateTime  | Server default now time                    |
| updated_at      | DateTime  | Server default now time                    |
| organization_id | Integer   | FK -> organizations(id)                    |
----------------------------------------------------------------------------
 
Table: organizations
-----------------------------------------------------------------
| Column      | Type      | Note                                |
-----------------------------------------------------------------
| id          | Integer   | PK, Autoincrement                   |
| name        | String    | Indexed, Unique, e.g. "Acme Corp"   |
| slug        | String    | Indexed, Unique, eg.g "acme"        |
| is_active   | Boolean   | Default=True                        |
| created_at  | DateTime  | Server default now time             |
| updated_at  | DateTime  | Server default now time             |
-----------------------------------------------------------------
"""

# Import column object and column types from SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

# Import relationship to optimize joins
from sqlalchemy.orm import relationship

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
    log_level = Column(String(20), index=True, nullable=False)
    message = Column(String(1000), nullable=False)
    log_metadata = Column(JSONB, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Create foreign keys that reference user and organization
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    # Optimize relationships to log's organization and log's author
    organization = relationship("Organization", back_populates="logs")
    author = relationship("User", back_populates="logs")

# Create users class
class User(Base):
    """
    Users class from Sentinel API database

    Once a user is registered, data is persisted
    in this table in the database.
    """

    # Define table name
    __tablename__ = "users"

    # Define user attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), nullable=False, default="VIEWER")

    # Timestamps for auditing.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Foreign key to organizations table
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    # Define relationship to organization and logs as "author"
    organization = relationship("Organization", back_populates="users")
    logs = relationship("Log", back_populates="author")

class Organization(Base):
    """
    Organization class from Sentinel API Database

    This table allows to viewers and services to
    view and create same logs respectively.
    """

    # Define table name
    __tablename__ = "organizations"

    # Define organization attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

    # Timestamps for auditing.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Create relationship to optimize queries from organizations to users and logs
    users = relationship("User", back_populates="organization")
    logs = relationship("Log", back_populates="organization")
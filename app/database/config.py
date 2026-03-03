"""
Sentinel API connection to database.

This module configures the connection to the PostgreSQL database in Neon.
It initializes the SQLAlchemy engine, the session factory, and the 
declarative base for the ORM models.
"""
# os module to get url from an environmental file
import os

# Import create engine to config connection from Python to the database
from sqlalchemy import create_engine

# Import declarative base from SQLAlchemy to handle the classes of the database in models.py
from sqlalchemy.ext.declarative import declarative_base

# Import session maker to create multiple sessions to connect to the database
from sqlalchemy.orm import sessionmaker

# Function to load enviromental files
from dotenv import load_dotenv

# Load environment variables from the .env file in the root directory
load_dotenv()

# Fetch the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Explicit check to satisfy the type checker and ensure security
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in the environment variables")

# Create the SQLAlchemy engine. 
# 'pool_pre_ping' ensures the connection is still valid before use.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal will be used to create a new database session for each request
# Autocommit as false ensures that data won't be modified until everything goes good and there's no
# errors connection or invalid or corrupt data
# Autoflush as false ensures that Python won't send old queries to the database
# binds the session to the specified engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all SQLAlchemy models to inherit from
Base = declarative_base()

def get_db():
    """
    Dependency that provides a dedicated database session for each request.

    This generator manages the session lifecycle:
    1. Opens a new SQLAlchemy session using SessionLocal.
    2. Yields the session object to the calling FastAPI endpoint.
    3. Suspends execution until the request-response cycle is complete.
    4. Closes the session in the 'finally' block to ensure resources 
       are released back to the connection pool, even if an error occurs.

    Yields:
    Session: An active SQLAlchemy database session.
    """
    # Create local session
    db = SessionLocal()

    # Try to connect to database
    try:
        # Suspend execution and return connection
        yield db

    # Finally close connection
    finally:
        db.close()
"""
Sentinel API connection to database.

This module configures the connection to the PostgreSQL database in Neon.
It initializes the SQLAlchemy engine, the session factory, and the 
declarative base for the ORM models.
"""
# Import settings object to get database url
from app.core.config import settings

# Import create engine to config connection from Python to the database
from sqlalchemy import create_engine

# Import declarative base from SQLAlchemy to handle the classes of the database in models.py
from sqlalchemy.ext.declarative import declarative_base

# Import sessionmaker to create multiple sessions to connect to the database
from sqlalchemy.orm import sessionmaker

# Import sentinel logger
from app.core.logger import logger

# Fetch the database URL from settings object
DATABASE_URL: str | None = settings.DATABASE_URL

# Explicit check to satisfy the type checker and ensure security
if DATABASE_URL is None:
    # Log error as critical
    logger.critical("DATABASE_URL is missing in environment variables!")

    # Raise value error
    raise ValueError("DATABASE_URL is not set in the environment variables")

# Create the SQLAlchemy engine. 
# 'pool_pre_ping' ensures the connection is still valid before use.
# pool_size is the min number of connections opened by default
# max_overfloe is the max number of connections opened in peak
# pool_timeout defines 30 seconds as timeout when all connections are in use
# pool_recycle refresh connections every 30 minutes
engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True,
    pool_size=20,           
    max_overflow=10,      
    pool_timeout=30,      
    pool_recycle=1800
)

# SessionLocal will be used to create a new database session for each request
# Autocommit as false ensures that data won't be modified until everything goes good and there's no
# connection errors or invalid or corrupt data
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

    # Log session aperture in Sentinel's log
    logger.info("DB: opening new session for request")

    # Try to connect to database
    try:
        # Suspend execution and return connection
        yield db

    # Exception 
    except Exception as e:
        # Log error
        logger.error(f"Database session error during request cycle: {str(e)}")
        raise e

    # Finally close connection
    finally:
        # Log session close
        logger.info("DB: closing session and returning to pool")
        db.close()
"""
Database utility functions for the Sentinel API.

This module contains helper functions for database connectivity checks, 
data formatting, and other reusable database-related logic that supports 
the main application endpoints.
"""

# Import text format to check database connection
from sqlalchemy import text

# Import Session object
from sqlalchemy.orm import Session

# Import Sentinel logger
from app.core.logger import logger

def check_db_connection(db: Session) -> bool:
    """
    Function that makes a query to the database and
    return True if doesn't raise an exception.
    """
    try:
        # Log connection attempt
        logger.info("Database health check initiated.")

        # Execute SELECT 1
        db.execute(text("SELECT 1"))

        # Return True
        return True
    
    # Return false if there's an exception
    except Exception as e:
        # Log error
        logger.error(f"Database health check FAILED: {e}")

        return False
    
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

def check_db_connection(db: Session) -> bool:
    """
    Function that makes a query to the database and
    return True if doesn't raise an exception.
    """
    try:
        # Execute SELECT 1
        db.execute(text("SELECT 1"))

        # Return True
        return True
    
    # Return false if there's an exception
    except Exception:
        return False
    
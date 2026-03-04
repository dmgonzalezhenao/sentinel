"""
Sentinel API CRUD Module for logs

This module maps log schema from Pydantic to a log class
in the database and inserts the log once it is validated.
"""
# Import session object to access the database
from sqlalchemy.orm import Session

# Import Log class (logs table from database)
from app.database.models import Log

# Import Pydantic schema for log data validation
from app.schemas.log_schema import LogCreate 

def create_log(db: Session, log_data: LogCreate) -> Log:
    """
    Function to create a SQLAlchemy Log object using the data
    from log_data and insert log in logs table in the database.
    """
    # Dump data from log_data and create the Log object
    db_log = Log(**log_data.model_dump()) 

    try:
        # Prepare data insertion in the database
        # Useful if something goes wrong, don't add anything to the database
        db.add(db_log)

        # Commit data in the database
        db.commit()

        # Get the log with its id and new timestamp
        db.refresh(db_log)

        # Return object with new data
        return db_log
    
    # Exception if connection fails
    except Exception as e:
        # Avoid every change to the database to
        # avoid errors or corrupt data insertions
        db.rollback()

        # Raise error to main
        raise e
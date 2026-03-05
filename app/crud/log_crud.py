"""
Sentinel API CRUD operations for logs.

This module implements the logic for interacting with the database,
including log ingestion, record retrieval, and specialized filtering 
based on service identifiers and severity levels.
"""

# Import session object to access the database
from sqlalchemy.orm import Session

# Import Log class (logs table from database)
from app.database.models import Log

# Import Pydantic schema for logs input and output
from app.schemas.log_schemas import LogCreate, LogResponse

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
    
def get_logs(
    db: Session, 
    service_name: str | None = None, 
    log_level: str | None = None, 
    limit: int = 10
) -> list[Log]:
    """
    Retrieve a collection of logs with optional filtering and pagination.
    """

    # Prepares query for the database (SELECT * FROM logs)
    query = db.query(Log)

    # If there's service_name provided
    if service_name is not None:
        # Filter data by service_name
        query = query.filter(Log.service_name == service_name)

    # If there's log level provided
    if log_level is not None:
        # Filter data by log_level
        query = query.filter(Log.log_level == log_level)

    # Return query to the database with the limit
    return query.limit(limit).all()

def get_logs_by_id(
    db: Session,
    log_id: int 
) -> Log | None:
    """
    Retrieve a specific log by its id.
    """
    return db.query(Log).filter(Log.id == log_id).first()
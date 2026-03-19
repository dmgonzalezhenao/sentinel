"""
Sentinel API CRUD operations for logs.

This module implements the logic for interacting with the database,
including log ingestion, record retrieval, and specialized filtering 
based on service identifiers and severity levels.
"""

# Import session object to access the database
from sqlalchemy.orm import Session

# Import Log and User classes (logs and users tables from database)
from app.database.models import Log, User

# Import Pydantic schema for logs input and output
from app.schemas.log_schemas import LogCreate, LogResponse

# Import Sentinel's logger
from app.core.logger import logger

def create_log(db: Session, log_data: LogCreate, current_user: User) -> Log:
    """
    Function to create a SQLAlchemy Log object using the data
    from log_data and insert log in logs table in the database.
    """
    # Dump data from log_data and create the Log object
    db_log = Log(
        **log_data.model_dump(), 

        # Extract data from user object
        user_id=current_user.id,
        organization_id=current_user.organization_id
    ) 

    try:
        # Log attempt to insert data in database
        logger.info(f"CRUD: Attempting to persist log for {log_data.service_name} from Org ID: {current_user.organization_id}")

        # Prepare data insertion in the database
        # Useful if something goes wrong, don't add anything to the database
        db.add(db_log)

        # Commit data in the database
        db.commit()

        # Get the log with its id and new timestamp
        db.refresh(db_log)

        # Log succesful log redords
        logger.info(f"CRUD: Log record created successfully with ID: {db_log.id}")

        # Return object with new data
        return db_log
    
    # Exception if connection fails
    except Exception as e:
        # Log error in Sentinel's logger
        logger.error(f"CRUD: Failed to create log entry: {str(e)}")

        # Avoid every change to the database to
        # avoid errors or corrupt data insertions
        db.rollback()

        # Raise error to main
        raise e
    
def get_logs(
    db: Session, 
    current_user: User,
    user_id: int | None = None,
    service_name: str | None = None, 
    log_level: str | None = None, 
    limit: int = 10
) -> list[Log]:
    """
    Retrieve a collection of logs with optional filtering and pagination.
    """
    # Log database query
    logger.info(
        f"CRUD: Fetching logs | Requester: {current_user.email} (Org: {current_user.organization_id}) | "
        f"Filters -> user_filter: {user_id}, service: {service_name}, level: {log_level}"
    )

    # Prepares query for the database (SELECT * FROM logs)
    query = db.query(Log)

    # Check user's role for filtering
    if str(current_user.role) != "ADMIN":
        # Filter by organization
        query = query.filter(Log.organization_id == current_user.organization_id)

        # Log filtering
        logger.debug(f"CRUD: Security isolation applied for Org {current_user.organization_id}")
    
    # Log admin access
    else:
        logger.info("CRUD: Admin bypass - accessing global logs")

    # Filter by user_id
    if user_id is not None:
        query = query.filter(Log.user_id == user_id)

    # If there's service_name provided
    if service_name is not None:
        # Filter data by service_name
        query = query.filter(Log.service_name == service_name)

    # If there's log level provided
    if log_level is not None:
        # Filter data by log_level
        query = query.filter(Log.log_level == log_level)

    # Return ordered query
    results = query.order_by(Log.id.desc()).limit(limit).all()

    # Log result in Sentinel's logger
    logger.info(f"CRUD: Successfully retrieved {len(results)} log records.")

    # Return result
    return results

def get_logs_by_id(
    db: Session,
    current_user: User,
    log_id: int
) -> Log | None:
    """
    Retrieve a specific log by its id. Restricted to organization
    for viewers.
    """
    # Log query to Sentinel
    logger.info(f"CRUD: User {current_user.email} attempting to fetch Log ID: {log_id}")

    # Create query
    query = db.query(Log).filter(Log.id == log_id)

    # Filter by organization if isn't an admin user
    if str(current_user.role) != "ADMIN":
        query = query.filter(Log.organization_id == current_user.organization_id)
    
    # Execute query
    result = query.first()

    # Check result and log succesful retrieve or failure
    if result is not None:
        logger.info(f"CRUD: Successfully retrieved log {log_id}")
    else:
        logger.warning(f"CRUD: Log {log_id} not found or access denied for Org {current_user.organization_id}")

    # Return log
    return result
"""
Sentinel API CRUD operations for logs.

This module implements the logic for interacting with the database,
including log ingestion, record retrieval, and specialized filtering 
based on service identifiers and severity levels.
"""

# Import session object to access the database
# Import joinedload to make joins automatically
from sqlalchemy.orm import Session, joinedload

# Import Log and User classes (logs and users tables from database)
from app.database.models import Log, User

# Import Pydantic schema for logs input and output
from app.schemas.log_schemas import LogCreate, LogResponse

# Import Sentinel's logger
from app.core.logger import logger

def create_log(db: Session, log_data: LogCreate, current_user: User) -> Log:
    """
    Creates and persists a new Log entry in the database.

    Args:
        db (Session): The database session object.
        log_data (LogCreate): Pydantic schema containing the log details (service, level, etc.).
        current_user (User): The user object representing the entity creating the log.

    Returns:
        Log: The newly created SQLAlchemy Log object with its generated ID and timestamp.

    Raises:
        Exception: If there is a database connection error or constraint violation. 
                 Performs a rollback to ensure data integrity.
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
    risk_score: int | None = None,
    is_anomaly: bool | None = None,
    limit: int = 10
) -> list[Log]:
    """
    Retrieves a collection of logs with multi-parameter filtering and security isolation.

    This function automatically restricts data access based on the user's role. 
    Non-admin users can only see logs from their own organization.

    Args:
        db (Session): The database session object.
        current_user (User): The user requesting the logs.
        user_id (int, optional): Filter logs by a specific author ID.
        service_name (str, optional): Filter logs by the source service name.
        log_level (str, optional): Filter by severity (INFO, DEBUG, ERROR, etc.).
        risk_score (int, optional): Filter by a specific security risk value.
        is_anomaly (bool, optional): Filter by anomaly detection flag.
        limit (int): Maximum number of records to return. Defaults to 10.

    Returns:
        list[Log]: A list of Log objects ordered by ID descending (most recent first).
    """
    # Log database query
    logger.info(
        f"CRUD: Fetching logs | Requester: {current_user.email} (Org: {current_user.organization_id}) | "
        f"Filters -> user_filter: {user_id}, service: {service_name}, level: {log_level}"
    )

    # Prepares query with Eager Loading to avoid N+1
    query = db.query(Log).options(
        joinedload(Log.author),     
        joinedload(Log.organization) 
    )

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

    # If theres risk score provided
    if risk_score is not None:
        # Filter data
        query = query.filter(Log.risk_score == risk_score)
    
    # If there's anomaly check provided
    if is_anomaly is not None:
        # Filter data
        query = query.filter(Log.is_anomaly == is_anomaly)
        
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
    Retrieves a single log record by its unique identifier.

    Non-admin users are restricted to fetching logs within their own organization.

    Args:
        db (Session): The database session object.
        current_user (User): The user requesting the specific log.
        log_id (int): The primary key ID of the log to retrieve.

    Returns:
        Log | None: The Log object if found and authorized, otherwise None.
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

def get_multiple_logs(
    db: Session,
    current_user: User,
    limit: int | None = 10000
) -> list[Log]:
    """
    Retrieves a high-volume bulk of logs for global administrative purposes.

    Designed for administrative oversight, analytics, and Machine Learning training. 
    It bypasses organizational filters to provide a global view of the infrastructure.

    Args:
        db (Session): The database session object.
        current_user (User): The admin user requesting the bulk data.
        limit (int, optional): Maximum number of logs to fetch. Defaults to 10000.

    Returns:
        list[Log]: A list of Log objects from across all organizations.
    """
    # Log bulk data in sentinel
    logger.info(f"CRUD: Admin {current_user.username} requesting a bulk of {limit} logs.")

    # Make query
    results = db.query(Log).order_by(Log.id.desc()).limit(limit).all()

    # Log result in Sentinel's logger
    logger.info(f"CRUD: Successfully retrieved {len(results)} log records.")

    # Return result
    return results
"""
Sentinel API Logs Endpoint

This module provides log endpoint logic to main.py,
ensuring connection to database, and implementing
CRUD operations for logs.
"""

# Import APIRouter to determine paths as Sentinel endpoints
# The other objects are for hinting
from fastapi import APIRouter, Depends, Body, Query, Path, HTTPException

# Import Pydantic Logs Schemas
from app.schemas.log_schemas import LogLevel, LogCreate, LogResponse

# Import CRUD logic to use logs in the database
from app.crud.log_crud import (
    create_log as crud_save_log, 
    get_logs as crud_get_logs, 
    get_logs_by_id as crud_get_logs_by_id)

# Import function to create a database session
from app.database.config import get_db

# Import dependencies to handle RBAC
from app.api.devs import get_current_user, RoleChecker

# Import Log and User database models for type hinting
from app.database.models import Log, User

# Import logger object for sentinel's logging
from app.core.logger import logger

# Import types for static analysis and type hinting
from typing import Annotated
from sqlalchemy.orm import Session

# Create router with path logs
router = APIRouter(prefix="/logs", tags=["Logs"])

@router.post("/", status_code=201, response_model=LogResponse)
async def ingest_log(
    log: Annotated[LogCreate, Body(description="The log data to be ingested")], 
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["ADMIN", "SERVICE"]))
) -> Log:
    """
    Receives logs from external services, validates them, 
    and persists them to the database.

    Args:
        log (LogCreate): Schema containing service name, level, and message.
        db (Session): Database session provided by dependency injection.
        current_user (User): Authenticated user with SERVICE or ADMIN role.

    Returns:
        Log: The persisted log record object.
    
    Raises:
        HTTPException: 401 if token is invalid.
        HTTPException: 403 if user role is not authorized.
    """
    # Log the ingestion
    logger.info(f"Ingestion request received from service: {log.service_name}")

    # Persist the validated log and return the database record
    return crud_save_log(db=db, log_data=log)

@router.get("/", response_model=list[LogResponse])
async def read_logs(
    db: Session = Depends(get_db),
    service_name: Annotated[str | None, Query(max_length=50)] = None,
    log_level: Annotated[LogLevel | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    current_user: User = Depends(RoleChecker(["ADMIN", "VIEWER"]))
    ) -> list[Log]:
    """
    Retrieve a filtered list of logs from the database.

    This endpoint allows for searching logs based on the originating service 
    name and the severity level. Supports pagination.

    Args:
        service_name (str, optional): The name of the service that generated the log.
        log_level (str, optional): The severity level of the log (e.g., INFO, ERROR).
        limit (int): Maximum number of log records to return (Default: 10, Max: 100).
        db (Session): Database session dependency.
        current_user (User): Authenticated user with VIEWER or ADMIN role.

    Returns:
        list[LogResponse]: A list of log records matching the criteria.
    
    Raises:
        HTTPException: 403 if user lacks required permissions.
        HTTPException: 500 if there's a database connection error.
    """
    # Log read logs in Sentinel's logger
    logger.info(f"Bulk log retrieval requested. Filters: service={service_name}, level={log_level}")

    # Return the logs list with get logs function
    return crud_get_logs(db, service_name=service_name, log_level=log_level, limit=limit)

@router.get("/{log_id}", response_model=LogResponse)
async def read_log(
    log_id: Annotated[int, Path(ge=1, description="The unique ID of the log record")],
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["ADMIN", "VIEWER"]))
) -> Log:
    """
    Retrieve a specific log record by its unique identifier.

    Fetches the full details of a single log entry. If the ID does not 
    match any record, a 404 error is returned.

    Args:
        log_id (int): The primary key of the log to be retrieved (min: 1).
        db (Session): Database session dependency.
        current_user (User): Authenticated user with VIEWER or ADMIN role.

    Returns:
        LogResponse: The complete log object if found.

    Raises:
        HTTPException: 404 if the log record does not exist in the database.
        HTTPException: 403 if user is not authorized.
    """

    # Log retrieval in Sentinel's logger
    logger.info(f"Single log retrieval requested for ID: {log_id}")

    # Get log from the database
    db_log = crud_get_logs_by_id(db, log_id=log_id)
    
    # Check if log exists
    if db_log is None:
        # Log warning message
        logger.warning(f"Log ID {log_id} not found")

        # Raise not found exception
        raise HTTPException(status_code=404, detail="Log record not found")
    
    # Return log
    return db_log
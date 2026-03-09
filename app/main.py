"""
Main entry point for the Sentinel API.

This module initializes the FastAPI application and defines the core routes
for log ingestion and system health monitoring.
"""
# Import FastAPI object
from fastapi import FastAPI, Depends, Body, Path, Query, HTTPException

# Import LogCreate object to get log data schema
from app.schemas.log_schemas import LogLevel, LogCreate, LogResponse

# Import function to create a database session
from app.database.config import get_db

# Import utils logic from database to check connection
from app.database.utils import check_db_connection

# Import CRUD logic to save logs in the database
from app.crud.log_crud import create_log as crud_save_log, get_logs as crud_get_logs, get_logs_by_id as crud_get_logs_by_id

# Import types for static analysis and type hinting
from datetime import datetime, timezone
from typing import Any, Annotated
from sqlalchemy.orm import Session

# Const to log Sentinel version
VERSION = "0.1.0"
# Initialize the FastAPI application with metadata
app = FastAPI(
    title="Project Sentinel",
    description="AI-Ready Infrastructure for Log Observability and Anomaly Detection.",
    version=VERSION
)

@app.get("/health", tags=["Monitoring"])
async def health_check(db: Session = Depends(get_db)) -> dict[str, Any]:
    """
    Check the operational status of the API and connection to the database.
    
    Returns:
    A dictionary containing the status, current timestamp, version, and
    subsystem health indicators.
    """

    # Check database connection (Boolean value)
    db_alive = check_db_connection(db)

    # Return result
    return {
        "status": "operational" if db_alive else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": VERSION,
        "services": {
            "database": "operational" if db_alive else "down",
            "ml_engine": "initialized" # Placeholder for your ML logic
        }
    }

@app.post("/v1/logs", tags=["Ingestion"], status_code=201, response_model=LogResponse)
async def ingest_log(
    # Receives log with LogCreate model and send it in the body
    log: Annotated[LogCreate, Body(description="The log data to be ingested")], 

    # Initialize a session with get_db function
    db: Session = Depends(get_db)
):
    """
    Receives logs from external services, validates them, 
    and persists them to the database
    """
    
    # Persist the validated log and return the database record
    return crud_save_log(db=db, log_data=log)

@app.get("/v1/logs", tags=["Retrieval"], response_model=list[LogResponse])
async def read_logs(
    # Create connection to database
    db: Session = Depends(get_db),

    # Get filters by service, level and limit the data
    service_name: Annotated[str | None, Query(max_length=50)] = None,
    log_level: Annotated[LogLevel | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 10
):
    """
    Retrieve a filtered list of logs from the database.

    This endpoint allows for searching logs based on the originating service 
    name and the severity level. It supports pagination through a limit 
    parameter to ensure optimal performance.

    Args:
        service_name (str, optional): The name of the service that generated the log.
        log_level (str, optional): The severity level of the log (e.g., INFO, ERROR).
        limit (int): The maximum number of log records to return (Default: 10, Max: 100).
        db (Session): Database session dependency.

    Returns:
        list[LogResponse]: A list of log records matching the criteria.
    """

    # Return the logs list with get logs function
    return crud_get_logs(db, service_name=service_name, log_level=log_level, limit=limit)

@app.get("/v1/logs/{log_id}", tags=["Retrieval"], response_model=LogResponse)
async def read_log(
    
    # Log id 
    # Must be an integer greater than or equal to 1.
    log_id: Annotated[int, Path(ge=1, description="The unique ID of the log record")],

    # Connect to the database
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific log record by its unique identifier.

    This endpoint fetches the full details of a single log entry from the database.
    If the provided ID does not match any existing record, a 404 Not Found 
    error is returned to the client.

    Args:
        log_id (int): The primary key of the log to be retrieved. 
                     Must be an integer greater than or equal to 1.
        db (Session): Database session dependency.

    Returns:
        LogResponse: The complete log object if found.

    Raises:
        HTTPException: 404 error if the log record does not exist in the database.
    """
    # Get log from the database
    db_log = crud_get_logs_by_id(db, log_id=log_id)

    # Check if log exists
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log record not found")
    
    # Return log
    return db_log
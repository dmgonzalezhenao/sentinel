"""
Main entry point for the Sentinel API.

This module initializes the FastAPI application and defines the core routes
for log ingestion and system health monitoring.
"""
# Import FastAPI object
from fastapi import FastAPI, Depends

# Import LogCreate object to get log data schema
from app.schemas.log_schema import LogCreate

# Import function to create a database session
from app.database.config import get_db

# Import CRUD logic to save logs in the database
from app.crud.log_crud import create_log as crud_save_log

# Import types for static analysis and type hinting
from datetime import datetime, timezone
from typing import Any
from sqlalchemy.orm import Session

# Initialize the FastAPI application with metadata
app = FastAPI(
    title="Project Sentinel",
    description="AI-Ready Infrastructure for Log Observability and Anomaly Detection.",
    version="0.1.0"
)

@app.get("/health", tags=["Monitoring"])
async def health_check() -> dict[str, Any]:
    """
    Check the operational status of the API and its core components.
    
    Returns:
    A dictionary containing the status, current timestamp, and 
    subsystem health indicators.
    """
    return {
        "status": "operational",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "0.1.0",
        "services": {
            "database": "pending",  # We will update this once we connect Postgres
            "ml_engine": "initialized" # Placeholder for your ML logic
        }
    }

@app.post("/v1/logs", tags=["Ingestion"], status_code=201, response_model=None)
async def ingest_log(log: LogCreate, db: Session = Depends(get_db)):
    """
    Receives logs from external services, validates them, 
    and persists them into the database.
    """
    
    # Persist the validated log and return the database record
    return crud_save_log(db=db, log_data=log)
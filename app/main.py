"""
Main entry point for the Sentinel API.

This module initializes the FastAPI application and defines the core routes
for log ingestion and system health monitoring.
"""
# Import FastAPI object
from fastapi import FastAPI

# Import datetime to log timestamp for health route and Any for Type Hinting
from datetime import datetime, timezone
from typing import Any

# Import LogCreate object to get log's format
from app.schemas import LogCreate

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

@app.post("/v1/logs", tags=["Ingestion"])
async def create_log(log: LogCreate) -> dict[str, Any]:
    """
    Endpoint to receive logs from external services.
    FastAPI will automatically validate the data using the LogCreate schema.
    """
    # For now, returns a success message
    return {
        "status": "success",
        "received_log": log
    }
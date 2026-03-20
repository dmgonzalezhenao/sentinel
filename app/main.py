"""
Main entry point for the Sentinel API.

This module initializes the FastAPI application and defines the core routes
for log ingestion and system health monitoring.
"""
# Import FastAPI object
from fastapi import FastAPI, Depends

# Import settings object 
from app.core.config import settings

# Import endpoints routers
from app.api.v1.endpoints import logs, users, organizations, auth

# Import function to create a database session
from app.database.config import get_db

# Import utils logic from database to check connection
from app.database.utils import check_db_connection

# Import types for static analysis and type hinting
from datetime import datetime, timezone
from typing import Any
from sqlalchemy.orm import Session

# Import sentinel logger
from app.core.logger import logger

# Initialize the FastAPI application with metadata
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Ready Infrastructure for Log Observability and Anomaly Detection.",
    version=settings.VERSION
)

# Include endpoints from routers
app.include_router(logs.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(organizations.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")

# --- Lifecycle logs ---
@app.on_event("startup")
async def startup_event() -> None:
    """
    Logs the startup event in Sentinel's logger.

    Returns:
    None
    """
    # Log startup as info
    logger.info(f"*** Starting {settings.PROJECT_NAME} v{settings.VERSION} ***")

@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Logs the shutdown event in Sentinel's logger.

    Returns:
    None
    """
    # Log shutdown as info
    logger.info(f"*** Shutting down {settings.PROJECT_NAME} ***")


@app.get("/health", tags=["Monitoring"])
async def health_check(db: Session = Depends(get_db)) -> dict[str, Any]:
    """
    Check the operational status of the API and connection to the database.
    
    Returns:
    A dictionary containing the status, current timestamp, version, and
    subsystem health indicators.
    """
    # Log /health call
    logger.info("Health check requested")

    # Check database connection (Boolean value)
    db_alive = check_db_connection(db)

    # Return result
    return {
        "status": "operational" if db_alive else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.VERSION,
        "services": {
            "database": "operational" if db_alive else "down",
            "ml_engine": "initialized" # Placeholder for your ML logic
        }
    }


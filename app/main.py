"""
Main entry point for the Sentinel API.

This module initializes the FastAPI application and defines the core routes
for log ingestion and system health monitoring.
"""
# Import FastAPI objects
from fastapi import FastAPI, Depends, Request, Response

# Import settings object 
from app.core.config import settings

# Import endpoints routers
from app.api.v1.endpoints import logs, users, organizations, auth

# Import function to create a database session
from app.database.config import get_db

# Import utils logic from database to check connection
from app.database.utils import check_db_connection

# Import time object to calculate response time (middleware)
import time

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

@app.middleware("http")
async def add_process_time_header(request: Request, call_next) -> Response:
    """
    Middleware for request latency measurement and observability.

    Calculates the elapsed time from when the request enters the system 
    until a response is generated, injecting the result into the 
    HTTP headers for performance monitoring (RNF-11).

    Args:
        request (Request): The incoming request object.
        call_next (Callable): The function that processes the request to the next 
                            node in the application (endpoint or middleware).

    Returns:
        Response: The processed response including the 'X-Process-Time' header.
    """
    # Start counting time
    start_time = time.time()
    
    # Process petition and await
    response = await call_next(request)
    
    # Calculate latency after awaiting
    process_time = time.time() - start_time
    
    # Inject in headers
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    
    # Log time in Sentinel's logger
    logger.info(f"Path: {request.url.path} | Latency: {process_time:.4f}s")
    
    # Return response to user
    return response

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
def health_check(db: Session = Depends(get_db)) -> dict[str, Any]:
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


"""
Main entry point for the Sentinel API.

This module initializes the FastAPI application and defines the core routes
for log ingestion and system health monitoring.
"""
from fastapi import FastAPI
from datetime import datetime

# Initialize the FastAPI application with metadata
app = FastAPI(
    title="Project Sentinel",
    description="AI-Ready Infrastructure for Log Observability and Anomaly Detection.",
    version="0.1.0"
)

@app.get("/health", tags=["Monitoring"])
async def health_check():
    """
    Check the operational status of the API and its core components.
    
    Returns:
        dict: A dictionary containing the status, current timestamp, and 
              sub-system health indicators.
    """
    return {
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0",
        "services": {
            "database": "pending",  # We will update this once we connect Postgres
            "ml_engine": "initialized" # Placeholder for your ML logic
        }
    }

"""
Sentinel API data schemas.

This module defines schemas for data validation and serialization.
"""
# Import basemodel for data schema
# Import field for validation
from pydantic import BaseModel, Field

# Import enum and datetime to put them  into the new class
from enum import Enum
from datetime import datetime, timezone
from typing import Any

# Enum for log level
class LogLevel(str, Enum):
    """
    Enumeration of allowed log severity levels.
    Inheriting from 'str' ensures the API handles text values correctly.
    """
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogCreate(BaseModel):
    """
    Schema for validating incoming log data.
    
    This model defines the required structure and data types for 
    new log entries sent by external services for ingestion.
    """
    service_name : str = Field(
        # Service name is required
        default=...,

        # Service name length
        min_length=3,
        max_length=50,

        # Description and examples for documentation
        description="The name of the service that generated this log.",
        examples=["auth-service"]
    )

    log_level: LogLevel = Field(
        # Log level is required
        default=..., 

        # Description and examples for documentation
        description="""The severity level of the log. Values must be:
                        'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        """,
        examples=["INFO", "ERROR"]
    )

    message: str = Field(
        # Message is required
        default=..., 

        # Length limits
        min_length=1, 
        max_length=1000,

        # Description and examples for documentation
        description="The main descriptive text of the log event.",
        examples=["User login failed", "Database connection timeout"]
    )

    timestamp : datetime = Field(
        # If there's no timestamp provided, calculate it from timezone
        default_factory=lambda: datetime.now(timezone.utc),

        # Description and examples for documentation
        description="The UTC timestamp of the log event in ISO 8601 format",
        examples=["2026-02-27T15:30:00Z"]
    )
    
    log_metadata : dict[str, Any] = Field(
        # If there's no metadata, put it as empty
        default={},

        # Description and examples for documentation
        description="""A flexible dictionary to store additional contextual information 
        about the log event, such as user IDs, request paths, or environment details.""",
        examples=[{"user_id": 12345, "ip_address": "192.168.1.1", "version": "v1.0.2"}]
    )

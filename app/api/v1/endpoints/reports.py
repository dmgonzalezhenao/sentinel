
"""
Sentinel API Report Endpoints.

This module handles the generation and export of system data into various 
formats (CSV, etc.) for administrative analysis, auditing, and 
Machine Learning dataset preparation.
"""
# Import csv and io to export logs to system
import csv
import io

# Import router to get access to endpoint, depends to await db
# and HTTPEcception to handle them
from fastapi import APIRouter, Query, Depends, HTTPException

# Import StreamingResponse to create CSV asynchronous
from fastapi.responses import StreamingResponse

# Import dependency to check user's role
from app.api.devs import RoleChecker, get_current_user

# Import get_db function to connect
from app.database.config import get_db

# Import User model for hinting
from app.database.models import User

# Import CRUD to request a bulk data
from app.crud.log_crud import get_multiple_logs

# Import Session object for hinting
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Annotated

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/export-csv")
def export_logs_to_csv(
    db: Session = Depends(get_db),
    current_user : User = Depends(RoleChecker(["ADMIN"])),
    limit: Annotated[int, Query()] = 10000,
):
    """
    Export a bulk of logs to a downloadable CSV file for administrative use.

    This endpoint retrieves log records globally across all organizations,
    formats them into a CSV structure, and streams the response to the client
    to minimize memory overhead. Restricted to Admin users only.

    Args:
        db (Session): Database session dependency.
        current_user (User): The authenticated admin user requesting the export.
        limit (int): Maximum number of log records to include in the report. Defaults to 10050.

    Returns:
        StreamingResponse: A file download response containing the log data in CSV format.

    Raises:
        HTTPException: 404 error if no logs are available for the requested criteria.
    """
    # Get logs from database
    logs = get_multiple_logs(db, current_user=current_user, limit=limit)
    
    # Raise error if there's no logs
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found to export")

    # Create generator to no saturate
    def generate():
        # Define CSV writer with streaming output
        output = io.StringIO()
        writer = csv.writer(output)

        # Add UTF-8
        yield "\ufeff"

        # Define headers for ML
        writer.writerow(["ID", "Service name", "Log Level", "Message", "Risk Score", "Is Anomaly", "Timestamp", "Process Time"])
        
        # Await to access value
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        # Write data in new CSV
        for log in logs:
            # Get metadata
            meta = log.log_metadata or {}
            
            # Get message as str
            raw_message = getattr(log, "message", None)     

            # Validate it
            if raw_message is not None:
                # Get clean message
                safe_message = str(raw_message).replace("\n", " ").replace("\r", "")[:100]            
            else:
                safe_message = "No message"

            # Format timestamp
            ts_str = log.timestamp.strftime("%Y-%m-%d %H:%M:%S") if log.timestamp is not None else "N/A"
            
            # Write by column
            writer.writerow([
                log.id,
                log.service_name or "unknown",
                log.log_level or "INFO",
                safe_message,
                meta.get("risk_score", 0),
                1 if meta.get("is_anomaly") else 0,
                ts_str,
                log.process_time
            ])
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    # Configure filename
    filename = f"sentinel_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

    # Return generate with csv type
    return StreamingResponse(
        generate(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
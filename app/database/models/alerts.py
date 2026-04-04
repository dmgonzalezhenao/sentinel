# Import column object and column types from SQLAlchemy
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey

# Import relationship to optimize joins
from sqlalchemy.orm import relationship

# Import JSONB attribute to save metadata (Only in PostgreSQL)
from sqlalchemy.dialects.postgresql import JSONB

# Function to get time automatically
from sqlalchemy.sql import func

# Import Base object to create Log table
from app.database.config import Base

class Alert(Base):
    """
    Represents the actionable incident layer in the Sentinel AIOps ecosystem.

    This table translates theoretical AI analysis into operational reality. It functions 
    as the primary queue for administrators to triage, investigate, and resolve 
    system anomalies identified by the ML models.

    Attributes:
        id (int): Primary key, auto-incrementing unique identifier for the alert.
        analysis_id (int): Foreign Key referencing the specific AIAnalysis record that triggered the alert.
        severity (str): Impact level mapped from the prediction_score (e.g., LOW, MEDIUM, HIGH, CRITICAL).
        status (str): Current lifecycle state of the incident (e.g., PENDING, INVESTIGATING, RESOLVED, FALSE_POSITIVE).
        assigned_to (int, optional): Reference to the administrator or user responsible for the resolution.
        notes (str, optional): Qualitative technical context or resolution steps provided by the operator.
        resolved_at (datetime, optional): UTC record of when the alert status was changed to RESOLVED.
        created_at (datetime): UTC timestamp of when the alert was initially triggered.
    """

    # Define table's name
    __tablename__ = "alerts"

    # Define alert attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    severity = Column(String(20), index=True, nullable=False)
    status = Column(String(20), index=True, nullable=False, default="PENDING")
    notes = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Foreign keys to analyses and admin user
    analysis_id = Column(Integer, ForeignKey("ai_analyses.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Optimize relationships
    ai_analysis = relationship("AIAnalysis", back_populates="alert")
    analyst = relationship("User", back_populates="alerts")
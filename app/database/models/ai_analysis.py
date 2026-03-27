# Import column object and column types from SQLAlchemy
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey, CheckConstraint

# Import relationship to optimize joins
from sqlalchemy.orm import relationship

# Import JSONB attribute to save metadata (Only in PostgreSQL)
from sqlalchemy.dialects.postgresql import JSONB

# Function to get time automatically
from sqlalchemy.sql import func

# Import Base object to create Log table
from app.database.config import Base

class AIAnalysis(Base):
    """
    Represents the intelligent interpretation layer of the Sentinel AIOps ecosystem.

    This table isolates the machine learning inference results from the raw log data, 
    enabling a clear separation between telemetry and analytical intelligence. 
    It supports model versioning and performance tracking for auditability.

    Attributes:
        id (int): Primary key, auto-incrementing unique identifier for the analysis record.
        log_id (int): Foreign Key referencing the original log entry analyzed by the AI.
        model_version (str): Identifier of the specific ML model used (e.g., 'random-forest-v1.2').
        prediction_score (float): Numerical confidence value (0.0 to 1.0) indicating risk level.
        is_anomaly (bool): Final binary classification determined by the model's threshold.
        inference_time_ms (float): Latency measured in milliseconds to process the inference.
        analysis_details (dict): Contextual "reasoning" stored as PostgreSQL JSONB (e.g., top-contributing features).
        created_at (datetime): UTC timestamp of when the analysis was generated.
    """

    # Define table's name
    __tablename__ = "ai_analyses"

    # Define attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    log_id = Column(Integer, ForeignKey("logs.id"), index=True, nullable=False)
    model_version = Column(String(50), nullable=False)
    prediction_score = Column(
        Float, 
        CheckConstraint("prediction_score >= 0.0 AND prediction_score <= 1.0"),
        nullable=False)
    is_anomaly = Column(Boolean, nullable=False, default=False)
    inference_time_ms = Column(Float, nullable=False)
    analysis_details = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

    # Optimize relationship's to log's analysis
    log = relationship("Log", back_populates="ai_analyses")
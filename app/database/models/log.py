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

class Log(Base):
    """
    Represents the central log entity in the Sentinel AIOps ecosystem.
    
    This table implements a multi-tenant architecture and aggregates data from three distinct sources:
    1. Client Data: Ingested via API (message, service_name, log_level).
    2. Observability Data: Calculated by the system Middleware (process_time).
    3. Artificial Intelligence: Generated asynchronously via background tasks (ai_category, risk_score, is_anomaly).
    
    Attributes:
        id (int): Primary key, auto-incrementing unique identifier.
        service_name (str): Name of the microservice or application originating the log.
        log_level (str): Event severity level (e.g., DEBUG, INFO, WARN, ERROR, CRITICAL).
        message (str): The raw descriptive content of the log entry.
        log_metadata (dict): Flexible context stored as PostgreSQL JSONB for schema-less data.
        timestamp (datetime): Server-side UTC record of when the log was received.
        user_id (int): Reference to the authenticated user who initiated the request.
        organization_id (int): Reference for data isolation in multi-tenant environments.
        process_time (float): Processing latency measured in seconds.
    """

    # Define table's name
    __tablename__ = 'logs'

    # Define log attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(50), index=True)
    log_level = Column(String(20), index=True, nullable=False)
    message = Column(String(1000), nullable=False)
    log_metadata = Column(JSONB, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Create foreign keys that reference user and organization
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), index=True, nullable=True)

    # Optimize relationships to organization, author and ai analyses
    organization = relationship("Organization", back_populates="logs")
    author = relationship("User", back_populates="logs")
    ai_analyses = relationship("AIAnalysis", back_populates="log", uselist=True)

    # Sentinel's latency time (middleware)
    process_time = Column(Float, nullable=True)

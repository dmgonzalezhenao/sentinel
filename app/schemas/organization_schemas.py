"""
Sentinel API organization schemas.

This module defines the Pydantic models for data validations (input)
and serialization (output) for registered organizations.
"""
# Import basemodel for logbase schema
# Import field for validation
# Import configdict to handle user objects from
# databases and get them as a dictionary
from pydantic import BaseModel, Field, ConfigDict

# Import datetime to put it in the new class
from datetime import datetime

class OrganizationBase(BaseModel):
    """
    Base schema for organization data.

    This model defines the core attributes shared by both organization
    creation and organization retrieval models, ensuring consistency
    accross the API.
    """
    name: str = Field(
        # Organization's name is required
        default=...,

        # Organization name length
        min_length=3,
        max_length=100,

        # Description and examples for documentation
        description="The name of the registered organization.",
        examples=["Microsoft", "Globant"]
    )

    slug: str = Field(
        # Organization slug is required

        # Organization slug length
        min_length=3,
        max_length=50,

        # Define slug pattern
        pattern=r"^[a-z0-9-]+$",

        # Description and examples for documentation
        description="The slug name of the registered organization.",
        examples=["Micro", "Go"]
    )

class OrganizationCreate(OrganizationBase):
    """Schema for creating a new organization."""
    pass

class OrganizationResponse(OrganizationBase):
    """
    Schema for returning organization's data from the database.
    """
    # Unique organization's id
    id: int = Field(
        # Description and examples for documentation
        description="Unique database ID.", 
        examples=[1, 105, 2304]
    )

    # Field to check organization is active
    is_active: bool = Field(
        # Description and examples for documentation
        description="Status of the organization.",
        examples=[True, False]
    )

    # Datetimes for auditing
    created_at: datetime = Field(
        # Description and examples for documentation
        description="The datetime when organization was created.",
        examples=["2024-03-20T10:00:00Z"]
    )

    updated_at: datetime = Field(
        # Description and examples for documentation
        description="The datetime of organization's last update.",
        examples=["2024-03-20T10:00:00Z"]
    )
    
    # Configures Pydantic to work with SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)

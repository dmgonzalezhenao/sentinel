"""
Sentinel API CRUD operations for organizations.

This module implements the logic for interacting with the database,
including users register and log in.
"""
# Import or_ to make comparations with SQL
from sqlalchemy import or_

# Import session object to access the database
from sqlalchemy.orm import Session

# Import organization class (organizations table from database)
from app.database.models import Organization

# Import Pydantic schemas to create and get organizations
from app.schemas.organization_schemas import OrganizationCreate, OrganizationResponse

# Import Sentinel's logger
from app.core.logger import logger

def create_organization(db: Session, organization: OrganizationCreate) -> Organization:
    """
    Function that creates a new register in organizations table.
    """
    # Instance organization
    db_org = Organization(
        name=organization.name,
        slug=organization.slug
    )

    try:
        # Log attempt to create organization
        logger.info(f"CRUD: Attempting to create organization '{organization.name}' with slug '{organization.slug}'")

        # Add changes and commit
        db.add(db_org)
        db.commit()

        # Refresh instance attributes
        db.refresh(db_org)

        # Log successful organization creation
        logger.info(f"CRUD: Successfuly created organization with name: {organization.name}")

        # Return object with new data
        return db_org
    
    # Exception if there's a connection error
    except Exception as e:
        # Log error in Sentinel's logger
        logger.error(f"CRUD: Failed to create organization: {str(e)}")

        # Avoid every change to the database to
        # avoid errors or corrupt data insertions
        db.rollback()

        # Raise error to main
        raise e

def get_organization(db: Session, name: str | None = None, slug: str | None = None) -> Organization | None:
    """
    Function that searches a organization by its name or its slug.
    It accepts both optional data.
    """
    # Prepare query
    query = db.query(Organization)

    # Check if both data is provided
    if slug is not None and name is not None:
        # Special case to check if anyone exists
        query = query.filter(or_(Organization.slug.is_(slug), Organization.name.is_(slug)))

    # Filter by slug
    elif slug is not None:
        query = query.filter(Organization.slug.is_(slug))

    # Filter by name
    elif name is not None:
        query = query.filter(Organization.name.is_(name))

    # Return None if there's no provided data
    else:
        return None

    # Return query
    return query.first()

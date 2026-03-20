"""
Sentinel API Organizations Endpoint

This module provides organization endpoint logic to main.py,
ensuring connection to database, and implementing
CRUD operations for organizations.
"""
# Import APIRouter to determine paths as Sentinel endpoints
# The other objects are for hinting
from fastapi import APIRouter, Depends, Body, HTTPException

# Import Pydantic organization schemas
from app.schemas.organization_schemas import OrganizationCreate, OrganizationResponse

# Import CRUD logic to handle organizations in database
from app.crud.organization_crud import (
    create_organization as crud_create_organization,
    get_organization as crud_get_organization
)

# Import function to create a database session
from app.database.config import get_db

# Import dependencies to handle RBAC
from app.api.devs import get_current_user, RoleChecker

# Import database models for type hinting
from app.database.models import Organization, Log, User

# Import logger object for sentinel's logging
from app.core.logger import logger

# Import types for static analysis and type hinting
from typing import Annotated, cast
from sqlalchemy.orm import Session

# Create router with path organizations
router = APIRouter(prefix="/organizations", tags=["Organizations"])

# Define ONLY admin users can register new organizations
allow_admin = RoleChecker(["ADMIN"])

@router.post("/", status_code=201, response_model=OrganizationResponse, dependencies=[Depends(allow_admin)])
def register_organization(
    organization_data: Annotated[OrganizationCreate, Body(description="The organization data for register")],
    db: Session = Depends(get_db)) -> Organization:
    """
    Register a new organization in the Sentinel system.

    This endpoint validates the input data, checks for existing name
    and slug records to prevent duplicates, and persists the new organization.

    Args:
        organization_data (OrganizationCreate): Schema containing name and slug.
        db (Session): Database session provided by dependency injection.

    Returns:
        Organization: The newly created organization object from the database.

    Raises:
        HTTPException: 400 error if the name or slug are already created.
    """
    # Log organization creation
    logger.info(f"Admin is creating new organization: {organization_data.name}")

    # Check if organization exists
    existing_organization = crud_get_organization(db=db, name=organization_data.name, slug=organization_data.slug)

    # Raise error if organization exists
    if existing_organization:
        raise HTTPException(status_code=409, detail="Organization already exists")

    # Validates the input and persists the organization record
    return crud_create_organization(db=db, organization=organization_data)

@router.get("/{slug}", response_model=OrganizationResponse)
def get_organization(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["ADMIN", "VIEWER"]))
) -> Organization:
    """
    Retrieve organization details by slug. 
    Admins can see any org; regular users can only see their own.

    Args:
        slug (str): Organization's slug.
        db (Session): Database session provided by dependency injection.
        current_user (User): Authenticated user with VIEWER or ADMIN role.

    Returns:
        OrganizationResponse: The complete organization object if found.

    Raises:
        HTTPException: 404 if the organization does not exist in the database.
        HTTPException: 403 if user is not authorized.
    """
    # Log attempt to get organization
    logger.info(f"Organization retrieval requested for slug: {slug}, by user: {current_user.email}")

    # Search organization
    org = crud_get_organization(db=db, slug=slug)

    # Raise error if doesn't exist
    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Hint user role and organization id
    user_role = str(cast(str, current_user.role))
    user_org_id = cast(int | None, current_user.organization_id)

    # Check role and if slug matches with organization
    if user_role != "ADMIN" and user_org_id != org.id:
        logger.warning(f"Unauthorized access attempt by {current_user.email} to org: {slug}")
        raise HTTPException(status_code=403, detail="Not enough permissions to view this organization")

    return org
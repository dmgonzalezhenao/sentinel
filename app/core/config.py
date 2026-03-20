"""
Sentinel API core's configuration

This module gets core data from environmental variables
to export them to the other modules by pydantic-settings.
"""

# Import base settings object to search data in the project files
# Import settings dict configuration to handle base settings
from pydantic_settings import BaseSettings, SettingsConfigDict

# Import pydantic to ensure Settings will find database url
from pydantic import Field

# Import os and PathLib to recognize environmental variables
import os
from pathlib import Path

# Root path
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    """
    Application settings and configuration manager for Sentinel API.

    This class centralizes all environment-specific variables, including 
    database connectivity, security parameters for JWT authentication, 
    and project metadata. It leverages Pydantic for automatic validation 
    and .env file parsing.

    Attributes:
        DATABASE_URL: The connection string for the PostgreSQL (Neon) database.
        VERSION: Current release version of the API.
        PROJECT_NAME: Formal name of the application.
        SECRET_KEY: Cryptographic key used for signing JWT tokens.
        ALGORITHM: Encryption algorithm used for session management.
        ACCESS_TOKEN_EXPIRE_MINUTES: Duration of token validity.
    """

    # Define global variables
    # BaseSettings will automatically search those values in
    # the project files
    DATABASE_URL: str = Field(validation_alias="DATABASE_URL")
    VERSION: str = "0.5.2"
    PROJECT_NAME: str = "Sentinel API"
    SECRET_KEY: str = Field(validation_alias="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, gt=0)

    # Configuration to specifically search in .env file for the variable names
    model_config = SettingsConfigDict(
        # Search .env file in root directory
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore" 
    )

# Create object (Could generate Pylance error)
settings = Settings() # type: ignore
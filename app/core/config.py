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

# Import any type for type hinting
from typing import Any

class Settings(BaseSettings):
    """
    Settings object that saves core data of Sentinel API,
    it includes:
    - URL to connect to the database
    - Sentinel API's version
    - Project's name
    """

    # Define global variables
    # BaseSettings will automatically search those values in
    # the project files
    DATABASE_URL: str | None = Field(default=None, validation_alias="DATABASE_URL")
    VERSION: str = "0.1.0"
    PROJECT_NAME: str = "Sentinel API"

    # Configuration to specifically search in .env file for the variable names
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" 
    )

# Create object
settings = Settings()
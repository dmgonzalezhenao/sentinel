"""
Sentinel API Logging Configuration.

This module initializes and configures the centralized logging system for 
the Sentinel API. It provides a dual-handler setup to capture system events 
in both the standard output (console) and a persistent rotating file.
"""

# Import logging module
import logging

# Import sys module 
import sys

# Import rotating file handler to handle file size
from logging.handlers import RotatingFileHandler

# Import path to create sentinel.log file
from pathlib import Path

# Import settings to access to sentinel's core ingo
from app.core.config import settings

# Search logs path 
LOG_DIR = Path("logs")

# Create paht if not exists
LOG_DIR.mkdir(exist_ok=True)

# Create sentinel.log file 
LOG_FILE = LOG_DIR / "sentinel.log"

# Define log format
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] -> %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

# Create logger object with project's name
logger = logging.getLogger(settings.PROJECT_NAME)

# Set level to only log info logs or superior
logger.setLevel(logging.INFO)

# Avoid duplicate logs in console
logger.propagate = False

# Handler for VSCode terminal
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

# --- Rotating File Handler: Manages long-term log persistence ---
file_handler = RotatingFileHandler(
    # Define log file (sentinel.log)
    LOG_FILE, 
    
    # File maximum size (5MB)
    maxBytes=5*1024*1024, 

    # Just allow 3 files max
    # When you create fourth one, the oldest is eliminated
    backupCount=3,       

    # Encoding for windows  
    encoding="utf-8"
)

# Set format
file_handler.setFormatter(formatter)

# Connect console and file handler to logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
"""
Structured logging configuration for Resumaker backend.

Provides centralized logging setup with file rotation and proper formatting.
"""
import logging
import sys
from datetime import datetime
import os
from pathlib import Path


def setup_logging() -> logging.Logger:
    """
    Configure structured logging for the application.

    Returns:
        Logger instance configured with both console and file handlers
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                logs_dir / f'app_{datetime.now().strftime("%Y%m%d")}.log'
            )
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized at {log_level} level")

    return logger

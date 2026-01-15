"""
Custom logger configuration for the QA automation framework.
Provides consistent logging across all test modules.
"""

import logging
import sys
from datetime import datetime
from config.settings import LOGS_DIR


def setup_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Create and configure a logger instance.

    Args:
        name: Name of the logger (usually __name__ of the calling module)
        level: Logging level (default: DEBUG)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_format)

    # File handler with timestamp
    log_filename = f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(
        LOGS_DIR / log_filename,
        mode="a",
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Create a default logger instance
default_logger = setup_logger("qa_framework")

"""
Configuration settings for the QA automation framework.
Loads environment variables and provides centralized configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Ensure directories exist
for directory in [LOGS_DIR, REPORTS_DIR, REPORTS_DIR / "artifacts"]:
    directory.mkdir(parents=True, exist_ok=True)


class Settings:
    """Application settings loaded from environment variables."""

    # URLs
    BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com")

    # Test credentials
    STANDARD_USER: str = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_OUT_USER: str = os.getenv("LOCKED_OUT_USER", "locked_out_user")
    PROBLEM_USER: str = os.getenv("PROBLEM_USER", "problem_user")
    PERFORMANCE_USER: str = os.getenv("PERFORMANCE_USER", "performance_glitch_user")
    ERROR_USER: str = os.getenv("ERROR_USER", "error_user")
    VISUAL_USER: str = os.getenv("VISUAL_USER", "visual_user")
    PASSWORD: str = os.getenv("PASSWORD", "secret_sauce")

    # Browser settings
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    SLOW_MO: int = int(os.getenv("SLOW_MO", "100"))
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30000"))

    # Reporting
    SCREENSHOT_ON_FAILURE: bool = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    VIDEO_ON_FAILURE: bool = os.getenv("VIDEO_ON_FAILURE", "true").lower() == "true"


settings = Settings()

"""
Data loader utility for loading test data from CSV and JSON files.
Supports parameterized testing with various data formats.
"""

import csv
import json
from typing import Any
from config.settings import DATA_DIR
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DataLoader:
    """Utility class for loading test data from various file formats."""

    @staticmethod
    def load_json(filename: str) -> dict[str, Any]:
        """
        Load data from a JSON file.

        Args:
            filename: Name of the JSON file (with or without .json extension)

        Returns:
            Dictionary containing the JSON data

        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file is not valid JSON
        """
        if not filename.endswith(".json"):
            filename = f"{filename}.json"

        filepath = DATA_DIR / filename
        logger.debug(f"Loading JSON data from: {filepath}")

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"Successfully loaded JSON data from {filename}")
            return data

    @staticmethod
    def load_csv(filename: str) -> list[dict[str, str]]:
        """
        Load data from a CSV file.

        Args:
            filename: Name of the CSV file (with or without .csv extension)

        Returns:
            List of dictionaries, where each dictionary represents a row

        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        if not filename.endswith(".csv"):
            filename = f"{filename}.csv"

        filepath = DATA_DIR / filename
        logger.debug(f"Loading CSV data from: {filepath}")

        with open(filepath, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = list(reader)
            logger.info(f"Successfully loaded {len(data)} rows from {filename}")
            return data

    @staticmethod
    def get_valid_users() -> list[dict[str, str]]:
        """Get valid user credentials for login tests."""
        data = DataLoader.load_json("users")
        return data.get("valid_users", [])

    @staticmethod
    def get_invalid_users() -> list[dict[str, str]]:
        """Get invalid user credentials for negative login tests."""
        data = DataLoader.load_json("users")
        return data.get("invalid_users", [])

    @staticmethod
    def get_valid_checkout_data() -> list[dict[str, str]]:
        """Get valid checkout form data."""
        data = DataLoader.load_json("checkout")
        return data.get("valid_checkout_data", [])

    @staticmethod
    def get_invalid_checkout_data() -> list[dict[str, str]]:
        """Get invalid checkout form data for negative tests."""
        data = DataLoader.load_json("checkout")
        return data.get("invalid_checkout_data", [])

    @staticmethod
    def get_products() -> list[dict[str, Any]]:
        """Get product data for inventory tests."""
        data = DataLoader.load_json("products")
        return data.get("products", [])

    @staticmethod
    def get_sort_options() -> list[dict[str, str]]:
        """Get sort options for inventory tests."""
        data = DataLoader.load_json("products")
        return data.get("sort_options", [])


# Create a singleton instance for convenience
data_loader = DataLoader()

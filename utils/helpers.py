"""
Helper utilities for common testing operations.
Provides reusable functions for assertions, waits, and data manipulation.
"""

import re
from playwright.sync_api import Page, expect
from utils.logger import setup_logger

logger = setup_logger(__name__)


def extract_price(price_string: str) -> float:
    """
    Extract numeric price from a string.

    Args:
        price_string: String containing price (e.g., "$29.99")

    Returns:
        Float value of the price
    """
    match = re.search(r"[\d.]+", price_string)
    if match:
        return float(match.group())
    raise ValueError(f"Could not extract price from: {price_string}")


def format_price(price: float) -> str:
    """
    Format a price value as a currency string.

    Args:
        price: Float price value

    Returns:
        Formatted price string (e.g., "$29.99")
    """
    return f"${price:.2f}"


def wait_for_page_load(page: Page, timeout: int = 30000) -> None:
    """
    Wait for page to be fully loaded.

    Args:
        page: Playwright Page instance
        timeout: Maximum wait time in milliseconds
    """
    logger.debug("Waiting for page to fully load...")
    page.wait_for_load_state("networkidle", timeout=timeout)
    logger.debug("Page fully loaded")


def take_screenshot(page: Page, name: str) -> str:
    """
    Take a screenshot of the current page.

    Args:
        page: Playwright Page instance
        name: Name for the screenshot file

    Returns:
        Path to the saved screenshot
    """
    from config.settings import REPORTS_DIR

    screenshot_path = REPORTS_DIR / "artifacts" / f"{name}.png"
    page.screenshot(path=str(screenshot_path))
    logger.info(f"Screenshot saved: {screenshot_path}")
    return str(screenshot_path)


def assert_element_visible(page: Page, selector: str) -> None:
    """
    Assert that an element is visible on the page.

    Args:
        page: Playwright Page instance
        selector: CSS selector for the element
    """
    element = page.locator(selector)
    expect(element).to_be_visible()
    logger.debug(f"Element visible: {selector}")


def assert_text_present(page: Page, text: str) -> None:
    """
    Assert that text is present on the page.

    Args:
        page: Playwright Page instance
        text: Text to search for
    """
    expect(page.get_by_text(text)).to_be_visible()
    logger.debug(f"Text found on page: {text}")


def assert_url_contains(page: Page, url_part: str) -> None:
    """
    Assert that the current URL contains a specific string.

    Args:
        page: Playwright Page instance
        url_part: String that should be in the URL
    """
    expect(page).to_have_url(re.compile(f".*{url_part}.*"))
    logger.debug(f"URL contains: {url_part}")


def get_element_count(page: Page, selector: str) -> int:
    """
    Get the count of elements matching a selector.

    Args:
        page: Playwright Page instance
        selector: CSS selector for the elements

    Returns:
        Number of matching elements
    """
    count = page.locator(selector).count()
    logger.debug(f"Found {count} elements matching: {selector}")
    return count


def scroll_to_element(page: Page, selector: str) -> None:
    """
    Scroll the page to make an element visible.

    Args:
        page: Playwright Page instance
        selector: CSS selector for the element
    """
    element = page.locator(selector)
    element.scroll_into_view_if_needed()
    logger.debug(f"Scrolled to element: {selector}")


def generate_test_id(prefix: str = "test") -> str:
    """
    Generate a unique test identifier.

    Args:
        prefix: Prefix for the ID

    Returns:
        Unique identifier string
    """
    import uuid
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

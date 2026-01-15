"""
Base Page Object class providing common functionality for all page objects.
Implements the Page Object Model (POM) pattern foundation.
"""

import re
from typing import Literal
from playwright.sync_api import Page, Locator, expect
from config.settings import settings
from utils.logger import setup_logger
from utils import helpers

logger = setup_logger(__name__)


class BasePage:
    """
    Base class for all page objects.

    Provides common methods for page interactions, navigation,
    and element handling that can be inherited by specific page objects.
    """

    def __init__(self, page: Page) -> None:
        """
        Initialize the base page.

        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.base_url = settings.BASE_URL
        self.timeout = settings.TIMEOUT

    # Navigation methods
    def navigate(self, path: str = "") -> None:
        """
        Navigate to a specific path relative to base URL.

        Args:
            path: Path to append to base URL
        """
        url = f"{self.base_url}/{path}" if path else self.base_url
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)
        self.wait_for_page_load()

    def navigate_to_url(self, url: str) -> None:
        """
        Navigate to an absolute URL.

        Args:
            url: Full URL to navigate to
        """
        logger.info(f"Navigating to URL: {url}")
        self.page.goto(url)
        self.wait_for_page_load()

    def reload(self) -> None:
        """Reload the current page."""
        logger.debug("Reloading page")
        self.page.reload()
        self.wait_for_page_load()

    def go_back(self) -> None:
        """Navigate back in browser history."""
        logger.debug("Going back in browser history")
        self.page.go_back()

    def go_forward(self) -> None:
        """Navigate forward in browser history."""
        logger.debug("Going forward in browser history")
        self.page.go_forward()

    # Wait methods
    def wait_for_page_load(self) -> None:
        """Wait for page to be fully loaded."""
        helpers.wait_for_page_load(self.page, self.timeout)

    def wait_for_element(
        self,
        selector: str,
        state: Literal["attached", "detached", "hidden", "visible"] = "visible"
    ) -> Locator:
        """
        Wait for an element to reach a specific state.

        Args:
            selector: CSS selector for the element
            state: State to wait for ('visible', 'hidden', 'attached', 'detached')

        Returns:
            Locator for the element
        """
        logger.debug(f"Waiting for element: {selector} to be {state}")
        locator = self.page.locator(selector)
        locator.wait_for(state=state, timeout=self.timeout)
        return locator

    def wait_for_url(self, url_pattern: str) -> None:
        """
        Wait for URL to match a pattern.

        Args:
            url_pattern: URL pattern to wait for (can be regex)
        """
        logger.debug(f"Waiting for URL pattern: {url_pattern}")
        self.page.wait_for_url(url_pattern, timeout=self.timeout)

    # Element interaction methods
    def click(self, selector: str) -> None:
        """
        Click on an element.

        Args:
            selector: CSS selector for the element
        """
        logger.debug(f"Clicking element: {selector}")
        self.page.locator(selector).click()

    def double_click(self, selector: str) -> None:
        """
        Double-click on an element.

        Args:
            selector: CSS selector for the element
        """
        logger.debug(f"Double-clicking element: {selector}")
        self.page.locator(selector).dblclick()

    def fill(self, selector: str, value: str) -> None:
        """
        Fill an input field with a value.

        Args:
            selector: CSS selector for the input
            value: Value to fill
        """
        logger.debug(f"Filling element {selector} with value")
        self.page.locator(selector).fill(value)

    def clear(self, selector: str) -> None:
        """
        Clear an input field.

        Args:
            selector: CSS selector for the input
        """
        logger.debug(f"Clearing element: {selector}")
        self.page.locator(selector).clear()

    def type_text(self, selector: str, text: str, delay: int = 50) -> None:
        """
        Type text into an element character by character.

        Args:
            selector: CSS selector for the element
            text: Text to type
            delay: Delay between keystrokes in milliseconds
        """
        logger.debug(f"Typing into element: {selector}")
        self.page.locator(selector).type(text, delay=delay)

    def select_option(self, selector: str, value: str) -> None:
        """
        Select an option from a dropdown.

        Args:
            selector: CSS selector for the select element
            value: Value of the option to select
        """
        logger.debug(f"Selecting option '{value}' in: {selector}")
        self.page.locator(selector).select_option(value)

    def check(self, selector: str) -> None:
        """
        Check a checkbox.

        Args:
            selector: CSS selector for the checkbox
        """
        logger.debug(f"Checking checkbox: {selector}")
        self.page.locator(selector).check()

    def uncheck(self, selector: str) -> None:
        """
        Uncheck a checkbox.

        Args:
            selector: CSS selector for the checkbox
        """
        logger.debug(f"Unchecking checkbox: {selector}")
        self.page.locator(selector).uncheck()

    def hover(self, selector: str) -> None:
        """
        Hover over an element.

        Args:
            selector: CSS selector for the element
        """
        logger.debug(f"Hovering over element: {selector}")
        self.page.locator(selector).hover()

    # Element state methods
    def get_text(self, selector: str) -> str:
        """
        Get text content of an element.

        Args:
            selector: CSS selector for the element

        Returns:
            Text content of the element
        """
        text = self.page.locator(selector).text_content() or ""
        logger.debug(f"Got text from {selector}: {text[:50]}...")
        return text

    def get_attribute(self, selector: str, attribute: str) -> str | None:
        """
        Get an attribute value from an element.

        Args:
            selector: CSS selector for the element
            attribute: Name of the attribute

        Returns:
            Attribute value or None
        """
        return self.page.locator(selector).get_attribute(attribute)

    def get_input_value(self, selector: str) -> str:
        """
        Get the value of an input field.

        Args:
            selector: CSS selector for the input

        Returns:
            Input value
        """
        return self.page.locator(selector).input_value()

    def is_visible(self, selector: str) -> bool:
        """
        Check if an element is visible.

        Args:
            selector: CSS selector for the element

        Returns:
            True if visible, False otherwise
        """
        return self.page.locator(selector).is_visible()

    def is_enabled(self, selector: str) -> bool:
        """
        Check if an element is enabled.

        Args:
            selector: CSS selector for the element

        Returns:
            True if enabled, False otherwise
        """
        return self.page.locator(selector).is_enabled()

    def is_checked(self, selector: str) -> bool:
        """
        Check if a checkbox/radio is checked.

        Args:
            selector: CSS selector for the element

        Returns:
            True if checked, False otherwise
        """
        return self.page.locator(selector).is_checked()

    def get_element_count(self, selector: str) -> int:
        """
        Get the count of elements matching a selector.

        Args:
            selector: CSS selector

        Returns:
            Number of matching elements
        """
        return helpers.get_element_count(self.page, selector)

    # Assertion methods
    def expect_visible(self, selector: str) -> None:
        """
        Assert that an element is visible.

        Args:
            selector: CSS selector for the element
        """
        expect(self.page.locator(selector)).to_be_visible()

    def expect_hidden(self, selector: str) -> None:
        """
        Assert that an element is hidden.

        Args:
            selector: CSS selector for the element
        """
        expect(self.page.locator(selector)).to_be_hidden()

    def expect_text(self, selector: str, text: str) -> None:
        """
        Assert that an element contains specific text.

        Args:
            selector: CSS selector for the element
            text: Expected text
        """
        expect(self.page.locator(selector)).to_contain_text(text)

    def expect_url(self, url_pattern: str) -> None:
        """
        Assert that the current URL matches a pattern.

        Args:
            url_pattern: Expected URL or pattern (regex supported with .* notation)
        """
        expect(self.page).to_have_url(re.compile(url_pattern))

    def expect_title(self, title: str) -> None:
        """
        Assert that the page title matches.

        Args:
            title: Expected title
        """
        expect(self.page).to_have_title(title)

    # Utility methods
    def get_locator(self, selector: str) -> Locator:
        """
        Get a Playwright Locator for an element.

        Args:
            selector: CSS selector

        Returns:
            Playwright Locator instance
        """
        return self.page.locator(selector)

    def scroll_to_element(self, selector: str) -> None:
        """
        Scroll to make an element visible.

        Args:
            selector: CSS selector for the element
        """
        helpers.scroll_to_element(self.page, selector)

    def take_screenshot(self, name: str) -> str:
        """
        Take a screenshot of the current page.

        Args:
            name: Name for the screenshot file

        Returns:
            Path to the saved screenshot
        """
        return helpers.take_screenshot(self.page, name)

    def get_current_url(self) -> str:
        """
        Get the current page URL.

        Returns:
            Current URL
        """
        return self.page.url

    def get_title(self) -> str:
        """
        Get the current page title.

        Returns:
            Page title
        """
        return self.page.title()

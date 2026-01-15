"""
Login Page Object for Sauce Demo application.
Handles all login-related interactions and verifications.
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LoginPageLocators:
    """Locators for the Login Page elements."""

    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    ERROR_BUTTON = ".error-button"
    LOGO = ".login_logo"


class LoginPage(BasePage):
    """
    Page Object for the Login page.

    Provides methods for:
    - Logging in with credentials
    - Verifying login errors
    - Checking login page state
    """

    def __init__(self, page: Page) -> None:
        """Initialize the Login Page."""
        super().__init__(page)
        self.locators = LoginPageLocators

    def open(self) -> "LoginPage":
        """
        Navigate to the login page.

        Returns:
            Self for method chaining
        """
        logger.info("Opening login page")
        self.navigate()
        return self

    def enter_username(self, username: str) -> "LoginPage":
        """
        Enter username in the login form.

        Args:
            username: Username to enter

        Returns:
            Self for method chaining
        """
        logger.debug(f"Entering username: {username}")
        self.fill(self.locators.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """
        Enter password in the login form.

        Args:
            password: Password to enter

        Returns:
            Self for method chaining
        """
        logger.debug("Entering password")
        self.fill(self.locators.PASSWORD_INPUT, password)
        return self

    def click_login_button(self) -> None:
        """Click the login button."""
        logger.info("Clicking login button")
        self.click(self.locators.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """
        Perform complete login action.

        Args:
            username: Username to use
            password: Password to use
        """
        logger.info(f"Logging in with user: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def login_as_standard_user(self) -> None:
        """Login with standard user credentials."""
        from config.settings import settings
        self.login(settings.STANDARD_USER, settings.PASSWORD)

    def login_as_locked_user(self) -> None:
        """Login with locked out user credentials."""
        from config.settings import settings
        self.login(settings.LOCKED_OUT_USER, settings.PASSWORD)

    def login_as_problem_user(self) -> None:
        """Login with problem user credentials."""
        from config.settings import settings
        self.login(settings.PROBLEM_USER, settings.PASSWORD)

    # Verification methods
    def is_login_page_displayed(self) -> bool:
        """
        Check if login page is displayed.

        Returns:
            True if login page is visible
        """
        return self.is_visible(self.locators.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """
        Get the error message text.

        Returns:
            Error message text
        """
        return self.get_text(self.locators.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """
        Check if an error message is displayed.

        Returns:
            True if error is visible
        """
        return self.is_visible(self.locators.ERROR_MESSAGE)

    def close_error_message(self) -> "LoginPage":
        """
        Close the error message by clicking the X button.

        Returns:
            Self for method chaining
        """
        if self.is_error_displayed():
            self.click(self.locators.ERROR_BUTTON)
        return self

    def clear_form(self) -> "LoginPage":
        """
        Clear the login form fields.

        Returns:
            Self for method chaining
        """
        self.clear(self.locators.USERNAME_INPUT)
        self.clear(self.locators.PASSWORD_INPUT)
        return self

    # Assertions
    def expect_login_successful(self) -> None:
        """Assert that login was successful by checking URL."""
        self.expect_url(".*inventory.*")
        logger.info("Login successful - redirected to inventory")

    def expect_login_failed(self, expected_error: str | None = None) -> None:
        """
        Assert that login failed.

        Args:
            expected_error: Optional expected error message
        """
        expect(self.page.locator(self.locators.ERROR_MESSAGE)).to_be_visible()
        if expected_error:
            expect(self.page.locator(self.locators.ERROR_MESSAGE)).to_contain_text(
                expected_error
            )
        logger.info("Login failed as expected")

    def expect_logo_visible(self) -> None:
        """Assert that the logo is visible."""
        self.expect_visible(self.locators.LOGO)

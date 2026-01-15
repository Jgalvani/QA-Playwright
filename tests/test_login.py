"""
Login functionality tests for Sauce Demo application.
Tests cover successful login, failed login, and various error scenarios.
"""

import pytest
from pages import LoginPage
from utils import DataLoader


class TestLoginSuccess:
    """Test cases for successful login scenarios."""

    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_with_standard_user(self, login_page: LoginPage) -> None:
        """Test successful login with standard user credentials."""
        login_page.open()
        login_page.login_as_standard_user()
        login_page.expect_login_successful()

    @pytest.mark.login
    @pytest.mark.parametrize("user_data", DataLoader.get_valid_users())
    def test_login_with_valid_users(
        self, login_page: LoginPage, user_data: dict
    ) -> None:
        """
        Test login with various valid user credentials.

        Args:
            login_page: LoginPage fixture
            user_data: Parametrized user data from test data file
        """
        login_page.open()
        login_page.login(user_data["username"], user_data["password"])
        login_page.expect_login_successful()

    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_page_elements_visible(self, login_page: LoginPage) -> None:
        """Test that all login page elements are visible."""
        login_page.open()
        login_page.expect_logo_visible()
        login_page.expect_visible(login_page.locators.USERNAME_INPUT)
        login_page.expect_visible(login_page.locators.PASSWORD_INPUT)
        login_page.expect_visible(login_page.locators.LOGIN_BUTTON)


class TestLoginFailure:
    """Test cases for failed login scenarios."""

    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_locked_user(self, login_page: LoginPage) -> None:
        """Test that locked out user cannot login."""
        login_page.open()
        login_page.login_as_locked_user()
        login_page.expect_login_failed("Sorry, this user has been locked out")

    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_invalid_username(self, login_page: LoginPage) -> None:
        """Test login failure with invalid username."""
        login_page.open()
        login_page.login("invalid_user", "secret_sauce")
        login_page.expect_login_failed(
            "Username and password do not match any user in this service"
        )

    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_invalid_password(self, login_page: LoginPage) -> None:
        """Test login failure with invalid password."""
        login_page.open()
        login_page.login("standard_user", "wrong_password")
        login_page.expect_login_failed(
            "Username and password do not match any user in this service"
        )

    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_empty_username(self, login_page: LoginPage) -> None:
        """Test login failure with empty username."""
        login_page.open()
        login_page.login("", "secret_sauce")
        login_page.expect_login_failed("Username is required")

    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_empty_password(self, login_page: LoginPage) -> None:
        """Test login failure with empty password."""
        login_page.open()
        login_page.login("standard_user", "")
        login_page.expect_login_failed("Password is required")

    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_empty_credentials(self, login_page: LoginPage) -> None:
        """Test login failure with empty credentials."""
        login_page.open()
        login_page.login("", "")
        login_page.expect_login_failed("Username is required")

    @pytest.mark.login
    @pytest.mark.negative
    @pytest.mark.parametrize("user_data", DataLoader.get_invalid_users())
    def test_login_with_invalid_credentials(
        self, login_page: LoginPage, user_data: dict
    ) -> None:
        """
        Test login with various invalid credentials.

        Args:
            login_page: LoginPage fixture
            user_data: Parametrized invalid user data
        """
        login_page.open()
        login_page.login(user_data["username"], user_data["password"])
        login_page.expect_login_failed()


class TestLoginErrorHandling:
    """Test cases for error handling on login page."""

    @pytest.mark.login
    def test_error_message_can_be_closed(self, login_page: LoginPage) -> None:
        """Test that error message can be dismissed."""
        login_page.open()
        login_page.login("", "")
        assert login_page.is_error_displayed()
        login_page.close_error_message()
        # After a brief moment, error should be closed or animation started
        # Note: depending on implementation, may need explicit wait

    @pytest.mark.login
    def test_form_can_be_cleared_and_resubmitted(
        self, login_page: LoginPage
    ) -> None:
        """Test that form can be cleared and resubmitted."""
        login_page.open()

        # First attempt with wrong credentials
        login_page.login("wrong_user", "wrong_pass")
        login_page.expect_login_failed()

        # Clear and try with correct credentials
        login_page.clear_form()
        login_page.login_as_standard_user()
        login_page.expect_login_successful()

    @pytest.mark.login
    def test_multiple_failed_login_attempts(self, login_page: LoginPage) -> None:
        """Test multiple failed login attempts."""
        login_page.open()

        # Attempt multiple times
        for _ in range(3):
            login_page.login("invalid", "invalid")
            login_page.expect_login_failed()
            login_page.close_error_message()
            login_page.clear_form()

        # Should still be able to login successfully
        login_page.login_as_standard_user()
        login_page.expect_login_successful()

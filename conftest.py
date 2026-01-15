"""
Pytest fixtures for the QA automation framework.
Provides reusable test fixtures for browser, pages, and test data.
"""

import pytest
from typing import Generator
from playwright.sync_api import Page

from pages import (
    LoginPage,
    InventoryPage,
    CartPage,
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage,
)
from config.settings import settings
from utils import setup_logger, DataLoader

logger = setup_logger(__name__)


# ==================== Browser Fixtures ====================


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """
    Configure browser context with custom viewport and locale.

    Args:
        browser_context_args: Default browser context arguments

    Returns:
        Updated browser context arguments
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "fr-FR",
        "timezone_id": "Europe/Paris",
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    """
    Configure browser launch options.

    Args:
        browser_type_launch_args: Default browser launch arguments

    Returns:
        Updated browser launch arguments
    """
    return {
        **browser_type_launch_args,
        "headless": settings.HEADLESS,
        "slow_mo": settings.SLOW_MO,
    }


# ==================== Page Object Fixtures ====================


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """
    Provide a LoginPage instance.

    Args:
        page: Playwright Page instance

    Returns:
        LoginPage instance
    """
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    """
    Provide an InventoryPage instance.

    Args:
        page: Playwright Page instance

    Returns:
        InventoryPage instance
    """
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    """
    Provide a CartPage instance.

    Args:
        page: Playwright Page instance

    Returns:
        CartPage instance
    """
    return CartPage(page)


@pytest.fixture
def checkout_step_one_page(page: Page) -> CheckoutStepOnePage:
    """
    Provide a CheckoutStepOnePage instance.

    Args:
        page: Playwright Page instance

    Returns:
        CheckoutStepOnePage instance
    """
    return CheckoutStepOnePage(page)


@pytest.fixture
def checkout_step_two_page(page: Page) -> CheckoutStepTwoPage:
    """
    Provide a CheckoutStepTwoPage instance.

    Args:
        page: Playwright Page instance

    Returns:
        CheckoutStepTwoPage instance
    """
    return CheckoutStepTwoPage(page)


@pytest.fixture
def checkout_complete_page(page: Page) -> CheckoutCompletePage:
    """
    Provide a CheckoutCompletePage instance.

    Args:
        page: Playwright Page instance

    Returns:
        CheckoutCompletePage instance
    """
    return CheckoutCompletePage(page)


# ==================== Authentication Fixtures ====================


@pytest.fixture
def logged_in_page(page: Page, login_page: LoginPage) -> Page:
    """
    Provide a page that is already logged in with standard user.

    Args:
        page: Playwright Page instance
        login_page: LoginPage fixture

    Returns:
        Page instance with logged in user
    """
    logger.info("Setting up logged in page")
    login_page.open()
    login_page.login_as_standard_user()
    login_page.expect_login_successful()
    return page


@pytest.fixture
def logged_in_inventory(
    logged_in_page: Page, inventory_page: InventoryPage
) -> InventoryPage:
    """
    Provide an InventoryPage that is already logged in.

    Args:
        logged_in_page: Page with logged in user
        inventory_page: InventoryPage fixture

    Returns:
        InventoryPage instance with logged in user
    """
    inventory_page.expect_on_inventory_page()
    return inventory_page


# ==================== Test Data Fixtures ====================


@pytest.fixture
def valid_users() -> list[dict]:
    """
    Provide valid user credentials.

    Returns:
        List of valid user data dictionaries
    """
    return DataLoader.get_valid_users()


@pytest.fixture
def invalid_users() -> list[dict]:
    """
    Provide invalid user credentials.

    Returns:
        List of invalid user data dictionaries
    """
    return DataLoader.get_invalid_users()


@pytest.fixture
def valid_checkout_data() -> list[dict]:
    """
    Provide valid checkout form data.

    Returns:
        List of valid checkout data dictionaries
    """
    return DataLoader.get_valid_checkout_data()


@pytest.fixture
def invalid_checkout_data() -> list[dict]:
    """
    Provide invalid checkout form data.

    Returns:
        List of invalid checkout data dictionaries
    """
    return DataLoader.get_invalid_checkout_data()


@pytest.fixture
def products_data() -> list[dict]:
    """
    Provide product data.

    Returns:
        List of product data dictionaries
    """
    return DataLoader.get_products()


# ==================== Cart Setup Fixtures ====================


@pytest.fixture
def cart_with_one_item(logged_in_inventory: InventoryPage) -> InventoryPage:
    """
    Provide inventory page with one item in cart.

    Args:
        logged_in_inventory: Logged in InventoryPage

    Returns:
        InventoryPage with one item in cart
    """
    logged_in_inventory.add_product_to_cart_by_name("Sauce Labs Backpack")
    logged_in_inventory.expect_cart_count(1)
    return logged_in_inventory


@pytest.fixture
def cart_with_multiple_items(logged_in_inventory: InventoryPage) -> InventoryPage:
    """
    Provide inventory page with multiple items in cart.

    Args:
        logged_in_inventory: Logged in InventoryPage

    Returns:
        InventoryPage with multiple items in cart
    """
    logged_in_inventory.add_product_to_cart_by_name("Sauce Labs Backpack")
    logged_in_inventory.add_product_to_cart_by_name("Sauce Labs Bike Light")
    logged_in_inventory.add_product_to_cart_by_name("Sauce Labs Bolt T-Shirt")
    logged_in_inventory.expect_cart_count(3)
    return logged_in_inventory


# ==================== Utility Fixtures ====================


@pytest.fixture(autouse=True)
def test_setup_teardown(request: pytest.FixtureRequest) -> Generator:
    """
    Setup and teardown for each test.
    Logs test start and end.

    Args:
        request: Pytest fixture request object

    Yields:
        None
    """
    test_name = request.node.name
    logger.info(f"{'=' * 50}")
    logger.info(f"Starting test: {test_name}")
    logger.info(f"{'=' * 50}")

    yield

    # Log test result
    if hasattr(request.node, "rep_call"):
        if request.node.rep_call.failed:
            logger.error(f"Test FAILED: {test_name}")
        else:
            logger.info(f"Test PASSED: {test_name}")
    else:
        logger.info(f"Test completed: {test_name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator:
    """
    Hook to capture test results for use in fixtures.

    Args:
        item: Pytest test item
        call: Pytest call info

    Yields:
        None
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ==================== Standard User Credentials ====================


@pytest.fixture
def standard_user() -> dict:
    """
    Provide standard user credentials.

    Returns:
        Dictionary with username and password
    """
    return {
        "username": settings.STANDARD_USER,
        "password": settings.PASSWORD,
    }


@pytest.fixture
def locked_user() -> dict:
    """
    Provide locked out user credentials.

    Returns:
        Dictionary with username and password
    """
    return {
        "username": settings.LOCKED_OUT_USER,
        "password": settings.PASSWORD,
    }

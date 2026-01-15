"""
Checkout Page Objects for Sauce Demo application.
Handles checkout information, overview, and completion.
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CheckoutStepOneLocators:
    """Locators for the Checkout Step One (Information) page."""

    HEADER_TITLE = ".title"
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BTN = "[data-test='continue']"
    CANCEL_BTN = "[data-test='cancel']"
    ERROR_MESSAGE = "[data-test='error']"
    ERROR_BUTTON = ".error-button"


class CheckoutStepTwoLocators:
    """Locators for the Checkout Step Two (Overview) page."""

    HEADER_TITLE = ".title"
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    PAYMENT_INFO = ".summary_value_label"
    SUBTOTAL = ".summary_subtotal_label"
    TAX = ".summary_tax_label"
    TOTAL = ".summary_total_label"
    FINISH_BTN = "[data-test='finish']"
    CANCEL_BTN = "[data-test='cancel']"


class CheckoutCompleteLocators:
    """Locators for the Checkout Complete page."""

    HEADER_TITLE = ".title"
    COMPLETE_HEADER = ".complete-header"
    COMPLETE_TEXT = ".complete-text"
    PONY_EXPRESS_IMG = ".pony_express"
    BACK_HOME_BTN = "[data-test='back-to-products']"


class CheckoutStepOnePage(BasePage):
    """
    Page Object for Checkout Step One (Customer Information).

    Handles entering customer information for checkout.
    """

    def __init__(self, page: Page) -> None:
        """Initialize the Checkout Step One Page."""
        super().__init__(page)
        self.locators = CheckoutStepOneLocators

    def open(self) -> "CheckoutStepOnePage":
        """
        Navigate directly to checkout step one.

        Returns:
            Self for method chaining
        """
        logger.info("Opening checkout step one")
        self.navigate("checkout-step-one.html")
        return self

    def enter_first_name(self, first_name: str) -> "CheckoutStepOnePage":
        """
        Enter first name.

        Args:
            first_name: Customer's first name

        Returns:
            Self for method chaining
        """
        logger.debug(f"Entering first name: {first_name}")
        self.fill(self.locators.FIRST_NAME_INPUT, first_name)
        return self

    def enter_last_name(self, last_name: str) -> "CheckoutStepOnePage":
        """
        Enter last name.

        Args:
            last_name: Customer's last name

        Returns:
            Self for method chaining
        """
        logger.debug(f"Entering last name: {last_name}")
        self.fill(self.locators.LAST_NAME_INPUT, last_name)
        return self

    def enter_postal_code(self, postal_code: str) -> "CheckoutStepOnePage":
        """
        Enter postal code.

        Args:
            postal_code: Customer's postal code

        Returns:
            Self for method chaining
        """
        logger.debug(f"Entering postal code: {postal_code}")
        self.fill(self.locators.POSTAL_CODE_INPUT, postal_code)
        return self

    def fill_checkout_info(
        self, first_name: str, last_name: str, postal_code: str
    ) -> "CheckoutStepOnePage":
        """
        Fill all checkout information fields.

        Args:
            first_name: Customer's first name
            last_name: Customer's last name
            postal_code: Customer's postal code

        Returns:
            Self for method chaining
        """
        logger.info("Filling checkout information")
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self

    def click_continue(self) -> None:
        """Click continue button to proceed to next step."""
        logger.info("Clicking continue")
        self.click(self.locators.CONTINUE_BTN)

    def click_cancel(self) -> None:
        """Click cancel button to go back to cart."""
        logger.info("Clicking cancel")
        self.click(self.locators.CANCEL_BTN)

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

    def close_error_message(self) -> "CheckoutStepOnePage":
        """
        Close the error message.

        Returns:
            Self for method chaining
        """
        if self.is_error_displayed():
            self.click(self.locators.ERROR_BUTTON)
        return self

    # Assertions
    def expect_on_checkout_step_one(self) -> None:
        """Assert that we are on checkout step one."""
        self.expect_url(".*checkout-step-one.*")
        expect(self.page.locator(self.locators.HEADER_TITLE)).to_have_text(
            "Checkout: Your Information"
        )

    def expect_error_message(self, expected_error: str | None = None) -> None:
        """
        Assert that an error is displayed.

        Args:
            expected_error: Optional expected error message
        """
        expect(self.page.locator(self.locators.ERROR_MESSAGE)).to_be_visible()
        if expected_error:
            expect(self.page.locator(self.locators.ERROR_MESSAGE)).to_contain_text(
                expected_error
            )


class CheckoutStepTwoPage(BasePage):
    """
    Page Object for Checkout Step Two (Order Overview).

    Handles reviewing order before completion.
    """

    def __init__(self, page: Page) -> None:
        """Initialize the Checkout Step Two Page."""
        super().__init__(page)
        self.locators = CheckoutStepTwoLocators

    def open(self) -> "CheckoutStepTwoPage":
        """
        Navigate directly to checkout step two.

        Returns:
            Self for method chaining
        """
        logger.info("Opening checkout step two")
        self.navigate("checkout-step-two.html")
        return self

    def get_item_names(self) -> list[str]:
        """
        Get names of all items in the order.

        Returns:
            List of item names
        """
        elements = self.page.locator(self.locators.ITEM_NAME).all()
        return [el.text_content() or "" for el in elements]

    def get_item_prices(self) -> list[float]:
        """
        Get prices of all items in the order.

        Returns:
            List of prices as floats
        """
        from utils.helpers import extract_price

        elements = self.page.locator(self.locators.ITEM_PRICE).all()
        return [extract_price(el.text_content() or "0") for el in elements]

    def get_subtotal(self) -> float:
        """
        Get the order subtotal.

        Returns:
            Subtotal amount
        """
        from utils.helpers import extract_price

        text = self.get_text(self.locators.SUBTOTAL)
        return extract_price(text)

    def get_tax(self) -> float:
        """
        Get the tax amount.

        Returns:
            Tax amount
        """
        from utils.helpers import extract_price

        text = self.get_text(self.locators.TAX)
        return extract_price(text)

    def get_total(self) -> float:
        """
        Get the order total.

        Returns:
            Total amount
        """
        from utils.helpers import extract_price

        text = self.get_text(self.locators.TOTAL)
        return extract_price(text)

    def click_finish(self) -> None:
        """Click finish button to complete the order."""
        logger.info("Clicking finish")
        self.click(self.locators.FINISH_BTN)

    def click_cancel(self) -> None:
        """Click cancel button to go back."""
        logger.info("Clicking cancel")
        self.click(self.locators.CANCEL_BTN)

    # Assertions
    def expect_on_checkout_step_two(self) -> None:
        """Assert that we are on checkout step two."""
        self.expect_url(".*checkout-step-two.*")
        expect(self.page.locator(self.locators.HEADER_TITLE)).to_have_text(
            "Checkout: Overview"
        )

    def expect_item_count(self, expected: int) -> None:
        """
        Assert the number of items in the order.

        Args:
            expected: Expected number of items
        """
        expect(self.page.locator(self.locators.CART_ITEM)).to_have_count(expected)

    def expect_total_correct(self) -> None:
        """Assert that total equals subtotal plus tax."""
        subtotal = self.get_subtotal()
        tax = self.get_tax()
        total = self.get_total()
        expected_total = round(subtotal + tax, 2)
        assert total == expected_total, f"Total {total} != subtotal {subtotal} + tax {tax}"
        logger.info(f"Total is correct: ${total}")


class CheckoutCompletePage(BasePage):
    """
    Page Object for the Checkout Complete page.

    Handles order completion confirmation.
    """

    def __init__(self, page: Page) -> None:
        """Initialize the Checkout Complete Page."""
        super().__init__(page)
        self.locators = CheckoutCompleteLocators

    def get_confirmation_header(self) -> str:
        """
        Get the confirmation header text.

        Returns:
            Confirmation header text
        """
        return self.get_text(self.locators.COMPLETE_HEADER)

    def get_confirmation_text(self) -> str:
        """
        Get the confirmation message text.

        Returns:
            Confirmation message text
        """
        return self.get_text(self.locators.COMPLETE_TEXT)

    def click_back_home(self) -> None:
        """Click back home button to return to inventory."""
        logger.info("Clicking back home")
        self.click(self.locators.BACK_HOME_BTN)

    # Assertions
    def expect_on_checkout_complete(self) -> None:
        """Assert that we are on the checkout complete page."""
        self.expect_url(".*checkout-complete.*")
        expect(self.page.locator(self.locators.HEADER_TITLE)).to_have_text(
            "Checkout: Complete!"
        )

    def expect_order_confirmed(self) -> None:
        """Assert that the order was confirmed successfully."""
        expect(self.page.locator(self.locators.COMPLETE_HEADER)).to_have_text(
            "Thank you for your order!"
        )
        expect(self.page.locator(self.locators.PONY_EXPRESS_IMG)).to_be_visible()
        logger.info("Order confirmed successfully")

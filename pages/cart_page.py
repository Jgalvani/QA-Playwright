"""
Cart Page Object for Sauce Demo application.
Handles shopping cart operations and verification.
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CartPageLocators:
    """Locators for the Cart Page elements."""

    # Header
    HEADER_TITLE = ".title"
    CART_BADGE = ".shopping_cart_badge"

    # Cart items
    CART_LIST = ".cart_list"
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_DESCRIPTION = ".inventory_item_desc"
    ITEM_PRICE = ".inventory_item_price"
    ITEM_QUANTITY = ".cart_quantity"
    REMOVE_BTN = "[data-test^='remove']"

    # Actions
    CONTINUE_SHOPPING_BTN = "[data-test='continue-shopping']"
    CHECKOUT_BTN = "[data-test='checkout']"


class CartPage(BasePage):
    """
    Page Object for the Shopping Cart page.

    Provides methods for:
    - Viewing cart contents
    - Removing items from cart
    - Proceeding to checkout
    """

    def __init__(self, page: Page) -> None:
        """Initialize the Cart Page."""
        super().__init__(page)
        self.locators = CartPageLocators

    def open(self) -> "CartPage":
        """
        Navigate directly to cart page.

        Returns:
            Self for method chaining
        """
        logger.info("Opening cart page")
        self.navigate("cart.html")
        return self

    # Cart item actions
    def get_cart_items_count(self) -> int:
        """
        Get the number of items in the cart.

        Returns:
            Number of items in cart
        """
        count = self.get_element_count(self.locators.CART_ITEM)
        logger.debug(f"Cart contains {count} items")
        return count

    def get_cart_item_names(self) -> list[str]:
        """
        Get names of all items in the cart.

        Returns:
            List of item names
        """
        elements = self.page.locator(self.locators.ITEM_NAME).all()
        names = [el.text_content() or "" for el in elements]
        logger.debug(f"Cart items: {names}")
        return names

    def get_cart_item_prices(self) -> list[float]:
        """
        Get prices of all items in the cart.

        Returns:
            List of prices as floats
        """
        from utils.helpers import extract_price

        elements = self.page.locator(self.locators.ITEM_PRICE).all()
        prices = [extract_price(el.text_content() or "0") for el in elements]
        logger.debug(f"Cart item prices: {prices}")
        return prices

    def get_total_price(self) -> float:
        """
        Calculate total price of items in cart.

        Returns:
            Total price
        """
        total = sum(self.get_cart_item_prices())
        logger.debug(f"Cart total: ${total:.2f}")
        return total

    def remove_item_by_name(self, item_name: str) -> "CartPage":
        """
        Remove an item from cart by its name.

        Args:
            item_name: Name of the item to remove

        Returns:
            Self for method chaining
        """
        data_test_name = item_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        selector = f"[data-test='remove-{data_test_name}']"
        self.click(selector)
        logger.info(f"Removed '{item_name}' from cart")
        return self

    def remove_item_by_index(self, index: int) -> "CartPage":
        """
        Remove an item from cart by its index.

        Args:
            index: Zero-based index of the item

        Returns:
            Self for method chaining
        """
        buttons = self.page.locator(self.locators.REMOVE_BTN).all()
        if index < len(buttons):
            buttons[index].click()
            logger.info(f"Removed item at index {index} from cart")
        else:
            raise IndexError(f"Item index {index} out of range")
        return self

    def remove_all_items(self) -> "CartPage":
        """
        Remove all items from the cart.

        Returns:
            Self for method chaining
        """
        logger.info("Removing all items from cart")
        while self.get_cart_items_count() > 0:
            self.remove_item_by_index(0)
        return self

    # Navigation
    def continue_shopping(self) -> None:
        """Go back to inventory page."""
        logger.info("Continuing shopping")
        self.click(self.locators.CONTINUE_SHOPPING_BTN)

    def proceed_to_checkout(self) -> None:
        """Proceed to checkout."""
        logger.info("Proceeding to checkout")
        self.click(self.locators.CHECKOUT_BTN)

    def click_on_item(self, item_name: str) -> None:
        """
        Click on an item to view its details.

        Args:
            item_name: Name of the item to click
        """
        logger.info(f"Clicking on item: {item_name}")
        self.page.get_by_text(item_name, exact=True).click()

    # Assertions
    def expect_on_cart_page(self) -> None:
        """Assert that we are on the cart page."""
        self.expect_url(".*cart.*")
        expect(self.page.locator(self.locators.HEADER_TITLE)).to_have_text("Your Cart")
        logger.info("On cart page")

    def expect_cart_empty(self) -> None:
        """Assert that the cart is empty."""
        expect(self.page.locator(self.locators.CART_ITEM)).to_have_count(0)
        logger.info("Cart is empty")

    def expect_cart_count(self, expected: int) -> None:
        """
        Assert the number of items in the cart.

        Args:
            expected: Expected number of items
        """
        expect(self.page.locator(self.locators.CART_ITEM)).to_have_count(expected)
        logger.info(f"Cart has {expected} items")

    def expect_item_in_cart(self, item_name: str) -> None:
        """
        Assert that a specific item is in the cart.

        Args:
            item_name: Name of the item to check
        """
        expect(self.page.get_by_text(item_name, exact=True)).to_be_visible()
        logger.info(f"Item '{item_name}' is in cart")

    def expect_item_not_in_cart(self, item_name: str) -> None:
        """
        Assert that a specific item is not in the cart.

        Args:
            item_name: Name of the item to check
        """
        expect(self.page.get_by_text(item_name, exact=True)).to_be_hidden()
        logger.info(f"Item '{item_name}' is not in cart")

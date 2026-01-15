"""
Inventory Page Object for Sauce Demo application.
Handles product listing, sorting, and cart operations.
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.logger import setup_logger

logger = setup_logger(__name__)


class InventoryPageLocators:
    """Locators for the Inventory Page elements."""

    # Header elements
    HEADER_TITLE = ".title"
    BURGER_MENU = "#react-burger-menu-btn"
    CART_LINK = ".shopping_cart_link"
    CART_BADGE = ".shopping_cart_badge"

    # Menu items
    MENU_CLOSE = "#react-burger-cross-btn"
    MENU_ALL_ITEMS = "#inventory_sidebar_link"
    MENU_ABOUT = "#about_sidebar_link"
    MENU_LOGOUT = "#logout_sidebar_link"
    MENU_RESET = "#reset_sidebar_link"

    # Product elements
    INVENTORY_LIST = ".inventory_list"
    INVENTORY_ITEM = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_DESCRIPTION = ".inventory_item_desc"
    ITEM_PRICE = ".inventory_item_price"
    ADD_TO_CART_BTN = "[data-test^='add-to-cart']"
    REMOVE_BTN = "[data-test^='remove']"

    # Sorting
    SORT_DROPDOWN = "[data-test='product-sort-container']"

    # Footer
    FOOTER = ".footer"
    SOCIAL_TWITTER = ".social_twitter"
    SOCIAL_FACEBOOK = ".social_facebook"
    SOCIAL_LINKEDIN = ".social_linkedin"


class InventoryPage(BasePage):
    """
    Page Object for the Inventory (Products) page.

    Provides methods for:
    - Viewing and sorting products
    - Adding/removing items from cart
    - Navigation through menu
    """

    def __init__(self, page: Page) -> None:
        """Initialize the Inventory Page."""
        super().__init__(page)
        self.locators = InventoryPageLocators

    def open(self) -> "InventoryPage":
        """
        Navigate directly to inventory page.

        Returns:
            Self for method chaining
        """
        logger.info("Opening inventory page")
        self.navigate("inventory.html")
        return self

    # Header actions
    def open_menu(self) -> "InventoryPage":
        """
        Open the burger menu.

        Returns:
            Self for method chaining
        """
        logger.debug("Opening burger menu")
        self.click(self.locators.BURGER_MENU)
        self.wait_for_element(self.locators.MENU_LOGOUT)
        return self

    def close_menu(self) -> "InventoryPage":
        """
        Close the burger menu.

        Returns:
            Self for method chaining
        """
        logger.debug("Closing burger menu")
        self.click(self.locators.MENU_CLOSE)
        return self

    def logout(self) -> None:
        """Logout from the application."""
        logger.info("Logging out")
        self.open_menu()
        self.click(self.locators.MENU_LOGOUT)

    def reset_app_state(self) -> "InventoryPage":
        """
        Reset the application state via menu.

        Returns:
            Self for method chaining
        """
        logger.info("Resetting app state")
        self.open_menu()
        self.click(self.locators.MENU_RESET)
        self.close_menu()
        return self

    def go_to_cart(self) -> None:
        """Navigate to the shopping cart."""
        logger.info("Going to cart")
        self.click(self.locators.CART_LINK)

    # Product actions
    def get_product_count(self) -> int:
        """
        Get the number of products displayed.

        Returns:
            Number of products
        """
        count = self.get_element_count(self.locators.INVENTORY_ITEM)
        logger.debug(f"Found {count} products")
        return count

    def get_product_names(self) -> list[str]:
        """
        Get all product names.

        Returns:
            List of product names
        """
        elements = self.page.locator(self.locators.ITEM_NAME).all()
        names = [el.text_content() or "" for el in elements]
        logger.debug(f"Product names: {names}")
        return names

    def get_product_prices(self) -> list[float]:
        """
        Get all product prices.

        Returns:
            List of prices as floats
        """
        from utils.helpers import extract_price

        elements = self.page.locator(self.locators.ITEM_PRICE).all()
        prices = [extract_price(el.text_content() or "0") for el in elements]
        logger.debug(f"Product prices: {prices}")
        return prices

    def add_product_to_cart_by_index(self, index: int) -> "InventoryPage":
        """
        Add a product to cart by its index.

        Args:
            index: Zero-based index of the product

        Returns:
            Self for method chaining
        """
        buttons = self.page.locator(self.locators.ADD_TO_CART_BTN).all()
        if index < len(buttons):
            buttons[index].click()
            logger.info(f"Added product at index {index} to cart")
        else:
            raise IndexError(f"Product index {index} out of range")
        return self

    def add_product_to_cart_by_name(self, product_name: str) -> "InventoryPage":
        """
        Add a product to cart by its name.

        Args:
            product_name: Name of the product to add

        Returns:
            Self for method chaining
        """
        # Convert product name to data-test attribute format
        data_test_name = product_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        selector = f"[data-test='add-to-cart-{data_test_name}']"
        self.click(selector)
        logger.info(f"Added '{product_name}' to cart")
        return self

    def remove_product_from_cart_by_name(self, product_name: str) -> "InventoryPage":
        """
        Remove a product from cart by its name.

        Args:
            product_name: Name of the product to remove

        Returns:
            Self for method chaining
        """
        data_test_name = product_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        selector = f"[data-test='remove-{data_test_name}']"
        self.click(selector)
        logger.info(f"Removed '{product_name}' from cart")
        return self

    def click_on_product(self, product_name: str) -> None:
        """
        Click on a product to view details.

        Args:
            product_name: Name of the product to click
        """
        logger.info(f"Clicking on product: {product_name}")
        self.page.get_by_text(product_name, exact=True).click()

    # Sorting actions
    def sort_by(self, option: str) -> "InventoryPage":
        """
        Sort products by a specific option.

        Args:
            option: Sort option value ('az', 'za', 'lohi', 'hilo')

        Returns:
            Self for method chaining
        """
        logger.info(f"Sorting by: {option}")
        self.select_option(self.locators.SORT_DROPDOWN, option)
        return self

    def sort_by_name_asc(self) -> "InventoryPage":
        """Sort products by name A to Z."""
        return self.sort_by("az")

    def sort_by_name_desc(self) -> "InventoryPage":
        """Sort products by name Z to A."""
        return self.sort_by("za")

    def sort_by_price_low_to_high(self) -> "InventoryPage":
        """Sort products by price low to high."""
        return self.sort_by("lohi")

    def sort_by_price_high_to_low(self) -> "InventoryPage":
        """Sort products by price high to low."""
        return self.sort_by("hilo")

    # Cart badge
    def get_cart_count(self) -> int:
        """
        Get the number of items in cart from badge.

        Returns:
            Number of items in cart (0 if badge not visible)
        """
        if self.is_visible(self.locators.CART_BADGE):
            text = self.get_text(self.locators.CART_BADGE)
            return int(text) if text else 0
        return 0

    # Assertions
    def expect_on_inventory_page(self) -> None:
        """Assert that we are on the inventory page."""
        self.expect_url(".*inventory.*")
        expect(self.page.locator(self.locators.HEADER_TITLE)).to_have_text("Products")
        logger.info("On inventory page")

    def expect_product_count(self, expected: int) -> None:
        """
        Assert the number of products displayed.

        Args:
            expected: Expected number of products
        """
        expect(self.page.locator(self.locators.INVENTORY_ITEM)).to_have_count(expected)

    def expect_cart_count(self, expected: int) -> None:
        """
        Assert the cart badge count.

        Args:
            expected: Expected cart count
        """
        if expected == 0:
            expect(self.page.locator(self.locators.CART_BADGE)).to_be_hidden()
        else:
            expect(self.page.locator(self.locators.CART_BADGE)).to_have_text(str(expected))

    def expect_products_sorted_by_name_asc(self) -> None:
        """Assert products are sorted by name A-Z."""
        names = self.get_product_names()
        assert names == sorted(names), f"Products not sorted A-Z: {names}"
        logger.info("Products correctly sorted A-Z")

    def expect_products_sorted_by_name_desc(self) -> None:
        """Assert products are sorted by name Z-A."""
        names = self.get_product_names()
        assert names == sorted(names, reverse=True), f"Products not sorted Z-A: {names}"
        logger.info("Products correctly sorted Z-A")

    def expect_products_sorted_by_price_asc(self) -> None:
        """Assert products are sorted by price low to high."""
        prices = self.get_product_prices()
        assert prices == sorted(prices), f"Products not sorted by price low-high: {prices}"
        logger.info("Products correctly sorted by price low-high")

    def expect_products_sorted_by_price_desc(self) -> None:
        """Assert products are sorted by price high to low."""
        prices = self.get_product_prices()
        assert prices == sorted(prices, reverse=True), f"Products not sorted by price high-low: {prices}"
        logger.info("Products correctly sorted by price high-low")

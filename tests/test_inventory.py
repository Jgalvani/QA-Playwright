"""
Inventory page tests for Sauce Demo application.
Tests cover product display, sorting, and cart operations from inventory.
"""

import pytest
from pages import InventoryPage, LoginPage


class TestInventoryDisplay:
    """Test cases for inventory display functionality."""

    @pytest.mark.smoke
    @pytest.mark.inventory
    def test_inventory_page_displays_products(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test that inventory page displays all products."""
        logged_in_inventory.expect_on_inventory_page()
        logged_in_inventory.expect_product_count(6)

    @pytest.mark.inventory
    def test_all_products_have_names(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test that all products have names displayed."""
        names = logged_in_inventory.get_product_names()
        assert len(names) == 6
        assert all(name for name in names)  # All names are non-empty

    @pytest.mark.inventory
    def test_all_products_have_prices(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test that all products have prices displayed."""
        prices = logged_in_inventory.get_product_prices()
        assert len(prices) == 6
        assert all(price > 0 for price in prices)  # All prices are positive

    @pytest.mark.inventory
    def test_product_details_link(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test clicking on product navigates to details page."""
        logged_in_inventory.click_on_product("Sauce Labs Backpack")
        logged_in_inventory.expect_url(".*inventory-item.*")


class TestInventorySorting:
    """Test cases for inventory sorting functionality."""

    @pytest.mark.inventory
    def test_sort_products_by_name_az(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test sorting products by name A to Z."""
        logged_in_inventory.sort_by_name_asc()
        logged_in_inventory.expect_products_sorted_by_name_asc()

    @pytest.mark.inventory
    def test_sort_products_by_name_za(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test sorting products by name Z to A."""
        logged_in_inventory.sort_by_name_desc()
        logged_in_inventory.expect_products_sorted_by_name_desc()

    @pytest.mark.inventory
    def test_sort_products_by_price_low_to_high(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test sorting products by price low to high."""
        logged_in_inventory.sort_by_price_low_to_high()
        logged_in_inventory.expect_products_sorted_by_price_asc()

    @pytest.mark.inventory
    def test_sort_products_by_price_high_to_low(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test sorting products by price high to low."""
        logged_in_inventory.sort_by_price_high_to_low()
        logged_in_inventory.expect_products_sorted_by_price_desc()

    @pytest.mark.inventory
    def test_default_sort_order(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test that default sort order is A-Z."""
        logged_in_inventory.expect_products_sorted_by_name_asc()


class TestAddToCartFromInventory:
    """Test cases for adding items to cart from inventory."""

    @pytest.mark.smoke
    @pytest.mark.inventory
    @pytest.mark.cart
    def test_add_single_item_to_cart(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test adding a single item to cart."""
        logged_in_inventory.expect_cart_count(0)
        logged_in_inventory.add_product_to_cart_by_name("Sauce Labs Backpack")
        logged_in_inventory.expect_cart_count(1)

    @pytest.mark.inventory
    @pytest.mark.cart
    def test_add_multiple_items_to_cart(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test adding multiple items to cart."""
        logged_in_inventory.add_product_to_cart_by_name("Sauce Labs Backpack")
        logged_in_inventory.add_product_to_cart_by_name("Sauce Labs Bike Light")
        logged_in_inventory.add_product_to_cart_by_name("Sauce Labs Bolt T-Shirt")
        logged_in_inventory.expect_cart_count(3)

    @pytest.mark.inventory
    @pytest.mark.cart
    def test_add_all_items_to_cart(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test adding all items to cart."""
        products = logged_in_inventory.get_product_names()
        for product in products:
            logged_in_inventory.add_product_to_cart_by_name(product)
        logged_in_inventory.expect_cart_count(6)

    @pytest.mark.inventory
    @pytest.mark.cart
    def test_remove_item_from_cart_on_inventory(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test removing an item from cart while on inventory page."""
        logged_in_inventory.add_product_to_cart_by_name("Sauce Labs Backpack")
        logged_in_inventory.expect_cart_count(1)
        logged_in_inventory.remove_product_from_cart_by_name("Sauce Labs Backpack")
        logged_in_inventory.expect_cart_count(0)

    @pytest.mark.inventory
    @pytest.mark.cart
    def test_cart_badge_updates_correctly(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test that cart badge updates when items are added/removed."""
        # Add items one by one and verify badge
        for i, product in enumerate(["Sauce Labs Backpack", "Sauce Labs Bike Light"], 1):
            logged_in_inventory.add_product_to_cart_by_name(product)
            logged_in_inventory.expect_cart_count(i)

        # Remove one item and verify
        logged_in_inventory.remove_product_from_cart_by_name("Sauce Labs Backpack")
        logged_in_inventory.expect_cart_count(1)


class TestInventoryNavigation:
    """Test cases for inventory navigation functionality."""

    @pytest.mark.inventory
    def test_navigate_to_cart(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test navigation from inventory to cart."""
        logged_in_inventory.go_to_cart()
        logged_in_inventory.expect_url(".*cart.*")

    @pytest.mark.inventory
    def test_logout_from_inventory(
        self, logged_in_inventory: InventoryPage, login_page: LoginPage
    ) -> None:
        """Test logging out from inventory page."""
        logged_in_inventory.logout()
        login_page.is_login_page_displayed()

    @pytest.mark.inventory
    def test_reset_app_state(
        self, logged_in_inventory: InventoryPage
    ) -> None:
        """Test resetting app state clears the cart."""
        # Add items to cart
        logged_in_inventory.add_product_to_cart_by_name("Sauce Labs Backpack")
        logged_in_inventory.add_product_to_cart_by_name("Sauce Labs Bike Light")
        logged_in_inventory.expect_cart_count(2)

        # Reset app state
        logged_in_inventory.reset_app_state()

        # Cart should be empty
        logged_in_inventory.expect_cart_count(0)


class TestInventoryAccess:
    """Test cases for inventory access control."""

    @pytest.mark.inventory
    @pytest.mark.negative
    def test_inventory_requires_login(
        self, inventory_page: InventoryPage, login_page: LoginPage
    ) -> None:
        """Test that inventory page requires authentication."""
        inventory_page.open()
        # Should be redirected to login or show error
        login_page.expect_login_failed("You can only access")

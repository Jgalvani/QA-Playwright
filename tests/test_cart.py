"""
Shopping cart tests for Sauce Demo application.
Tests cover cart operations, item management, and navigation.
"""

import pytest
from pages import CartPage, InventoryPage


class TestCartDisplay:
    """Test cases for cart display functionality."""

    @pytest.mark.cart
    def test_empty_cart_display(
        self, logged_in_inventory: InventoryPage, cart_page: CartPage
    ) -> None:
        """Test that empty cart is displayed correctly."""
        logged_in_inventory.go_to_cart()
        cart_page.expect_on_cart_page()
        cart_page.expect_cart_empty()

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_cart_with_one_item(
        self, cart_with_one_item: InventoryPage, cart_page: CartPage
    ) -> None:
        """Test cart display with one item."""
        cart_with_one_item.go_to_cart()
        cart_page.expect_on_cart_page()
        cart_page.expect_cart_count(1)
        cart_page.expect_item_in_cart("Sauce Labs Backpack")

    @pytest.mark.cart
    def test_cart_with_multiple_items(
        self, cart_with_multiple_items: InventoryPage, cart_page: CartPage
    ) -> None:
        """Test cart display with multiple items."""
        cart_with_multiple_items.go_to_cart()
        cart_page.expect_on_cart_page()
        cart_page.expect_cart_count(3)
        cart_page.expect_item_in_cart("Sauce Labs Backpack")
        cart_page.expect_item_in_cart("Sauce Labs Bike Light")
        cart_page.expect_item_in_cart("Sauce Labs Bolt T-Shirt")


class TestCartItemRemoval:
    """Test cases for removing items from cart."""

    @pytest.mark.cart
    def test_remove_single_item_from_cart(
        self, cart_with_one_item: InventoryPage, cart_page: CartPage
    ) -> None:
        """Test removing a single item from cart."""
        cart_with_one_item.go_to_cart()
        cart_page.remove_item_by_name("Sauce Labs Backpack")
        cart_page.expect_cart_empty()

    @pytest.mark.cart
    def test_remove_one_item_from_multiple(
        self, cart_with_multiple_items: InventoryPage, cart_page: CartPage
    ) -> None:
        """Test removing one item from cart with multiple items."""
        cart_with_multiple_items.go_to_cart()
        cart_page.remove_item_by_name("Sauce Labs Bike Light")
        cart_page.expect_cart_count(2)
        cart_page.expect_item_not_in_cart("Sauce Labs Bike Light")
        cart_page.expect_item_in_cart("Sauce Labs Backpack")
        cart_page.expect_item_in_cart("Sauce Labs Bolt T-Shirt")

    @pytest.mark.cart
    def test_remove_all_items_from_cart(
        self, cart_with_multiple_items: InventoryPage, cart_page: CartPage
    ) -> None:
        """Test removing all items from cart."""
        cart_with_multiple_items.go_to_cart()
        cart_page.remove_all_items()
        cart_page.expect_cart_empty()


class TestCartPricing:
    """Test cases for cart pricing functionality."""

    @pytest.mark.cart
    def test_cart_total_calculation(
        self, cart_with_multiple_items: InventoryPage, cart_page: CartPage
    ) -> None:
        """Test that cart total is calculated correctly."""
        cart_with_multiple_items.go_to_cart()
        prices = cart_page.get_cart_item_prices()
        total = cart_page.get_total_price()
        assert total == sum(prices), f"Cart total {total} != sum of prices {sum(prices)}"

    @pytest.mark.cart
    def test_cart_items_have_correct_prices(
        self, logged_in_inventory: InventoryPage, cart_page: CartPage
    ) -> None:
        """Test that cart items have correct prices from inventory."""
        # Get price from inventory
        inventory_prices = logged_in_inventory.get_product_prices()
        inventory_names = logged_in_inventory.get_product_names()

        # Add first item
        first_name = inventory_names[0]
        first_price = inventory_prices[0]
        logged_in_inventory.add_product_to_cart_by_name(first_name)

        # Verify price in cart
        logged_in_inventory.go_to_cart()
        cart_prices = cart_page.get_cart_item_prices()
        assert cart_prices[0] == first_price


class TestCartNavigation:
    """Test cases for cart navigation."""

    @pytest.mark.cart
    def test_continue_shopping_returns_to_inventory(
        self, cart_with_one_item: InventoryPage, cart_page: CartPage
    ) -> None:
        """Test that continue shopping returns to inventory."""
        cart_with_one_item.go_to_cart()
        cart_page.continue_shopping()
        cart_page.expect_url(".*inventory.*")

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_proceed_to_checkout(
        self, cart_with_one_item: InventoryPage, cart_page: CartPage
    ) -> None:
        """Test proceeding to checkout from cart."""
        cart_with_one_item.go_to_cart()
        cart_page.proceed_to_checkout()
        cart_page.expect_url(".*checkout-step-one.*")

    @pytest.mark.cart
    def test_click_on_cart_item_shows_details(
        self, cart_with_one_item: InventoryPage, cart_page: CartPage
    ) -> None:
        """Test clicking on cart item navigates to details."""
        cart_with_one_item.go_to_cart()
        cart_page.click_on_item("Sauce Labs Backpack")
        cart_page.expect_url(".*inventory-item.*")


class TestCartPersistence:
    """Test cases for cart persistence."""

    @pytest.mark.cart
    def test_cart_persists_after_navigation(
        self, cart_with_one_item: InventoryPage, cart_page: CartPage
    ) -> None:
        """Test that cart persists after navigating away and back."""
        cart_with_one_item.go_to_cart()
        cart_page.expect_cart_count(1)

        # Navigate away
        cart_page.continue_shopping()

        # Navigate back
        cart_with_one_item.go_to_cart()
        cart_page.expect_cart_count(1)
        cart_page.expect_item_in_cart("Sauce Labs Backpack")

    @pytest.mark.cart
    def test_cart_persists_after_product_details(
        self, cart_with_one_item: InventoryPage, cart_page: CartPage
    ) -> None:
        """Test that cart persists after viewing product details."""
        cart_with_one_item.go_to_cart()

        # Click on item to view details
        cart_page.click_on_item("Sauce Labs Backpack")
        cart_page.expect_url(".*inventory-item.*")

        # Go back to cart
        cart_page.go_back()
        cart_page.expect_cart_count(1)

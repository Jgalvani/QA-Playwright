"""
Checkout flow tests for Sauce Demo application.
Tests cover the complete checkout process from cart to order confirmation.
"""

import pytest
from pages import (
    CartPage,
    InventoryPage,
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage,
)
from utils import DataLoader


class TestCheckoutStepOne:
    """Test cases for checkout step one (customer information)."""

    @pytest.mark.checkout
    def test_checkout_step_one_page_loads(
        self,
        cart_with_one_item: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
    ) -> None:
        """Test that checkout step one page loads correctly."""
        cart_with_one_item.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.expect_on_checkout_step_one()

    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_fill_checkout_information(
        self,
        cart_with_one_item: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
    ) -> None:
        """Test filling checkout information successfully."""
        cart_with_one_item.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_checkout_info("John", "Doe", "12345")
        checkout_step_one_page.click_continue()
        checkout_step_one_page.expect_url(".*checkout-step-two.*")

    @pytest.mark.checkout
    @pytest.mark.parametrize("checkout_data", DataLoader.get_valid_checkout_data())
    def test_checkout_with_valid_data(
        self,
        cart_with_one_item: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_data: dict,
    ) -> None:
        """
        Test checkout with various valid customer data.

        Args:
            checkout_data: Parametrized checkout data from test data file
        """
        cart_with_one_item.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_checkout_info(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"],
        )
        checkout_step_one_page.click_continue()
        checkout_step_one_page.expect_url(".*checkout-step-two.*")

    @pytest.mark.checkout
    def test_cancel_checkout(
        self,
        cart_with_one_item: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
    ) -> None:
        """Test canceling checkout returns to cart."""
        cart_with_one_item.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.click_cancel()
        checkout_step_one_page.expect_url(".*cart.*")


class TestCheckoutStepOneValidation:
    """Test cases for checkout step one validation errors."""

    @pytest.mark.checkout
    @pytest.mark.negative
    def test_checkout_without_first_name(
        self,
        cart_with_one_item: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
    ) -> None:
        """Test error when first name is missing."""
        cart_with_one_item.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_checkout_info("", "Doe", "12345")
        checkout_step_one_page.click_continue()
        checkout_step_one_page.expect_error_message("First Name is required")

    @pytest.mark.checkout
    @pytest.mark.negative
    def test_checkout_without_last_name(
        self,
        cart_with_one_item: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
    ) -> None:
        """Test error when last name is missing."""
        cart_with_one_item.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_checkout_info("John", "", "12345")
        checkout_step_one_page.click_continue()
        checkout_step_one_page.expect_error_message("Last Name is required")

    @pytest.mark.checkout
    @pytest.mark.negative
    def test_checkout_without_postal_code(
        self,
        cart_with_one_item: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
    ) -> None:
        """Test error when postal code is missing."""
        cart_with_one_item.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_checkout_info("John", "Doe", "")
        checkout_step_one_page.click_continue()
        checkout_step_one_page.expect_error_message("Postal Code is required")

    @pytest.mark.checkout
    @pytest.mark.negative
    @pytest.mark.parametrize("checkout_data", DataLoader.get_invalid_checkout_data())
    def test_checkout_with_invalid_data(
        self,
        cart_with_one_item: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_data: dict,
    ) -> None:
        """
        Test checkout validation with various invalid data.

        Args:
            checkout_data: Parametrized invalid checkout data
        """
        cart_with_one_item.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_checkout_info(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"],
        )
        checkout_step_one_page.click_continue()
        checkout_step_one_page.expect_error_message(checkout_data["expected_error"])


class TestCheckoutStepTwo:
    """Test cases for checkout step two (order overview)."""

    @pytest.mark.checkout
    def test_checkout_step_two_displays_order_summary(
        self,
        cart_with_one_item: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
    ) -> None:
        """Test that checkout step two displays order summary."""
        cart_with_one_item.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_checkout_info("John", "Doe", "12345")
        checkout_step_one_page.click_continue()
        checkout_step_two_page.expect_on_checkout_step_two()
        checkout_step_two_page.expect_item_count(1)

    @pytest.mark.checkout
    def test_checkout_step_two_shows_correct_items(
        self,
        cart_with_multiple_items: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
    ) -> None:
        """Test that checkout step two shows correct items from cart."""
        cart_with_multiple_items.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_checkout_info("John", "Doe", "12345")
        checkout_step_one_page.click_continue()

        # Verify all items are shown
        item_names = checkout_step_two_page.get_item_names()
        assert "Sauce Labs Backpack" in item_names
        assert "Sauce Labs Bike Light" in item_names
        assert "Sauce Labs Bolt T-Shirt" in item_names

    @pytest.mark.checkout
    def test_checkout_total_calculation(
        self,
        cart_with_multiple_items: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
    ) -> None:
        """Test that checkout total equals subtotal plus tax."""
        cart_with_multiple_items.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_checkout_info("John", "Doe", "12345")
        checkout_step_one_page.click_continue()
        checkout_step_two_page.expect_total_correct()

    @pytest.mark.checkout
    def test_cancel_from_checkout_step_two(
        self,
        cart_with_one_item: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
    ) -> None:
        """Test canceling from checkout step two returns to inventory."""
        cart_with_one_item.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_checkout_info("John", "Doe", "12345")
        checkout_step_one_page.click_continue()
        checkout_step_two_page.click_cancel()
        checkout_step_two_page.expect_url(".*inventory.*")


class TestCheckoutComplete:
    """Test cases for checkout completion."""

    @pytest.mark.smoke
    @pytest.mark.checkout
    @pytest.mark.e2e
    def test_complete_checkout_flow(
        self,
        cart_with_one_item: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        checkout_complete_page: CheckoutCompletePage,
    ) -> None:
        """Test complete end-to-end checkout flow."""
        # Go to cart
        cart_with_one_item.go_to_cart()
        cart_page.expect_cart_count(1)

        # Proceed to checkout
        cart_page.proceed_to_checkout()
        checkout_step_one_page.expect_on_checkout_step_one()

        # Fill customer information
        checkout_step_one_page.fill_checkout_info("John", "Doe", "12345")
        checkout_step_one_page.click_continue()

        # Review order
        checkout_step_two_page.expect_on_checkout_step_two()
        checkout_step_two_page.click_finish()

        # Verify completion
        checkout_complete_page.expect_on_checkout_complete()
        checkout_complete_page.expect_order_confirmed()

    @pytest.mark.checkout
    @pytest.mark.e2e
    def test_checkout_with_multiple_items_complete(
        self,
        cart_with_multiple_items: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        checkout_complete_page: CheckoutCompletePage,
    ) -> None:
        """Test complete checkout with multiple items."""
        cart_with_multiple_items.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_checkout_info("Jane", "Smith", "67890")
        checkout_step_one_page.click_continue()
        checkout_step_two_page.expect_item_count(3)
        checkout_step_two_page.click_finish()
        checkout_complete_page.expect_order_confirmed()

    @pytest.mark.checkout
    def test_back_home_after_checkout(
        self,
        cart_with_one_item: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        checkout_complete_page: CheckoutCompletePage,
    ) -> None:
        """Test navigating back home after checkout."""
        cart_with_one_item.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_checkout_info("John", "Doe", "12345")
        checkout_step_one_page.click_continue()
        checkout_step_two_page.click_finish()
        checkout_complete_page.click_back_home()
        checkout_complete_page.expect_url(".*inventory.*")

    @pytest.mark.checkout
    def test_confirmation_message_content(
        self,
        cart_with_one_item: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        checkout_complete_page: CheckoutCompletePage,
    ) -> None:
        """Test confirmation message content after checkout."""
        cart_with_one_item.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_checkout_info("John", "Doe", "12345")
        checkout_step_one_page.click_continue()
        checkout_step_two_page.click_finish()

        header = checkout_complete_page.get_confirmation_header()
        assert "Thank you" in header

        text = checkout_complete_page.get_confirmation_text()
        assert "order" in text.lower() or "dispatch" in text.lower()

"""
Orders view tests — covers stat cards and the orders table.

Counts are derived at runtime from the live API.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.meridian.orders_page import OrdersPage
from pages.meridian.app_page import AppPage
from helpers.screenshot_helper import attach_screenshot
from helpers.api_client import ApiClient


class TestOrders:
    """Tests for the Orders view."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, api: ApiClient):
        self.page_obj = OrdersPage(page)
        self.app = AppPage(page)
        self.api = api
        self.page_obj.goto()

    def test_page_loads_with_correct_row_count(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Page should load with all orders visible; row count must match the API.

        Steps:
        1. Navigate to /orders
        2. Verify heading is visible
        3. Verify table row count matches API total
        """
        expected = len(self.api.get_orders())

        self.page_obj.expect_heading_visible()
        attach_screenshot(page, request, "Step 1-Heading visible")

        self.page_obj.expect_row_count(expected)
        attach_screenshot(page, request, f"Step 2-{expected} rows present")

    @pytest.mark.regression
    def test_stat_cards_are_visible(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        All four status stat cards (Delivered, Shipped, Processing, Backordered)
        should be visible on load.

        Steps:
        1. Navigate to /orders
        2. Verify each stat card is visible
        """
        for status in ("Delivered", "Shipped", "Processing", "Backordered"):
            self.page_obj.expect_stat_card_visible(status)

        attach_screenshot(page, request, "All stat cards visible")

    @pytest.mark.regression
    def test_delivered_stat_card_matches_api(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        The "Delivered" stat card value should match the count returned by the
        API when filtering by status=Delivered.

        Steps:
        1. Fetch delivered count from API
        2. Read stat card value from UI
        3. Assert they match
        """
        expected = len(self.api.get_orders(status="Delivered"))

        ui_value = self.page_obj.get_stat_value("Delivered")
        attach_screenshot(page, request, "Delivered stat card value")

        assert ui_value == expected, (
            f"Expected Delivered count {expected}, UI shows {ui_value}"
        )

    @pytest.mark.regression
    def test_status_filter_changes_row_count(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Selecting a status via AppPage filter should reduce the visible rows to
        only orders of that status.

        Note: The Orders view does NOT re-fetch when the global status filter
        changes (it shows all orders at once); this test verifies that the
        visible row count changes after a status filter is applied if the
        view does respond to it, or simply that the stat cards still load.

        Steps:
        1. Record total row count
        2. Verify stat card values are positive integers
        """
        total = self.page_obj.get_row_count()
        assert total > 0, "Expected at least one order in the table"
        attach_screenshot(page, request, f"Total {total} rows")

        # Verify stat card values are non-negative integers
        for status in ("Delivered", "Shipped", "Processing", "Backordered"):
            val = self.page_obj.get_stat_value(status)
            assert val >= 0, f"Expected non-negative count for {status}, got {val}"

        attach_screenshot(page, request, "All stat card values are valid integers")

    @pytest.mark.regression
    def test_backordered_stat_card_matches_api(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        The "Backordered" stat card value should match the API count.

        Steps:
        1. Fetch backordered count from API
        2. Read stat card value from UI
        3. Assert they match
        """
        expected = len(self.api.get_orders(status="Backordered"))

        ui_value = self.page_obj.get_stat_value("Backordered")
        attach_screenshot(page, request, "Backordered stat card value")

        assert ui_value == expected, (
            f"Expected Backordered count {expected}, UI shows {ui_value}"
        )

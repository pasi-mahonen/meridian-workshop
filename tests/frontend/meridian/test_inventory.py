"""
Inventory view tests — covers the stock levels table, search, and filters.

Row counts are derived at runtime from the live API so the tests remain
valid if the underlying mock data changes.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.meridian.inventory_page import InventoryPage
from pages.meridian.app_page import AppPage
from helpers.screenshot_helper import attach_screenshot
from helpers.api_client import ApiClient


class TestInventory:
    """Tests for the Inventory view."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, api: ApiClient):
        self.page_obj = InventoryPage(page)
        self.app = AppPage(page)
        self.api = api
        self.page_obj.goto()

    def test_page_loads_with_correct_item_count(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Page should load with a heading visible and a row count that matches
        the API with no filters applied.

        Steps:
        1. Navigate to /inventory
        2. Verify heading is visible
        3. Verify table row count matches API
        """
        expected = len(self.api.get_inventory())

        self.page_obj.expect_heading_visible()
        attach_screenshot(page, request, "Step 1-Heading visible")

        self.page_obj.expect_row_count(expected)
        attach_screenshot(page, request, f"Step 2-{expected} rows present")

    @pytest.mark.regression
    def test_search_filters_rows(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Searching by a term that matches a subset of items should reduce the
        row count below the full count.

        Steps:
        1. Record full row count from API
        2. Type "Sensor" into the search box
        3. Verify row count is less than the full count and greater than zero
        """
        full_count = len(self.api.get_inventory())

        self.page_obj.search("Sensor")
        attach_screenshot(page, request, "Step 1-After search 'Sensor'")

        filtered_count = self.page_obj.get_row_count()
        assert 0 < filtered_count < full_count, (
            f"Expected search to filter rows: full={full_count}, "
            f"filtered={filtered_count}"
        )
        attach_screenshot(page, request, f"Step 2-{filtered_count} rows after search")

    @pytest.mark.regression
    def test_clear_search_restores_full_count(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Clearing the search box should restore the full item count.

        Steps:
        1. Search for "Sensor" to reduce the list
        2. Clear the search
        3. Verify row count is back to the full API count
        """
        full_count = len(self.api.get_inventory())

        self.page_obj.search("Sensor")
        filtered_count = self.page_obj.get_row_count()
        assert filtered_count < full_count, "Search should have filtered rows"
        attach_screenshot(page, request, "Step 1-Search applied")

        self.page_obj.clear_search()
        attach_screenshot(page, request, "Step 2-Search cleared")

        self.page_obj.expect_row_count(full_count)
        attach_screenshot(page, request, f"Step 3-All {full_count} rows restored")

    @pytest.mark.regression
    def test_search_input_value_reflects_query(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        The search input value should match the text that was typed.

        Steps:
        1. Type "Circuit" into the search box
        2. Verify the input value equals "Circuit"
        """
        self.page_obj.search("Circuit")
        attach_screenshot(page, request, "After typing 'Circuit'")

        value = self.page_obj.get_search_input_value()
        assert value == "Circuit", f"Expected search value 'Circuit', got '{value}'"

    @pytest.mark.regression
    def test_warehouse_filter_changes_row_count(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Selecting a warehouse from the Location filter should change the row
        count to match the API response for that warehouse.

        Steps:
        1. Get the Tokyo item count from the API
        2. Select "Tokyo" in the Location filter
        3. Verify row count matches
        """
        warehouse = "Tokyo"
        expected = len(self.api.get_inventory(warehouse=warehouse))

        self.app.select_location(warehouse)
        self.page_obj.page.wait_for_load_state("networkidle")
        attach_screenshot(page, request, f"Step 1-Location filter {warehouse}")

        self.page_obj.expect_row_count(expected)
        attach_screenshot(page, request, f"Step 2-{expected} rows for {warehouse}")

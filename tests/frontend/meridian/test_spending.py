"""
Finance/Spending view tests — covers KPI stat cards and category spending.

This view derives its data from /api/spending/* and /api/orders endpoints; no
row-count assertion is made against a single "get_spending()" call since the
view aggregates multiple endpoints.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.meridian.spending_page import SpendingPage
from helpers.screenshot_helper import attach_screenshot
from helpers.api_client import ApiClient


class TestSpending:
    """Tests for the Finance/Spending view."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, api: ApiClient):
        self.page_obj = SpendingPage(page)
        self.api = api
        self.page_obj.goto()

    def test_page_loads_with_heading(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        The page should load and the heading should be visible.

        Steps:
        1. Navigate to /spending
        2. Verify heading is visible
        """
        self.page_obj.expect_heading_visible()
        attach_screenshot(page, request, "Heading visible")

    @pytest.mark.regression
    def test_stat_cards_are_visible(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        All four KPI stat cards should be visible: Total Revenue, Total Costs,
        Net Profit, and Avg Order Value.

        Steps:
        1. Navigate to /spending
        2. Verify each stat card label is visible
        """
        labels = ["Total Revenue", "Total Costs", "Net Profit", "Avg Order Value"]
        for label in labels:
            self.page_obj.expect_stat_card_visible(label)

        attach_screenshot(page, request, "All KPI stat cards visible")

    @pytest.mark.regression
    def test_stat_card_values_are_non_empty(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Each KPI stat card value should contain a non-empty currency string.

        Steps:
        1. Navigate to /spending
        2. Read each stat card value
        3. Verify none are empty
        """
        labels = ["Total Revenue", "Total Costs", "Net Profit", "Avg Order Value"]
        for label in labels:
            value = self.page_obj.get_stat_value(label)
            assert value, f"Stat card '{label}' has an empty value"

        attach_screenshot(page, request, "All stat card values populated")

    @pytest.mark.regression
    def test_category_spending_section_shows_categories(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        The category spending section should show at least as many categories
        as the API returns.

        Steps:
        1. Get category count from API
        2. Verify UI category count matches
        """
        api_categories = self.api.get_spending_categories()
        expected_count = len(api_categories)
        assert expected_count > 0, "API returned no categories — check mock data"

        ui_count = self.page_obj.get_category_count()
        attach_screenshot(page, request, f"Category list: {ui_count} items")

        assert ui_count == expected_count, (
            f"Expected {expected_count} categories, UI shows {ui_count}"
        )

    @pytest.mark.regression
    def test_category_names_are_visible(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Each category name in the spending breakdown should be readable
        (non-empty visible text — guards against the dark-mode invisible-text bug).

        Steps:
        1. Read all category names from the UI
        2. Verify each name is a non-empty string
        """
        names = self.page_obj.get_category_names()
        assert names, "No category names found in the spending section"

        for name in names:
            assert name.strip(), f"A category name is empty or whitespace: '{name}'"

        attach_screenshot(page, request, f"Category names: {names}")

    @pytest.mark.regression
    def test_category_list_is_visible(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        The category spending list container should be present and visible.

        Steps:
        1. Navigate to /spending
        2. Assert .category-list element is visible
        """
        self.page_obj.expect_category_list_visible()
        attach_screenshot(page, request, "Category list visible")

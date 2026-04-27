"""
Demand Forecast view tests — covers trend cards and the forecast table.

Counts are derived at runtime from the live API.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.meridian.demand_page import DemandPage
from helpers.screenshot_helper import attach_screenshot
from helpers.api_client import ApiClient


class TestDemand:
    """Tests for the Demand Forecast view."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, api: ApiClient):
        self.page_obj = DemandPage(page)
        self.api = api
        self.page_obj.goto()

    def test_page_loads_with_correct_row_count(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Page should load with a heading and a table whose row count matches the
        total number of demand forecasts from the API.

        Steps:
        1. Navigate to /demand
        2. Verify heading is visible
        3. Verify table row count matches API
        """
        expected = len(self.api.get_demand())

        self.page_obj.expect_heading_visible()
        attach_screenshot(page, request, "Step 1-Heading visible")

        self.page_obj.expect_row_count(expected)
        attach_screenshot(page, request, f"Step 2-{expected} rows present")

    @pytest.mark.regression
    def test_trend_cards_are_visible(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        All three trend cards (increasing, stable, decreasing) should be
        visible on load.

        Steps:
        1. Navigate to /demand
        2. Verify each trend card is visible
        """
        for trend in ("increasing", "stable", "decreasing"):
            self.page_obj.expect_trend_card_visible(trend)

        attach_screenshot(page, request, "All three trend cards visible")

    @pytest.mark.regression
    def test_increasing_trend_card_count_matches_api(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        The "increasing" trend card should display the count of forecasts with
        trend == "increasing" from the API.

        Steps:
        1. Count increasing-trend items from API
        2. Read the count from the UI trend card
        3. Assert they match
        """
        all_forecasts = self.api.get_demand()
        expected = sum(1 for f in all_forecasts if f["trend"] == "increasing")

        ui_count = self.page_obj.get_trend_count("increasing")
        attach_screenshot(page, request, "Increasing trend card count")

        assert ui_count == expected, (
            f"Expected {expected} increasing items, UI shows {ui_count}"
        )

    @pytest.mark.regression
    def test_stable_trend_card_count_matches_api(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        The "stable" trend card count should match the API.

        Steps:
        1. Count stable-trend items from API
        2. Read the count from the UI trend card
        3. Assert they match
        """
        all_forecasts = self.api.get_demand()
        expected = sum(1 for f in all_forecasts if f["trend"] == "stable")

        ui_count = self.page_obj.get_trend_count("stable")
        attach_screenshot(page, request, "Stable trend card count")

        assert ui_count == expected, (
            f"Expected {expected} stable items, UI shows {ui_count}"
        )

    @pytest.mark.regression
    def test_decreasing_trend_card_count_matches_api(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        The "decreasing" trend card count should match the API.

        Steps:
        1. Count decreasing-trend items from API
        2. Read the count from the UI trend card
        3. Assert they match
        """
        all_forecasts = self.api.get_demand()
        expected = sum(1 for f in all_forecasts if f["trend"] == "decreasing")

        ui_count = self.page_obj.get_trend_count("decreasing")
        attach_screenshot(page, request, "Decreasing trend card count")

        assert ui_count == expected, (
            f"Expected {expected} decreasing items, UI shows {ui_count}"
        )

    @pytest.mark.regression
    def test_trend_card_counts_sum_to_total(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        The sum of all three trend card counts should equal the total table row
        count (every forecast belongs to exactly one trend).

        Steps:
        1. Read all three trend card counts from UI
        2. Read the table row count
        3. Assert the sum equals the row count
        """
        increasing = self.page_obj.get_trend_count("increasing")
        stable = self.page_obj.get_trend_count("stable")
        decreasing = self.page_obj.get_trend_count("decreasing")
        total_cards = increasing + stable + decreasing

        row_count = self.page_obj.get_table_row_count()

        attach_screenshot(
            page, request,
            f"Trend counts: +{increasing} ={stable} -{decreasing}, rows={row_count}"
        )

        assert total_cards == row_count, (
            f"Sum of trend card counts ({total_cards}) != table rows ({row_count})"
        )

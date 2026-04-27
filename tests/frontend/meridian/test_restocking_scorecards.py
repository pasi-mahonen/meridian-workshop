"""
Restocking Recommendations scorecard tests.

Verifies the 4 KPI stat cards that appear above the budget row:
  - Items Recommended
  - Total Estimated Cost
  - Items Below Reorder
  - High Priority Items

Item counts are fetched from the live API so the tests remain valid if the
underlying mock data changes.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.meridian.restocking_page import RestockingPage
from helpers.screenshot_helper import attach_screenshot
from helpers.api_client import ApiClient

BUDGET_20K = 20_000


class TestRestockingScoreCards:
    """Tests for the KPI scorecard row on the Restocking Recommendations view."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, api: ApiClient):
        self.page_obj = RestockingPage(page)
        self.api = api
        self.page_obj.goto()

    def test_all_scorecards_are_visible(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        All 4 scorecard labels should be visible on initial load.

        Steps:
        1. Navigate to /restocking
        2. Verify each scorecard label is visible
        """
        labels = [
            "Items Recommended",
            "Total Estimated Cost",
            "Items Below Reorder",
            "High Priority Items",
        ]
        for label in labels:
            self.page_obj.expect_scorecard_visible(label)

        attach_screenshot(page, request, "All 4 scorecards visible")

    def test_items_recommended_matches_table(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        "Items Recommended" scorecard value should equal the data row count in
        the table, and both should equal what the API returns with no filters.

        Steps:
        1. Read the scorecard value for "Items Recommended"
        2. Read the table row count
        3. Assert they are equal and match the API
        """
        expected = len(self.api.get_restocking())

        scorecard_value = self.page_obj.get_scorecard_value("Items Recommended")
        row_count = self.page_obj.get_row_count()

        attach_screenshot(page, request, "Items Recommended vs table row count")

        assert int(scorecard_value) == row_count, (
            f"Scorecard shows '{scorecard_value}' but table has {row_count} rows"
        )
        assert row_count == expected, (
            f"Expected {expected} items from API, got {row_count}"
        )

    def test_scorecards_update_after_budget_filter(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        After applying a $20,000 budget, "Items Recommended" scorecard should
        update to reflect the items that fit within that budget.

        Steps:
        1. Verify baseline matches API (no budget)
        2. Apply $20,000 budget ceiling
        3. Verify scorecard matches API response for that budget
        """
        baseline_expected = len(self.api.get_restocking())
        budget_expected = len(self.api.get_restocking(budget=BUDGET_20K))

        # Step 1: Baseline
        baseline = self.page_obj.get_scorecard_value("Items Recommended")
        assert int(baseline) == baseline_expected, (
            f"Expected baseline of {baseline_expected}, got '{baseline}'"
        )
        attach_screenshot(page, request, f"Step 1-Baseline scorecard ({baseline_expected} items)")

        # Step 2: Apply budget
        self.page_obj.apply_budget(BUDGET_20K)
        attach_screenshot(page, request, "Step 2-Budget applied ($20k)")

        # Step 3: Scorecard updates to match API
        updated_value = self.page_obj.get_scorecard_value("Items Recommended")
        attach_screenshot(page, request, "Step 3-Scorecard after budget filter")

        assert updated_value == str(budget_expected), (
            f"Expected 'Items Recommended' scorecard to show '{budget_expected}' "
            f"after $20k budget, got '{updated_value}'"
        )

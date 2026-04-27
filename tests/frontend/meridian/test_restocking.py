"""
Restocking Recommendations tests — covers R2: budget ceiling feature.

Row counts and dollar amounts are derived at runtime from the live API so
the tests do not break if the underlying data changes.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.meridian.restocking_page import RestockingPage
from pages.meridian.app_page import AppPage
from helpers.screenshot_helper import attach_screenshot
from helpers.api_client import ApiClient

BUDGET_20K = 20_000
BUDGET_50K = 50_000


class TestRestocking:
    """Tests for the Restocking Recommendations view."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, api: ApiClient):
        self.page_obj = RestockingPage(page)
        self.app = AppPage(page)
        self.api = api
        self.page_obj.goto()

    def test_page_loads_with_recommendations(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Page should load with the heading and the API-expected number of items.

        Steps:
        1. Navigate to /restocking
        2. Verify heading is visible
        3. Verify table row count matches the API
        """
        expected = len(self.api.get_restocking())

        self.page_obj.expect_heading_visible()
        attach_screenshot(page, request, "Step 1-Heading visible")

        self.page_obj.expect_row_count(expected)
        attach_screenshot(page, request, f"Step 2-{expected} items present")

    @pytest.mark.regression
    def test_budget_ceiling_filters_to_fitting_items(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        A $20,000 budget ceiling should reduce the list to only those items
        whose estimated cost fits within the budget (greedy algorithm).

        Steps:
        1. Verify baseline row count matches API (no budget)
        2. Apply $20,000 budget
        3. Verify row count matches what the API returns for that budget
        4. Verify budget tag is shown
        """
        baseline = len(self.api.get_restocking())
        expected_with_budget = len(self.api.get_restocking(budget=BUDGET_20K))

        # Step 1: Confirm baseline
        self.page_obj.expect_row_count(baseline)
        attach_screenshot(page, request, "Step 1-Baseline items")

        # Step 2: Apply budget ceiling
        self.page_obj.apply_budget(BUDGET_20K)
        attach_screenshot(page, request, "Step 2-Budget applied")

        # Step 3: Row count should match API
        self.page_obj.expect_row_count(expected_with_budget)
        attach_screenshot(page, request, f"Step 3-{expected_with_budget} item(s) after budget")

        # Step 4: Budget tag visible in summary bar
        self.page_obj.expect_budget_tag_visible(BUDGET_20K)
        attach_screenshot(page, request, "Step 4-Budget tag visible")

    @pytest.mark.regression
    def test_budget_ceiling_50k_shows_multiple_items(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        A $50,000 budget should accommodate more than one item (verified via API).

        Steps:
        1. Ask API how many items fit in $50k
        2. Apply $50,000 budget
        3. Verify UI shows the expected count
        """
        expected = len(self.api.get_restocking(budget=BUDGET_50K))
        assert expected > 1, (
            f"API only returns {expected} item(s) for a $50k budget — "
            "test precondition not met; check mock data"
        )

        self.page_obj.apply_budget(BUDGET_50K)
        attach_screenshot(page, request, "Step 1-50k budget applied")

        self.page_obj.expect_row_count(expected)
        attach_screenshot(page, request, f"Step 2-{expected} items shown")

    @pytest.mark.regression
    def test_clear_budget_restores_all_items(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Clearing the budget ceiling should restore all recommendations.

        Steps:
        1. Apply $20,000 budget (reduces the list)
        2. Click the ✕ clear button
        3. Verify all items are back (count matches API with no budget)
        """
        all_count = len(self.api.get_restocking())
        budget_count = len(self.api.get_restocking(budget=BUDGET_20K))

        # Step 1: Narrow the list
        self.page_obj.apply_budget(BUDGET_20K)
        self.page_obj.expect_row_count(budget_count)
        attach_screenshot(page, request, f"Step 1-Budget applied ({budget_count} item(s))")

        # Step 2: Clear
        self.page_obj.clear_budget()
        attach_screenshot(page, request, "Step 2-Budget cleared")

        # Step 3: All items back
        self.page_obj.expect_row_count(all_count)
        attach_screenshot(page, request, f"Step 3-All {all_count} items restored")

    @pytest.mark.regression
    def test_location_filter_tokyo_shows_correct_count(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Selecting Tokyo in the Location filter should show only Tokyo items.

        Steps:
        1. Ask API for the Tokyo restocking count
        2. Select Tokyo from the Location filter
        3. Verify UI row count matches
        """
        location = "Tokyo"
        expected_count = len(self.api.get_restocking(warehouse=location))

        self.app.select_location(location)
        self.page_obj.page.wait_for_load_state("networkidle")
        attach_screenshot(page, request, f"Step 1-Location filter {location}")

        self.page_obj.expect_row_count(expected_count)
        attach_screenshot(page, request, f"Step 2-{expected_count} items for {location}")

    @pytest.mark.regression
    def test_location_filter_london_shows_correct_count(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        London filter should show only London restocking items.

        Steps:
        1. Ask API for the London restocking count
        2. Select London from the Location filter
        3. Verify UI row count matches
        """
        location = "London"
        expected_count = len(self.api.get_restocking(warehouse=location))

        self.app.select_location(location)
        self.page_obj.page.wait_for_load_state("networkidle")
        attach_screenshot(page, request, "Step 1-London filter applied")

        self.page_obj.expect_row_count(expected_count)
        attach_screenshot(page, request, f"Step 2-{expected_count} London item(s) shown")

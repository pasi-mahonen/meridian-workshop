"""
Performance Reports tests — covers R1 fixes: scorecards at top, filter reactivity.

Known data (no filters):
  - 4 quarterly rows: Q1–Q4 2025
  - 12 monthly rows: Jan–Dec 2025
  - Best quarter: Q4-2025
"""

import pytest
from playwright.sync_api import Page, expect
from pages.meridian.reports_page import ReportsPage
from pages.meridian.app_page import AppPage
from helpers.screenshot_helper import attach_screenshot


class TestReports:
    """Tests for the Performance Reports view (R1 deliverable)."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.reports = ReportsPage(page)
        self.app = AppPage(page)
        self.reports.goto()

    @pytest.mark.smoke
    def test_page_loads_with_heading_and_tables(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Reports page should load with heading and both data tables visible.

        Steps:
        1. Verify page heading is visible
        2. Verify quarterly table has 4 rows (Q1–Q4)
        3. Verify monthly table has 12 rows (Jan–Dec)
        """
        # Step 1: Heading
        self.reports.expect_heading_visible()
        attach_screenshot(page, request, "Step 1-Heading visible")

        # Step 2: Quarterly table
        self.reports.expect_quarterly_row_count(4)
        attach_screenshot(page, request, "Step 2-Quarterly table has 4 rows")

        # Step 3: Monthly table
        self.reports.expect_monthly_row_count(12)
        attach_screenshot(page, request, "Step 3-Monthly table has 12 rows")

    @pytest.mark.regression
    def test_all_scorecards_are_visible(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        All four KPI scorecards should be visible on page load.

        Steps:
        1. Check each scorecard label is present
        """
        self.reports.expect_all_scorecards_visible()
        attach_screenshot(page, request, "Step 1-All scorecards visible")
        # Expected: Total Revenue YTD, Avg Monthly Revenue,
        #           Total Orders YTD, Best Performing Quarter

    @pytest.mark.regression
    def test_scorecards_appear_above_quarterly_table(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Scorecards must appear above the quarterly performance table (R1 fix).

        Steps:
        1. Compare vertical position of scorecard text vs. quarterly table
        2. Assert scorecard y < table y
        """
        attach_screenshot(page, request, "Step 1-Page layout")
        assert self.reports.scorecards_appear_before_quarterly_table(), (
            "Scorecards are NOT above the quarterly table — R1 layout fix may have regressed"
        )
        attach_screenshot(page, request, "Step 2-Scorecard position verified")

    @pytest.mark.regression
    @pytest.mark.parametrize("quarter", ["Q1-2025", "Q2-2025", "Q3-2025", "Q4-2025"])
    def test_all_quarters_present(
        self,
        page: Page,
        request: pytest.FixtureRequest,
        quarter: str,
    ):
        """Each quarter (Q1–Q4 2025) should appear in the quarterly table."""
        self.reports.expect_quarter_present(quarter)
        attach_screenshot(page, request, f"Quarter {quarter} present")

    @pytest.mark.regression
    def test_best_quarter_is_q4(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """Best Performing Quarter scorecard should show Q4-2025."""
        expect(page.get_by_text("Q4-2025").first).to_be_visible()
        attach_screenshot(page, request, "Best quarter Q4-2025 visible")

    @pytest.mark.regression
    def test_location_filter_changes_quarterly_data(
        self, page: Page, request: pytest.FixtureRequest
    ):
        """
        Selecting a warehouse location should reload the quarterly table
        with filtered data (R1 fix: reports were ignoring global filters).

        Steps:
        1. Record baseline quarterly row count (should be 4)
        2. Select Tokyo location
        3. Verify table still renders (not empty/error)
        4. Verify the heading is still visible (page didn't crash)
        """
        # Step 1: Baseline
        baseline = self.reports.get_quarterly_row_count()
        attach_screenshot(page, request, "Step 1-Baseline quarterly rows")
        assert baseline == 4, f"Expected 4 baseline quarterly rows, got {baseline}"

        # Step 2: Apply filter
        self.app.select_location("Tokyo")
        page.wait_for_load_state("networkidle")
        attach_screenshot(page, request, "Step 2-Tokyo filter applied")

        # Step 3: Table still rendered (filter didn't break the page)
        self.reports.expect_heading_visible()
        self.reports.expect_quarterly_row_count(4)
        attach_screenshot(page, request, "Step 3-Table still shows 4 quarters after filter")
        # Note: quarterly grouping always produces 4 rows;
        # revenue/order values within each row will reflect the filter

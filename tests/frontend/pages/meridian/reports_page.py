"""
ReportsPage — scorecards, quarterly performance table, monthly trend table.

Key elements (from accessibility snapshot):
  - heading: "Performance Reports"
  - scorecards section: 4 stat cards (Total Revenue YTD, Avg Monthly Revenue,
    Total Orders YTD, Best Performing Quarter)
  - heading "Quarterly Performance" + table with 4 data rows (Q1–Q4)
  - heading "Month-over-Month Analysis" + table with 12 data rows
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ReportsPage(BasePage):
    """Page object for the /reports view."""

    def __init__(self, page: Page, base_url: str = "http://localhost:3000"):
        super().__init__(page, base_url)
        self.heading = page.get_by_role("heading", name="Performance Reports")
        self.quarterly_heading = page.get_by_role("heading", name="Quarterly Performance")
        self.monthly_heading = page.get_by_role("heading", name="Month-over-Month Analysis")
        # Tables — first table is quarterly, second is month-over-month
        self._tables = page.get_by_role("table")

    def goto(self) -> None:
        self.navigate("/reports")
        self.wait_for_load_state()

    # --- Scorecard helpers ---

    def get_scorecard_value(self, label: str) -> str:
        """Return the value text of a named scorecard."""
        scorecard = self.page.locator(".stat-card, .scorecard-item").filter(
            has_text=label
        )
        return scorecard.locator(".stat-value, .scorecard-value").first.inner_text()

    def expect_scorecard_visible(self, label: str) -> None:
        expect(self.page.get_by_text(label)).to_be_visible()

    # --- Quarterly table ---

    def get_quarterly_row_count(self) -> int:
        return self._tables.first.locator("tbody tr").count()

    def expect_quarterly_row_count(self, count: int) -> None:
        expect(self._tables.first.locator("tbody tr")).to_have_count(count)

    def expect_quarter_present(self, quarter: str) -> None:
        expect(self._tables.first.get_by_text(quarter)).to_be_visible()

    # --- Monthly table ---

    def get_monthly_row_count(self) -> int:
        return self._tables.last.locator("tbody tr").count()

    def expect_monthly_row_count(self, count: int) -> None:
        expect(self._tables.last.locator("tbody tr")).to_have_count(count)

    # --- Ordering check ---

    def scorecards_appear_before_quarterly_table(self) -> bool:
        """
        Verify scorecards section is above the quarterly table in the DOM.
        Returns True if the first table appears after the scorecard texts.
        """
        scorecard_box = self.page.get_by_text("Total Revenue (YTD)").bounding_box()
        table_box = self._tables.first.bounding_box()
        if scorecard_box and table_box:
            return scorecard_box["y"] < table_box["y"]
        return False

    # --- Assertions ---

    def expect_heading_visible(self) -> None:
        expect(self.heading).to_be_visible()

    def expect_all_scorecards_visible(self) -> None:
        for label in [
            "Total Revenue (YTD)",
            "Avg Monthly Revenue",
            "Total Orders (YTD)",
            "Best Performing Quarter",
        ]:
            self.expect_scorecard_visible(label)

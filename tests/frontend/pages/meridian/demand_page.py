"""
DemandPage — trend cards and demand forecast table.

Key elements:
  - heading: "Demand Forecast" (via i18n key demand.title)
  - 3 trend cards with class .trend-card, each containing a .trend-count
    element showing "{n} items" text
  - trend card classes: .increasing-card, .stable-card, .decreasing-card
  - table: single table with tbody rows (one per forecast)
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class DemandPage(BasePage):
    """Page object for the /demand view."""

    def __init__(self, page: Page, base_url: str = "http://localhost:3000"):
        super().__init__(page, base_url)
        self.table = page.get_by_role("table")

    def goto(self) -> None:
        self.navigate("/demand")
        self.wait_for_load_state()
        self.page.wait_for_timeout(300)

    # --- Table helpers ---

    def get_table_row_count(self) -> int:
        """Count data rows in the demand forecast table (excludes header)."""
        return self.table.locator("tbody tr").count()

    # --- Trend card helpers ---

    def get_trend_card(self, trend: str):
        """
        Return the locator for the trend card matching *trend*.

        *trend* should be one of: "increasing", "stable", "decreasing".
        """
        css_class = f".{trend}-card"
        return self.page.locator(css_class)

    def get_trend_count(self, trend: str) -> int:
        """
        Return the item count from the trend card for the given trend.

        Parses the text from the .trend-count element inside the card.
        The element contains text like "4 items" — returns the leading integer.
        """
        count_text = self.get_trend_card(trend).locator(".trend-count").inner_text()
        # Extract leading number from "N items" (i18n may vary the suffix)
        return int(count_text.strip().split()[0])

    # --- Assertions ---

    def expect_heading_visible(self) -> None:
        expect(self.page.get_by_role("heading", level=2)).to_be_visible()

    def expect_row_count(self, count: int) -> None:
        expect(self.table.locator("tbody tr")).to_have_count(count)

    def expect_trend_card_visible(self, trend: str) -> None:
        expect(self.get_trend_card(trend)).to_be_visible()

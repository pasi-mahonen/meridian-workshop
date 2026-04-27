"""
OrdersPage — stat cards and orders table.

Key elements:
  - heading: "Order Management" (via i18n key orders.title)
  - 4 stat cards: Delivered, Shipped, Processing, Backordered
    (labels come from t('status.*') — in English: "Delivered", "Shipped",
     "Processing", "Backordered")
  - table: single orders table with tbody rows
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class OrdersPage(BasePage):
    """Page object for the /orders view."""

    def __init__(self, page: Page, base_url: str = "http://localhost:3000"):
        super().__init__(page, base_url)
        self.table = page.get_by_role("table")

    def goto(self) -> None:
        self.navigate("/orders")
        self.wait_for_load_state()
        self.page.wait_for_timeout(300)

    # --- Table helpers ---

    def get_row_count(self) -> int:
        """Count data rows in the orders table (excludes header)."""
        return self.table.locator("tbody tr").count()

    # --- Stat card helpers ---

    def get_stat_value(self, status: str) -> int:
        """
        Return the integer value from the stat card whose label matches *status*.

        *status* should be the English label text, e.g. "Delivered", "Shipped",
        "Processing", "Backordered".
        """
        card = self.page.locator(".stat-card").filter(has_text=status)
        text = card.locator(".stat-value").inner_text()
        return int(text.strip())

    # --- Assertions ---

    def expect_heading_visible(self) -> None:
        expect(self.page.get_by_role("heading", level=2)).to_be_visible()

    def expect_row_count(self, count: int) -> None:
        expect(self.table.locator("tbody tr")).to_have_count(count)

    def expect_stat_card_visible(self, status: str) -> None:
        expect(self.page.locator(".stat-card").filter(has_text=status)).to_be_visible()

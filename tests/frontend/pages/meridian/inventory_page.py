"""
InventoryPage — stock levels table with search box.

Key elements:
  - heading: "Inventory Management" (via i18n key inventory.title)
  - card title contains "(N SKUs)" — use get_row_count() rather than parsing
  - search input: type="text" with placeholder containing "Search"
  - clear search: button that appears when input has content (contains an SVG,
    title attribute = "Clear search")
  - table: single table with tbody rows
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page object for the /inventory view."""

    def __init__(self, page: Page, base_url: str = "http://localhost:3000"):
        super().__init__(page, base_url)
        self.table = page.get_by_role("table")
        # The search input has a dynamic placeholder via i18n — match by CSS class
        self.search_input = page.locator("input.search-input")

    def goto(self) -> None:
        self.navigate("/inventory")
        self.wait_for_load_state()
        self.page.wait_for_timeout(300)

    # --- Table helpers ---

    def get_row_count(self) -> int:
        """Count data rows in the inventory table (excludes header)."""
        return self.table.locator("tbody tr").count()

    # --- Search helpers ---

    def search(self, query: str) -> None:
        """Fill the search box and wait for the table to filter."""
        self.search_input.fill(query)
        self.page.wait_for_timeout(300)

    def clear_search(self) -> None:
        """Click the ✕ clear button inside the search box."""
        self.page.locator("button.clear-search").click()
        self.page.wait_for_timeout(300)

    def get_search_input_value(self) -> str:
        """Return the current value of the search input."""
        return self.search_input.input_value()

    # --- Assertions ---

    def expect_heading_visible(self) -> None:
        expect(self.page.get_by_role("heading", level=2)).to_be_visible()

    def expect_row_count(self, count: int) -> None:
        expect(self.table.locator("tbody tr")).to_have_count(count)

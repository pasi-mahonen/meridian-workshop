"""
SpendingPage — Finance/Spending view with revenue KPI cards and category list.

Key elements:
  - heading: "Financial Overview" (via i18n key finance.title)
  - 4 stat cards in .stats-grid-finance: Total Revenue, Total Costs, Net Profit,
    Avg Order Value — each with .stat-label and .stat-value
  - category spending list: .category-item elements, each with .category-name
    and .category-amount
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class SpendingPage(BasePage):
    """Page object for the /spending view."""

    def __init__(self, page: Page, base_url: str = "http://localhost:3000"):
        super().__init__(page, base_url)
        self.stats_grid = page.locator(".stats-grid-finance")
        self.category_list = page.locator(".category-list")

    def goto(self) -> None:
        self.navigate("/spending")
        self.wait_for_load_state()
        self.page.wait_for_timeout(300)

    # --- Stat card helpers ---

    def get_stat_value(self, label: str) -> str:
        """
        Return the raw text from the stat value element for the given label.

        *label* is the English label text, e.g. "Total Revenue", "Net Profit".
        """
        card = self.stats_grid.locator(".stat-card").filter(has_text=label)
        return card.locator(".stat-value").first.inner_text().strip()

    # --- Category spending helpers ---

    def get_category_count(self) -> int:
        """Return the number of category spending items."""
        return self.category_list.locator(".category-item").count()

    def get_category_names(self) -> list[str]:
        """Return the visible text of all .category-name elements."""
        items = self.category_list.locator(".category-name").all()
        return [item.inner_text().strip() for item in items]

    def is_category_name_visible(self, name: str) -> bool:
        """Return True if a .category-name element containing *name* is visible."""
        locator = self.category_list.locator(".category-name").filter(has_text=name)
        return locator.is_visible()

    # --- Assertions ---

    def expect_heading_visible(self) -> None:
        expect(self.page.get_by_role("heading", level=2)).to_be_visible()

    def expect_stat_card_visible(self, label: str) -> None:
        expect(self.stats_grid.locator(".stat-card").filter(has_text=label)).to_be_visible()

    def expect_category_list_visible(self) -> None:
        expect(self.category_list).to_be_visible()

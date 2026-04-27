"""
AppPage — top-level navigation and filter bar, present on every Meridian page.

Nav links (from accessibility snapshot):
  Overview, Inventory, Orders, Finance, Demand Forecast, Reports, Restocking

Filter bar comboboxes (positional, 0-indexed):
  0 = Time Period, 1 = Location, 2 = Category, 3 = Order Status
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage

NAV_LINKS = [
    "Overview",
    "Inventory",
    "Orders",
    "Finance",
    "Demand Forecast",
    "Reports",
    "Restocking",
]


class AppPage(BasePage):
    """Shared navigation and filter bar for all Meridian views."""

    def __init__(self, page: Page, base_url: str = "http://localhost:3000"):
        super().__init__(page, base_url)
        self.nav = page.get_by_role("navigation")
        self.language_button = page.get_by_role("button", name="English")
        self._comboboxes = page.get_by_role("combobox")

    # --- Navigation ---

    def goto(self, path: str = "/") -> None:
        self.navigate(path)
        self.wait_for_load_state()

    def get_nav_link(self, name: str):
        return self.nav.get_by_role("link", name=name)

    def click_nav_link(self, name: str) -> None:
        self.get_nav_link(name).click()
        self.wait_for_load_state()

    def expect_nav_link_visible(self, name: str) -> None:
        expect(self.get_nav_link(name)).to_be_visible()

    # --- Language switcher ---

    def switch_to_japanese(self) -> None:
        """Open the language dropdown and select Japanese."""
        self.language_button.click()
        self.page.get_by_role("button", name="Japanese").click()

    # --- Filter bar (comboboxes are positional: 0=TimePeriod, 1=Location, 2=Category, 3=Status) ---

    def select_location(self, value: str) -> None:
        self._comboboxes.nth(1).select_option(value)

    def select_category(self, value: str) -> None:
        self._comboboxes.nth(2).select_option(value)

    def select_time_period(self, value: str) -> None:
        self._comboboxes.nth(0).select_option(value)

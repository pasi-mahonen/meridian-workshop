"""Base class shared by all Meridian page objects."""

from playwright.sync_api import Page, expect


class BasePage:
    """Common navigation and assertion helpers for all pages."""

    def __init__(self, page: Page, base_url: str = "http://localhost:3000"):
        self.page = page
        self.base_url = base_url

    def navigate(self, path: str = "") -> None:
        """Navigate to a path relative to base_url."""
        url = f"{self.base_url}{path}" if path else self.base_url
        self.page.goto(url)

    def wait_for_load_state(self, state: str = "networkidle") -> None:
        self.page.wait_for_load_state(state)

    def expect_url_contains(self, text: str) -> None:
        expect(self.page).to_have_url(text)

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

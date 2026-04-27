"""
Navigation smoke tests — verify all nav links exist and route correctly.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.meridian.app_page import AppPage, NAV_LINKS
from helpers.screenshot_helper import attach_screenshot


class TestNavigation:
    """Smoke tests for the top navigation bar."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.app = AppPage(page)
        self.app.goto("/")

    @pytest.mark.smoke
    @pytest.mark.parametrize("link_name", NAV_LINKS)
    def test_nav_link_is_visible(self, page: Page, request: pytest.FixtureRequest, link_name: str):
        """Every nav link must be visible on page load."""
        self.app.expect_nav_link_visible(link_name)
        attach_screenshot(page, request, f"nav_link_visible_{link_name}")

    @pytest.mark.smoke
    @pytest.mark.parametrize("link_name,expected_path", [
        ("Overview", "/"),
        ("Inventory", "/inventory"),
        ("Orders", "/orders"),
        ("Finance", "/spending"),
        ("Demand Forecast", "/demand"),
        ("Reports", "/reports"),
        ("Restocking", "/restocking"),
    ])
    def test_nav_link_navigates(
        self,
        page: Page,
        request: pytest.FixtureRequest,
        link_name: str,
        expected_path: str,
    ):
        """Clicking each nav link should land on the correct URL."""
        self.app.click_nav_link(link_name)
        attach_screenshot(page, request, f"after_click_{link_name}")
        expect(page).to_have_url(f"http://localhost:3000{expected_path}")

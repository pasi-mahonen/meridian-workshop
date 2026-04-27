"""Tests for dark mode toggle functionality."""

import pytest
from pages.meridian.dark_mode_page import DarkModePage
from helpers.screenshot_helper import attach_screenshot


@pytest.fixture
def dark_page(page):
    """DarkModePage POM, always starting in light mode."""
    pom = DarkModePage(page)
    pom.navigate_home()
    pom.clear_dark_mode_storage()
    return pom


class TestDarkMode:
    def test_dark_mode_toggle_applies_class(self, dark_page, request):
        """Clicking the toggle once should add 'dark' class to <html>."""
        attach_screenshot(dark_page.page, request, "before_toggle")
        assert not dark_page.is_dark_mode_active(), "Should start in light mode"

        dark_page.toggle_dark_mode()

        attach_screenshot(dark_page.page, request, "after_toggle")
        assert dark_page.is_dark_mode_active(), "'dark' class should be on <html> after toggle"

    def test_dark_mode_toggle_twice_removes_class(self, dark_page, request):
        """Clicking the toggle twice should remove 'dark' class from <html>."""
        dark_page.toggle_dark_mode()
        assert dark_page.is_dark_mode_active(), "Should be dark after first click"

        dark_page.toggle_dark_mode()

        attach_screenshot(dark_page.page, request, "after_second_toggle")
        assert not dark_page.is_dark_mode_active(), "'dark' class should be gone after second click"

    def test_dark_mode_persists_on_reload(self, dark_page, request):
        """Dark mode preference should survive a page reload."""
        dark_page.toggle_dark_mode()
        assert dark_page.is_dark_mode_active(), "Should be dark before reload"

        dark_page.page.reload()
        dark_page.page.wait_for_load_state("networkidle")

        attach_screenshot(dark_page.page, request, "after_reload")
        assert dark_page.is_dark_mode_active(), "'dark' class should be restored after reload"

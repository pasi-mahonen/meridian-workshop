"""Page object model for dark mode toggle interactions."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pages.base_page import BasePage


class DarkModePage(BasePage):
    """POM for dark mode toggle functionality."""

    def navigate_home(self) -> None:
        self.navigate("/")
        self.wait_for_load_state()

    def toggle_dark_mode(self) -> None:
        """Click the dark mode toggle button (matched by aria-label)."""
        btn = self.page.locator(
            "button[aria-label='Switch to dark mode'], button[aria-label='Switch to light mode']"
        )
        btn.click()

    def is_dark_mode_active(self) -> bool:
        """Return True if the html element has the 'dark' class."""
        return self.page.evaluate("document.documentElement.classList.contains('dark')")

    def clear_dark_mode_storage(self) -> None:
        """Remove the dark mode preference from localStorage and the class."""
        self.page.evaluate("localStorage.removeItem('meridian-dark-mode')")
        self.page.evaluate("document.documentElement.classList.remove('dark')")

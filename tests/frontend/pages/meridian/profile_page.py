"""Page object for profile menu, My Tasks modal, and Profile Details modal."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ProfilePage(BasePage):
    """POM covering the profile dropdown and both modals it opens."""

    def navigate_home(self) -> None:
        self.navigate("/")
        self.wait_for_load_state()

    # --- Profile dropdown ---

    def open_profile_dropdown(self) -> None:
        self.page.get_by_role("button", name="John Doe").click()

    def click_my_tasks(self) -> None:
        self.open_profile_dropdown()
        self.page.get_by_role("button", name="My Tasks").click()

    def click_profile_details(self) -> None:
        self.open_profile_dropdown()
        self.page.get_by_role("button", name="Profile Details").click()

    # --- My Tasks modal ---

    def expect_tasks_modal_visible(self) -> None:
        expect(self.page.get_by_role("heading", name="My Tasks")).to_be_visible()

    def expect_tasks_modal_hidden(self) -> None:
        expect(self.page.get_by_role("heading", name="My Tasks")).not_to_be_visible()

    def close_tasks_modal_via_button(self) -> None:
        # The × close button is inside the modal header
        self.page.locator(".modal-header .close-button").first.click()

    def close_tasks_modal_via_footer(self) -> None:
        self.page.get_by_role("button", name="Close").click()

    def get_task_items(self):
        return self.page.locator(".task-item")

    def get_pending_task_badge(self):
        return self.page.locator(".task-badge")

    # --- Profile Details modal ---

    def expect_profile_modal_visible(self) -> None:
        expect(self.page.get_by_role("heading", name="Profile Details")).to_be_visible()

    def expect_profile_modal_hidden(self) -> None:
        expect(self.page.get_by_role("heading", name="Profile Details")).not_to_be_visible()

    def close_profile_modal_via_button(self) -> None:
        self.page.locator(".modal-header .close-button").first.click()

    def close_profile_modal_via_footer(self) -> None:
        # The footer close button text varies by locale; match by role in the modal footer
        self.page.locator(".modal-footer .btn-secondary").click()

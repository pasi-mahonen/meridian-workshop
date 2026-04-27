"""Tests for the My Tasks and Profile Details modals accessed via the profile menu."""

import pytest
from playwright.sync_api import Page, expect
from pages.meridian.profile_page import ProfilePage
from helpers.screenshot_helper import attach_screenshot


@pytest.fixture
def profile(page: Page):
    pom = ProfilePage(page)
    pom.navigate_home()
    return pom


class TestMyTasksModal:
    """My Tasks modal opened from the profile dropdown."""

    @pytest.fixture(autouse=True)
    def setup(self, profile: ProfilePage):
        self.pom = profile

    def test_opens_from_profile_menu(self, page: Page, request: pytest.FixtureRequest):
        """Clicking My Tasks in the profile dropdown opens the modal."""
        self.pom.click_my_tasks()
        self.pom.expect_tasks_modal_visible()
        attach_screenshot(page, request, "tasks_modal_open")

    def test_shows_task_items(self, page: Page, request: pytest.FixtureRequest):
        """Modal lists the user's pending tasks."""
        self.pom.click_my_tasks()
        self.pom.expect_tasks_modal_visible()
        expect(page.get_by_text("Review Q4 inventory levels")).to_be_visible()
        expect(page.get_by_text("Approve Tokyo warehouse orders")).to_be_visible()
        attach_screenshot(page, request, "tasks_modal_items")

    def test_shows_four_tasks(self, page: Page, request: pytest.FixtureRequest):
        """All four mock tasks should be rendered."""
        self.pom.click_my_tasks()
        expect(self.pom.get_task_items()).to_have_count(4)
        attach_screenshot(page, request, "tasks_modal_count")

    def test_close_button_closes_modal(self, page: Page, request: pytest.FixtureRequest):
        """The × button in the modal header dismisses the modal."""
        self.pom.click_my_tasks()
        self.pom.expect_tasks_modal_visible()
        self.pom.close_tasks_modal_via_button()
        self.pom.expect_tasks_modal_hidden()
        attach_screenshot(page, request, "tasks_modal_closed_via_x")

    def test_footer_close_button_closes_modal(self, page: Page, request: pytest.FixtureRequest):
        """The Close button in the modal footer dismisses the modal."""
        self.pom.click_my_tasks()
        self.pom.expect_tasks_modal_visible()
        self.pom.close_tasks_modal_via_footer()
        self.pom.expect_tasks_modal_hidden()
        attach_screenshot(page, request, "tasks_modal_closed_via_footer")

    def test_profile_badge_shows_pending_count(self, page: Page, request: pytest.FixtureRequest):
        """Profile dropdown button shows the number of pending tasks."""
        self.pom.open_profile_dropdown()
        badge = self.pom.get_pending_task_badge()
        expect(badge).to_be_visible()
        expect(badge).to_have_text("4")
        attach_screenshot(page, request, "profile_task_badge")


class TestProfileDetailsModal:
    """Profile Details modal opened from the profile dropdown."""

    @pytest.fixture(autouse=True)
    def setup(self, profile: ProfilePage):
        self.pom = profile

    def test_opens_from_profile_menu(self, page: Page, request: pytest.FixtureRequest):
        """Clicking Profile Details in the dropdown opens the modal."""
        self.pom.click_profile_details()
        self.pom.expect_profile_modal_visible()
        attach_screenshot(page, request, "profile_details_modal_open")

    def test_shows_user_name(self, page: Page, request: pytest.FixtureRequest):
        """Modal displays the current user's name."""
        self.pom.click_profile_details()
        expect(page.get_by_text("John Doe").first).to_be_visible()
        attach_screenshot(page, request, "profile_details_name")

    def test_shows_user_email(self, page: Page, request: pytest.FixtureRequest):
        """Modal displays the user's email address."""
        self.pom.click_profile_details()
        expect(page.get_by_text("john.doe@catalystcomponents.com")).to_be_visible()
        attach_screenshot(page, request, "profile_details_email")

    def test_shows_department(self, page: Page, request: pytest.FixtureRequest):
        """Modal displays the user's department."""
        self.pom.click_profile_details()
        expect(page.get_by_text("Supply Chain Operations")).to_be_visible()
        attach_screenshot(page, request, "profile_details_department")

    def test_close_button_closes_modal(self, page: Page, request: pytest.FixtureRequest):
        """The × button in the modal header dismisses the modal."""
        self.pom.click_profile_details()
        self.pom.expect_profile_modal_visible()
        self.pom.close_profile_modal_via_button()
        self.pom.expect_profile_modal_hidden()
        attach_screenshot(page, request, "profile_details_closed_via_x")

    def test_footer_close_button_closes_modal(self, page: Page, request: pytest.FixtureRequest):
        """The footer button dismisses the Profile Details modal."""
        self.pom.click_profile_details()
        self.pom.expect_profile_modal_visible()
        self.pom.close_profile_modal_via_footer()
        self.pom.expect_profile_modal_hidden()
        attach_screenshot(page, request, "profile_details_closed_via_footer")

"""Pytest fixtures for Meridian frontend tests."""

import sys
from pathlib import Path

# Add tests/frontend to sys.path so pages/ and helpers/ are importable
sys.path.insert(0, str(Path(__file__).parent))

import pytest
from playwright.sync_api import Page
from helpers.screenshot_helper import take_screenshot_on_failure
from helpers.api_client import ApiClient


@pytest.fixture(autouse=True)
def setup_and_teardown(page: Page, request: pytest.FixtureRequest):
    """Capture a full-page screenshot automatically on test failure."""
    yield
    take_screenshot_on_failure(page, request)


@pytest.fixture(scope="session")
def api():
    """Session-scoped API client for fetching live data in assertions."""
    return ApiClient()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test result available to fixtures for failure screenshots."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

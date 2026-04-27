"""Screenshot utilities for attaching captures to pytest-html reports."""

import base64
from pathlib import Path
from playwright.sync_api import Page
import pytest


def attach_screenshot(
    page: Page,
    request: pytest.FixtureRequest,
    description: str,
    full_page: bool = False,
) -> bytes:
    """
    Capture a screenshot and attach it to the pytest-html report as an
    embedded base64 image so the report is fully self-contained.

    Args:
        page: Playwright page instance
        request: pytest request fixture
        description: Label for the screenshot (used in filename)
        full_page: Capture full scrollable page when True

    Returns:
        Screenshot bytes
    """
    screenshots_dir = Path("test-results/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    test_name = request.node.name
    safe_desc = description.replace(" ", "_").replace(":", "-")
    filepath = screenshots_dir / f"{test_name}_{safe_desc}.png"

    screenshot_bytes = page.screenshot(path=str(filepath), full_page=full_page)

    if hasattr(request.node, "add_report_section"):
        b64 = base64.b64encode(screenshot_bytes).decode("utf-8")
        request.node.add_report_section(
            "call",
            "screenshot",
            f'<img src="data:image/png;base64,{b64}" alt="{description}" style="max-width:100%;"/>',
        )

    return screenshot_bytes


def take_screenshot_on_failure(page: Page, request: pytest.FixtureRequest) -> None:
    """Capture a full-page screenshot when the test has failed."""
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        attach_screenshot(page, request, "FAILURE", full_page=True)

"""
RestockingPage — budget ceiling input, summary bar, and recommendations table.

Key elements (from accessibility snapshot):
  - heading: "Restocking Recommendations"
  - spinbutton: budget number input
  - button "Apply": applies budget ceiling
  - button "✕": clears budget (only visible when budget > 0)
  - summary text: "{n} items recommended" and "Total cost: ${amount}"
  - table with header row + data rows (one row per recommended item)
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class RestockingPage(BasePage):
    """Page object for the /restocking view."""

    def __init__(self, page: Page, base_url: str = "http://localhost:3000"):
        super().__init__(page, base_url)
        self.heading = page.get_by_role("heading", name="Restocking Recommendations")
        self.budget_input = page.get_by_role("spinbutton")
        self.apply_button = page.get_by_role("button", name="Apply")
        self.clear_button = page.get_by_role("button", name="✕")
        self.table = page.get_by_role("table")

    def goto(self) -> None:
        self.navigate("/restocking")
        self.wait_for_load_state()

    # --- Budget controls ---

    def apply_budget(self, amount: int) -> None:
        """Fill budget input and click Apply, then wait for table to reload."""
        self.budget_input.fill(str(amount))
        self.apply_button.click()
        self.page.wait_for_load_state("networkidle")

    def clear_budget(self) -> None:
        """Click the ✕ clear button (only present when budget > 0)."""
        self.clear_button.click()
        self.page.wait_for_load_state("networkidle")

    # --- Table helpers ---

    def get_data_rows(self):
        """Return all non-header table rows."""
        return self.table.get_by_role("row").filter(
            has_not=self.table.get_by_role("columnheader")
        )

    def get_row_count(self) -> int:
        """Count data rows (excludes header)."""
        rows = self.table.locator("tbody tr")
        return rows.count()

    def get_sku_in_row(self, row_index: int) -> str:
        """Return the SKU text from the given row (0-indexed)."""
        return self.table.locator("tbody tr").nth(row_index).locator("td").first.inner_text()

    # --- Summary bar ---

    def get_summary_text(self) -> str:
        return self.page.locator(".summary-bar").inner_text()

    # --- Assertions ---

    def expect_heading_visible(self) -> None:
        expect(self.heading).to_be_visible()

    def expect_row_count(self, count: int) -> None:
        expect(self.table.locator("tbody tr")).to_have_count(count)

    def expect_budget_tag_visible(self, amount: int) -> None:
        """The blue budget pill should show after Apply is clicked."""
        expect(self.page.locator(".budget-tag")).to_be_visible()
        expect(self.page.locator(".budget-tag")).to_contain_text(f"{amount:,}")

    # --- Scorecard helpers ---

    def expect_scorecard_visible(self, label: str) -> None:
        """Verify a scorecard with the given label is visible."""
        expect(self.page.get_by_text(label, exact=True)).to_be_visible()

    def get_scorecard_value(self, label: str) -> str:
        """Return the value text from the scorecard matching the given label."""
        scorecard = self.page.locator(".scorecard").filter(has_text=label)
        return scorecard.locator(".scorecard-value").inner_text()

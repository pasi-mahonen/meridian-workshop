"""Thin HTTP client for the Meridian backend API used in test fixtures."""

import requests

API_BASE = "http://localhost:8001/api"


class ApiClient:
    """Wraps requests calls to the Meridian API and returns parsed JSON."""

    def _get(self, path: str, params: dict) -> list | dict:
        """Issue a GET request, strip None/falsy values from params."""
        clean = {k: v for k, v in params.items() if v is not None}
        response = requests.get(f"{API_BASE}{path}", params=clean, timeout=10)
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    # Endpoints
    # ------------------------------------------------------------------

    def get_inventory(
        self,
        warehouse: str | None = None,
        category: str | None = None,
    ) -> list:
        """GET /api/inventory — returns list of inventory items."""
        return self._get(
            "/inventory",
            {"warehouse": warehouse, "category": category},
        )

    def get_restocking(
        self,
        budget: float | None = None,
        warehouse: str | None = None,
        category: str | None = None,
    ) -> list:
        """GET /api/restocking — returns list of restocking recommendations."""
        return self._get(
            "/restocking",
            {"budget": budget, "warehouse": warehouse, "category": category},
        )

    def get_orders(
        self,
        warehouse: str | None = None,
        category: str | None = None,
        status: str | None = None,
    ) -> list:
        """GET /api/orders — returns list of orders."""
        return self._get(
            "/orders",
            {"warehouse": warehouse, "category": category, "status": status},
        )

    def get_demand(
        self,
        warehouse: str | None = None,
        category: str | None = None,
    ) -> list:
        """GET /api/demand — returns list of demand forecasts.

        Note: the backend /api/demand endpoint does not accept filters;
        warehouse/category are accepted here for future-proofing but are
        currently ignored server-side.
        """
        return self._get("/demand", {})

    def get_spending(
        self,
        warehouse: str | None = None,
        category: str | None = None,
    ) -> dict:
        """GET /api/spending/summary — returns spending summary."""
        return self._get("/spending/summary", {})

    def get_spending_categories(self) -> list:
        """GET /api/spending/categories — returns category spending breakdown."""
        return self._get("/spending/categories", {})

    def get_reports(
        self,
        warehouse: str | None = None,
        category: str | None = None,
    ) -> list:
        """GET /api/reports/quarterly — returns quarterly performance data."""
        return self._get(
            "/reports/quarterly",
            {"warehouse": warehouse, "category": category},
        )

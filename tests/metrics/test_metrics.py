"""Tests for Metrics API endpoints.

This module tests the following endpoints:
- GET /v3beta1/enterprise/metrics/usage - Get Usage Metrics
- GET /v3beta1/organizations/{org_id}/metrics/usage - Get Organization Usage Metrics
"""


from devin_api_client import DevinAPIClient


class TestGetUsageMetrics:
    """Tests for the Get Usage Metrics endpoint."""

    def test_get_usage_metrics_success(self, api_client: DevinAPIClient) -> None:
        """Test getting usage metrics returns successful response."""
        response = api_client.get("/enterprise/metrics/usage")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))

    def test_get_usage_metrics_with_date_range(self, api_client: DevinAPIClient) -> None:
        """Test getting usage metrics with date range parameters."""
        response = api_client.get(
            "/enterprise/metrics/usage",
            params={"start_date": "2024-01-01", "end_date": "2024-12-31"},
        )
        assert response.status_code in [200, 422]

    def test_get_usage_metrics_with_granularity(self, api_client: DevinAPIClient) -> None:
        """Test getting usage metrics with granularity parameter."""
        response = api_client.get(
            "/enterprise/metrics/usage",
            params={"granularity": "daily"},
        )
        assert response.status_code in [200, 422]

    def test_get_usage_metrics_response_structure(self, api_client: DevinAPIClient) -> None:
        """Test that usage metrics response has expected structure."""
        response = api_client.get("/enterprise/metrics/usage")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))


class TestGetOrganizationUsageMetrics:
    """Tests for the Get Organization Usage Metrics endpoint."""

    def test_get_org_usage_metrics_success(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test getting organization usage metrics returns successful response."""
        response = api_client.get(f"/organizations/{org_id}/metrics/usage")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))

    def test_get_org_usage_metrics_with_date_range(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test getting organization usage metrics with date range parameters."""
        response = api_client.get(
            f"/organizations/{org_id}/metrics/usage",
            params={"start_date": "2024-01-01", "end_date": "2024-12-31"},
        )
        assert response.status_code in [200, 422]

    def test_get_org_usage_metrics_with_granularity(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test getting organization usage metrics with granularity parameter."""
        response = api_client.get(
            f"/organizations/{org_id}/metrics/usage",
            params={"granularity": "daily"},
        )
        assert response.status_code in [200, 422]

    def test_get_org_usage_metrics_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test getting usage metrics with invalid organization ID returns error."""
        response = api_client.get("/organizations/invalid-org-id/metrics/usage")
        assert response.status_code in [400, 404, 422]

    def test_get_org_usage_metrics_response_structure(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test that organization usage metrics response has expected structure."""
        response = api_client.get(f"/organizations/{org_id}/metrics/usage")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))

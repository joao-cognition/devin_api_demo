"""Tests for Audit Logs API endpoints.

This module tests the following endpoints:
- GET /v3beta1/enterprise/audit-logs - List Audit Logs
- GET /v3beta1/organizations/{org_id}/audit-logs - List Organization Audit Logs
"""


from devin_api_client import DevinAPIClient


class TestListAuditLogs:
    """Tests for the List Audit Logs endpoint."""

    def test_list_audit_logs_success(self, api_client: DevinAPIClient) -> None:
        """Test listing audit logs returns successful response."""
        response = api_client.get("/enterprise/audit-logs")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_list_audit_logs_with_limit(self, api_client: DevinAPIClient) -> None:
        """Test listing audit logs with limit parameter."""
        response = api_client.get("/enterprise/audit-logs", params={"limit": 5})
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) <= 5

    def test_list_audit_logs_with_offset(self, api_client: DevinAPIClient) -> None:
        """Test listing audit logs with offset parameter."""
        response = api_client.get("/enterprise/audit-logs", params={"offset": 0, "limit": 10})
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_list_audit_logs_with_action_filter(self, api_client: DevinAPIClient) -> None:
        """Test listing audit logs filtered by action type."""
        response = api_client.get("/enterprise/audit-logs", params={"action": "session.created"})
        assert response.status_code in [200, 422]

    def test_list_audit_logs_response_structure(self, api_client: DevinAPIClient) -> None:
        """Test that audit logs response has expected structure."""
        response = api_client.get("/enterprise/audit-logs", params={"limit": 1})
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        if data["items"]:
            log_entry = data["items"][0]
            assert "action" in log_entry or "event_type" in log_entry or "id" in log_entry


class TestListOrganizationAuditLogs:
    """Tests for the List Organization Audit Logs endpoint."""

    def test_list_org_audit_logs_success(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing organization audit logs returns successful response."""
        response = api_client.get(f"/organizations/{org_id}/audit-logs")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_list_org_audit_logs_with_limit(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing organization audit logs with limit parameter."""
        response = api_client.get(f"/organizations/{org_id}/audit-logs", params={"limit": 5})
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) <= 5

    def test_list_org_audit_logs_with_offset(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing organization audit logs with offset parameter."""
        response = api_client.get(
            f"/organizations/{org_id}/audit-logs", params={"offset": 0, "limit": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_list_org_audit_logs_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test listing audit logs with invalid organization ID."""
        response = api_client.get("/organizations/invalid-org-id/audit-logs")
        assert response.status_code in [400, 404, 422]

    def test_list_org_audit_logs_response_structure(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test that organization audit logs response has expected structure."""
        response = api_client.get(f"/organizations/{org_id}/audit-logs", params={"limit": 1})
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

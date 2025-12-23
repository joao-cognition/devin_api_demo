"""Tests for Consumption API endpoints.

This module tests the following endpoints:
- GET /v3beta1/enterprise/consumption/cycles - List Consumption Cycles
- GET /v3beta1/enterprise/consumption/daily - Get Daily Consumption
- GET /v3beta1/organizations/{org_id}/consumption/daily - Get Organization Daily Consumption
- GET /v3beta1/enterprise/users/{user_id}/consumption/daily - Get User Daily Consumption
- GET /v3beta1/sessions/{session_id}/consumption/daily - Get Session Daily Consumption
"""


from devin_api_client import DevinAPIClient


class TestListConsumptionCycles:
    """Tests for the List Consumption Cycles endpoint."""

    def test_list_consumption_cycles_success(self, api_client: DevinAPIClient) -> None:
        """Test listing consumption cycles returns successful response."""
        response = api_client.get("/enterprise/consumption/cycles")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "cycles" in data or isinstance(data, list)

    def test_list_consumption_cycles_with_limit(self, api_client: DevinAPIClient) -> None:
        """Test listing consumption cycles with limit parameter."""
        response = api_client.get("/enterprise/consumption/cycles", params={"limit": 5})
        assert response.status_code == 200

    def test_list_consumption_cycles_response_structure(self, api_client: DevinAPIClient) -> None:
        """Test that consumption cycles response has expected structure."""
        response = api_client.get("/enterprise/consumption/cycles")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))


class TestGetDailyConsumption:
    """Tests for the Get Daily Consumption endpoint."""

    def test_get_daily_consumption_success(self, api_client: DevinAPIClient) -> None:
        """Test getting daily consumption returns successful response."""
        response = api_client.get("/enterprise/consumption/daily")
        assert response.status_code == 200

    def test_get_daily_consumption_with_date_range(self, api_client: DevinAPIClient) -> None:
        """Test getting daily consumption with date range parameters."""
        response = api_client.get(
            "/enterprise/consumption/daily",
            params={"start_date": "2024-01-01", "end_date": "2024-12-31"},
        )
        assert response.status_code in [200, 422]

    def test_get_daily_consumption_response_structure(self, api_client: DevinAPIClient) -> None:
        """Test that daily consumption response has expected structure."""
        response = api_client.get("/enterprise/consumption/daily")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))


class TestGetOrganizationDailyConsumption:
    """Tests for the Get Organization Daily Consumption endpoint."""

    def test_get_org_daily_consumption_success(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test getting organization daily consumption returns successful response."""
        response = api_client.get(f"/organizations/{org_id}/consumption/daily")
        assert response.status_code == 200

    def test_get_org_daily_consumption_with_date_range(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test getting organization daily consumption with date range parameters."""
        response = api_client.get(
            f"/organizations/{org_id}/consumption/daily",
            params={"start_date": "2024-01-01", "end_date": "2024-12-31"},
        )
        assert response.status_code in [200, 422]

    def test_get_org_daily_consumption_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test getting daily consumption with invalid organization ID."""
        response = api_client.get("/organizations/invalid-org-id/consumption/daily")
        assert response.status_code in [400, 404, 422]

    def test_get_org_daily_consumption_response_structure(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test that organization daily consumption response has expected structure."""
        response = api_client.get(f"/organizations/{org_id}/consumption/daily")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))


class TestGetUserDailyConsumption:
    """Tests for the Get User Daily Consumption endpoint."""

    def test_get_user_daily_consumption_success(
        self, api_client: DevinAPIClient, user_id: str
    ) -> None:
        """Test getting user daily consumption returns successful response."""
        response = api_client.get(f"/enterprise/users/{user_id}/consumption/daily")
        assert response.status_code == 200

    def test_get_user_daily_consumption_with_date_range(
        self, api_client: DevinAPIClient, user_id: str
    ) -> None:
        """Test getting user daily consumption with date range parameters."""
        response = api_client.get(
            f"/enterprise/users/{user_id}/consumption/daily",
            params={"start_date": "2024-01-01", "end_date": "2024-12-31"},
        )
        assert response.status_code in [200, 422]

    def test_get_user_daily_consumption_invalid_user_id(self, api_client: DevinAPIClient) -> None:
        """Test getting daily consumption with invalid user ID."""
        response = api_client.get("/enterprise/users/invalid-user-id/consumption/daily")
        assert response.status_code in [400, 404, 422]

    def test_get_user_daily_consumption_response_structure(
        self, api_client: DevinAPIClient, user_id: str
    ) -> None:
        """Test that user daily consumption response has expected structure."""
        response = api_client.get(f"/enterprise/users/{user_id}/consumption/daily")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))


class TestGetSessionDailyConsumption:
    """Tests for the Get Session Daily Consumption endpoint."""

    def test_get_session_daily_consumption_success(
        self, api_client: DevinAPIClient, session_id: str
    ) -> None:
        """Test getting session daily consumption returns successful response."""
        response = api_client.get(f"/sessions/{session_id}/consumption/daily")
        assert response.status_code == 200

    def test_get_session_daily_consumption_invalid_session_id(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test getting daily consumption with invalid session ID."""
        response = api_client.get("/sessions/invalid-session-id/consumption/daily")
        assert response.status_code in [400, 404, 422]

    def test_get_session_daily_consumption_response_structure(
        self, api_client: DevinAPIClient, session_id: str
    ) -> None:
        """Test that session daily consumption response has expected structure."""
        response = api_client.get(f"/sessions/{session_id}/consumption/daily")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))

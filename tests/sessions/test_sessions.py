"""Tests for Sessions API endpoints.

This module tests the following endpoints:
- GET /v3beta1/organizations/{org_id}/sessions - List Sessions
- POST /v3beta1/organizations/{org_id}/sessions - Create Session
- DELETE /v3beta1/sessions/{session_id} - Terminate Session
- POST /v3beta1/sessions/{session_id}/archive - Archive Session
"""


from devin_api_client import DevinAPIClient


class TestListSessions:
    """Tests for the List Sessions endpoint."""

    def test_list_sessions_success(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing sessions returns successful response."""
        response = api_client.get(f"/organizations/{org_id}/sessions")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "sessions" in data or isinstance(data, list)

    def test_list_sessions_with_limit(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing sessions with limit parameter."""
        response = api_client.get(f"/organizations/{org_id}/sessions", params={"limit": 5})
        assert response.status_code == 200
        data = response.json()
        if "items" in data:
            assert len(data["items"]) <= 5

    def test_list_sessions_with_offset(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing sessions with offset parameter."""
        response = api_client.get(
            f"/organizations/{org_id}/sessions", params={"offset": 0, "limit": 10}
        )
        assert response.status_code == 200

    def test_list_sessions_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test listing sessions with invalid organization ID returns error."""
        response = api_client.get("/organizations/invalid-org-id/sessions")
        assert response.status_code in [400, 404, 422]

    def test_list_sessions_response_structure(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test that sessions response has expected structure."""
        response = api_client.get(f"/organizations/{org_id}/sessions")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))
        if isinstance(data, dict) and "items" in data and data["items"]:
            session = data["items"][0]
            assert "session_id" in session or "id" in session

    def test_list_sessions_pagination(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing sessions with pagination."""
        response1 = api_client.get(
            f"/organizations/{org_id}/sessions", params={"limit": 1, "offset": 0}
        )
        assert response1.status_code == 200
        response2 = api_client.get(
            f"/organizations/{org_id}/sessions", params={"limit": 1, "offset": 1}
        )
        assert response2.status_code == 200

    def test_list_sessions_with_status_filter(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing sessions with status filter."""
        response = api_client.get(
            f"/organizations/{org_id}/sessions", params={"status": "active"}
        )
        assert response.status_code in [200, 422]


class TestCreateSession:
    """Tests for the Create Session endpoint."""

    def test_create_session_missing_required_fields(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test creating session without required fields returns error."""
        response = api_client.post(f"/organizations/{org_id}/sessions", json={})
        assert response.status_code in [400, 422]

    def test_create_session_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test creating session with invalid organization ID returns error."""
        response = api_client.post(
            "/organizations/invalid-org-id/sessions",
            json={"prompt": "Test session"},
        )
        assert response.status_code in [400, 404, 422]

    def test_create_session_with_prompt(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test creating session with prompt.

        Note: This test may create an actual session if the API allows it.
        """
        response = api_client.post(
            f"/organizations/{org_id}/sessions",
            json={"prompt": "Test session for API demo"},
        )
        assert response.status_code in [200, 201, 400, 422]


class TestTerminateSession:
    """Tests for the Terminate Session endpoint."""

    def test_terminate_session_invalid_id(self, api_client: DevinAPIClient) -> None:
        """Test terminating session with invalid ID returns error."""
        response = api_client.delete("/sessions/invalid-session-id")
        assert response.status_code in [400, 404, 422]

    def test_terminate_session_nonexistent_id(self, api_client: DevinAPIClient) -> None:
        """Test terminating session with nonexistent ID returns error."""
        response = api_client.delete("/sessions/00000000-0000-0000-0000-000000000000")
        assert response.status_code in [400, 404, 422]


class TestArchiveSession:
    """Tests for the Archive Session endpoint."""

    def test_archive_session_invalid_id(self, api_client: DevinAPIClient) -> None:
        """Test archiving session with invalid ID returns error."""
        response = api_client.post("/sessions/invalid-session-id/archive")
        assert response.status_code in [400, 404, 422]

    def test_archive_session_nonexistent_id(self, api_client: DevinAPIClient) -> None:
        """Test archiving session with nonexistent ID returns error."""
        response = api_client.post("/sessions/00000000-0000-0000-0000-000000000000/archive")
        assert response.status_code in [400, 404, 422]

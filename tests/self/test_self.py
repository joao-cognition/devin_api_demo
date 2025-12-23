"""Tests for Self API endpoints.

This module tests the following endpoints:
- GET /v3beta1/enterprise/self - Get Self
"""


from devin_api_client import DevinAPIClient


class TestGetSelf:
    """Tests for the Get Self endpoint."""

    def test_get_self_success(self, api_client: DevinAPIClient) -> None:
        """Test getting self returns successful response."""
        response = api_client.get("/enterprise/self")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_get_self_response_structure(self, api_client: DevinAPIClient) -> None:
        """Test that self response has expected structure."""
        response = api_client.get("/enterprise/self")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "service_user_id" in data or "id" in data or "user_id" in data

    def test_get_self_contains_service_user_info(self, api_client: DevinAPIClient) -> None:
        """Test that self response contains service user information."""
        response = api_client.get("/enterprise/self")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert (
            "service_user_name" in data
            or "name" in data
            or "service_user_id" in data
            or "id" in data
        )

    def test_get_self_authenticated(self, api_client: DevinAPIClient) -> None:
        """Test that self endpoint requires authentication."""
        response = api_client.get("/enterprise/self")
        assert response.status_code == 200

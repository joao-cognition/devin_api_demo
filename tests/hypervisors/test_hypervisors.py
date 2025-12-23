"""Tests for Hypervisors API endpoints.

This module tests the following endpoints:
- GET /v3beta1/enterprise/hypervisors - List Hypervisors
"""


from devin_api_client import DevinAPIClient


class TestListHypervisors:
    """Tests for the List Hypervisors endpoint."""

    def test_list_hypervisors_success(self, api_client: DevinAPIClient) -> None:
        """Test listing hypervisors returns successful response."""
        response = api_client.get("/enterprise/hypervisors")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "hypervisors" in data or isinstance(data, list)

    def test_list_hypervisors_with_limit(self, api_client: DevinAPIClient) -> None:
        """Test listing hypervisors with limit parameter."""
        response = api_client.get("/enterprise/hypervisors", params={"limit": 5})
        assert response.status_code == 200

    def test_list_hypervisors_with_offset(self, api_client: DevinAPIClient) -> None:
        """Test listing hypervisors with offset parameter."""
        response = api_client.get("/enterprise/hypervisors", params={"offset": 0, "limit": 10})
        assert response.status_code == 200

    def test_list_hypervisors_response_structure(self, api_client: DevinAPIClient) -> None:
        """Test that hypervisors response has expected structure."""
        response = api_client.get("/enterprise/hypervisors")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))

    def test_list_hypervisors_pagination(self, api_client: DevinAPIClient) -> None:
        """Test listing hypervisors with pagination."""
        response1 = api_client.get("/enterprise/hypervisors", params={"limit": 1, "offset": 0})
        assert response1.status_code == 200
        response2 = api_client.get("/enterprise/hypervisors", params={"limit": 1, "offset": 1})
        assert response2.status_code == 200

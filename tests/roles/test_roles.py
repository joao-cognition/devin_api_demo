"""Tests for Roles API endpoints.

This module tests the following endpoints:
- GET /v3beta1/enterprise/roles - List Roles
"""


from devin_api_client import DevinAPIClient


class TestListRoles:
    """Tests for the List Roles endpoint."""

    def test_list_roles_success(self, api_client: DevinAPIClient) -> None:
        """Test listing roles returns successful response."""
        response = api_client.get("/enterprise/roles")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "roles" in data or isinstance(data, list)

    def test_list_roles_with_limit(self, api_client: DevinAPIClient) -> None:
        """Test listing roles with limit parameter."""
        response = api_client.get("/enterprise/roles", params={"limit": 5})
        assert response.status_code == 200

    def test_list_roles_with_offset(self, api_client: DevinAPIClient) -> None:
        """Test listing roles with offset parameter."""
        response = api_client.get("/enterprise/roles", params={"offset": 0, "limit": 10})
        assert response.status_code == 200

    def test_list_roles_response_structure(self, api_client: DevinAPIClient) -> None:
        """Test that roles response has expected structure."""
        response = api_client.get("/enterprise/roles")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))

    def test_list_roles_pagination(self, api_client: DevinAPIClient) -> None:
        """Test listing roles with pagination."""
        response1 = api_client.get("/enterprise/roles", params={"limit": 1, "offset": 0})
        assert response1.status_code == 200
        response2 = api_client.get("/enterprise/roles", params={"limit": 1, "offset": 1})
        assert response2.status_code == 200

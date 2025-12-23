"""Tests for Git Connections API endpoints.

This module tests the following endpoints:
- GET /v3beta1/enterprise/git-connections - List Git Connections
"""


from devin_api_client import DevinAPIClient


class TestListGitConnections:
    """Tests for the List Git Connections endpoint."""

    def test_list_git_connections_success(self, api_client: DevinAPIClient) -> None:
        """Test listing git connections returns successful response."""
        response = api_client.get("/enterprise/git-connections")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "connections" in data or isinstance(data, list)

    def test_list_git_connections_with_limit(self, api_client: DevinAPIClient) -> None:
        """Test listing git connections with limit parameter."""
        response = api_client.get("/enterprise/git-connections", params={"limit": 5})
        assert response.status_code == 200

    def test_list_git_connections_with_offset(self, api_client: DevinAPIClient) -> None:
        """Test listing git connections with offset parameter."""
        response = api_client.get("/enterprise/git-connections", params={"offset": 0, "limit": 10})
        assert response.status_code == 200

    def test_list_git_connections_response_structure(self, api_client: DevinAPIClient) -> None:
        """Test that git connections response has expected structure."""
        response = api_client.get("/enterprise/git-connections")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))
        if isinstance(data, dict) and "items" in data and data["items"]:
            connection = data["items"][0]
            assert isinstance(connection, dict)

    def test_list_git_connections_pagination(self, api_client: DevinAPIClient) -> None:
        """Test listing git connections with pagination."""
        response1 = api_client.get("/enterprise/git-connections", params={"limit": 1, "offset": 0})
        assert response1.status_code == 200
        response2 = api_client.get("/enterprise/git-connections", params={"limit": 1, "offset": 1})
        assert response2.status_code == 200

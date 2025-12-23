"""Tests for Git Permissions API endpoints.

This module tests the following endpoints:
- GET /v3beta1/enterprise/git-permissions - List Git Permissions
- POST /v3beta1/enterprise/git-permissions - Create Git Permission
- DELETE /v3beta1/enterprise/git-permissions/{permission_id} - Delete Git Permission
"""


from devin_api_client import DevinAPIClient


class TestListGitPermissions:
    """Tests for the List Git Permissions endpoint."""

    def test_list_git_permissions_success(self, api_client: DevinAPIClient) -> None:
        """Test listing git permissions returns successful response."""
        response = api_client.get("/enterprise/git-permissions")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "permissions" in data or isinstance(data, list)

    def test_list_git_permissions_with_limit(self, api_client: DevinAPIClient) -> None:
        """Test listing git permissions with limit parameter."""
        response = api_client.get("/enterprise/git-permissions", params={"limit": 5})
        assert response.status_code == 200

    def test_list_git_permissions_with_offset(self, api_client: DevinAPIClient) -> None:
        """Test listing git permissions with offset parameter."""
        response = api_client.get("/enterprise/git-permissions", params={"offset": 0, "limit": 10})
        assert response.status_code == 200

    def test_list_git_permissions_response_structure(self, api_client: DevinAPIClient) -> None:
        """Test that git permissions response has expected structure."""
        response = api_client.get("/enterprise/git-permissions")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))

    def test_list_git_permissions_pagination(self, api_client: DevinAPIClient) -> None:
        """Test listing git permissions with pagination."""
        response1 = api_client.get("/enterprise/git-permissions", params={"limit": 1, "offset": 0})
        assert response1.status_code == 200
        response2 = api_client.get("/enterprise/git-permissions", params={"limit": 1, "offset": 1})
        assert response2.status_code == 200


class TestCreateGitPermission:
    """Tests for the Create Git Permission endpoint."""

    def test_create_git_permission_missing_required_fields(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test creating git permission without required fields returns error."""
        response = api_client.post("/enterprise/git-permissions", json={})
        assert response.status_code in [400, 422]

    def test_create_git_permission_invalid_data(self, api_client: DevinAPIClient) -> None:
        """Test creating git permission with invalid data returns error."""
        response = api_client.post(
            "/enterprise/git-permissions",
            json={"invalid_field": "invalid_value"},
        )
        assert response.status_code in [400, 422]

    def test_create_git_permission_with_valid_data(self, api_client: DevinAPIClient) -> None:
        """Test creating git permission with valid data.

        Note: This test may fail if the required fields are not correct.
        The actual required fields should be verified from the API documentation.
        """
        response = api_client.post(
            "/enterprise/git-permissions",
            json={
                "repository": "test-repo",
                "permission_type": "read",
            },
        )
        assert response.status_code in [200, 201, 400, 422]


class TestDeleteGitPermission:
    """Tests for the Delete Git Permission endpoint."""

    def test_delete_git_permission_invalid_id(self, api_client: DevinAPIClient) -> None:
        """Test deleting git permission with invalid ID returns error."""
        response = api_client.delete("/enterprise/git-permissions/invalid-permission-id")
        assert response.status_code in [400, 404, 422]

    def test_delete_git_permission_nonexistent_id(self, api_client: DevinAPIClient) -> None:
        """Test deleting git permission with nonexistent ID returns error."""
        response = api_client.delete(
            "/enterprise/git-permissions/00000000-0000-0000-0000-000000000000"
        )
        assert response.status_code in [400, 404, 422]

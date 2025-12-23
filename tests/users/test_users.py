"""Tests for Users API endpoints.

This module tests the following endpoints:
Enterprise Users:
- GET /v3beta1/enterprise/users - List Enterprise Users
- POST /v3beta1/enterprise/users - Create Enterprise User
- PATCH /v3beta1/enterprise/users/{user_id} - Update Enterprise User
- DELETE /v3beta1/enterprise/users/{user_id} - Delete Enterprise User

Organization Users:
- GET /v3beta1/organizations/{org_id}/users - List Organization Users
- POST /v3beta1/organizations/{org_id}/users - Create Organization User
- PATCH /v3beta1/organizations/{org_id}/users/{user_id} - Update Organization User
- DELETE /v3beta1/organizations/{org_id}/users/{user_id} - Delete Organization User
"""


from devin_api_client import DevinAPIClient


class TestListEnterpriseUsers:
    """Tests for the List Enterprise Users endpoint."""

    def test_list_enterprise_users_success(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise users returns successful response."""
        response = api_client.get("/enterprise/users")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "users" in data or isinstance(data, list)

    def test_list_enterprise_users_with_limit(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise users with limit parameter."""
        response = api_client.get("/enterprise/users", params={"limit": 5})
        assert response.status_code == 200
        data = response.json()
        if "items" in data:
            assert len(data["items"]) <= 5

    def test_list_enterprise_users_with_offset(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise users with offset parameter."""
        response = api_client.get("/enterprise/users", params={"offset": 0, "limit": 10})
        assert response.status_code == 200

    def test_list_enterprise_users_response_structure(self, api_client: DevinAPIClient) -> None:
        """Test that enterprise users response has expected structure."""
        response = api_client.get("/enterprise/users")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))
        if isinstance(data, dict) and "items" in data and data["items"]:
            user = data["items"][0]
            assert "user_id" in user or "id" in user or "email" in user

    def test_list_enterprise_users_pagination(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise users with pagination."""
        response1 = api_client.get("/enterprise/users", params={"limit": 1, "offset": 0})
        assert response1.status_code == 200
        response2 = api_client.get("/enterprise/users", params={"limit": 1, "offset": 1})
        assert response2.status_code == 200


class TestCreateEnterpriseUser:
    """Tests for the Create Enterprise User endpoint."""

    def test_create_enterprise_user_missing_required_fields(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test creating enterprise user without required fields returns error."""
        response = api_client.post("/enterprise/users", json={})
        assert response.status_code in [400, 422]

    def test_create_enterprise_user_invalid_data(self, api_client: DevinAPIClient) -> None:
        """Test creating enterprise user with invalid data returns error."""
        response = api_client.post(
            "/enterprise/users",
            json={"invalid_field": "invalid_value"},
        )
        assert response.status_code in [400, 422]

    def test_create_enterprise_user_invalid_email(self, api_client: DevinAPIClient) -> None:
        """Test creating enterprise user with invalid email returns error."""
        response = api_client.post(
            "/enterprise/users",
            json={"email": "invalid-email"},
        )
        assert response.status_code in [400, 422]


class TestUpdateEnterpriseUser:
    """Tests for the Update Enterprise User endpoint."""

    def test_update_enterprise_user_invalid_id(self, api_client: DevinAPIClient) -> None:
        """Test updating enterprise user with invalid ID returns error."""
        response = api_client.patch(
            "/enterprise/users/invalid-user-id",
            json={"name": "Updated User"},
        )
        assert response.status_code in [400, 404, 422]

    def test_update_enterprise_user_nonexistent_id(self, api_client: DevinAPIClient) -> None:
        """Test updating enterprise user with nonexistent ID returns error."""
        response = api_client.patch(
            "/enterprise/users/00000000-0000-0000-0000-000000000000",
            json={"name": "Updated User"},
        )
        assert response.status_code in [400, 404, 422]

    def test_update_enterprise_user_empty_body(
        self, api_client: DevinAPIClient, user_id: str
    ) -> None:
        """Test updating enterprise user with empty body."""
        response = api_client.patch(f"/enterprise/users/{user_id}", json={})
        assert response.status_code in [200, 400, 422]


class TestDeleteEnterpriseUser:
    """Tests for the Delete Enterprise User endpoint."""

    def test_delete_enterprise_user_invalid_id(self, api_client: DevinAPIClient) -> None:
        """Test deleting enterprise user with invalid ID returns error."""
        response = api_client.delete("/enterprise/users/invalid-user-id")
        assert response.status_code in [400, 404, 422]

    def test_delete_enterprise_user_nonexistent_id(self, api_client: DevinAPIClient) -> None:
        """Test deleting enterprise user with nonexistent ID returns error."""
        response = api_client.delete("/enterprise/users/00000000-0000-0000-0000-000000000000")
        assert response.status_code in [400, 404, 422]


class TestListOrganizationUsers:
    """Tests for the List Organization Users endpoint."""

    def test_list_org_users_success(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing organization users returns successful response."""
        response = api_client.get(f"/organizations/{org_id}/users")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "users" in data or isinstance(data, list)

    def test_list_org_users_with_limit(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing organization users with limit parameter."""
        response = api_client.get(f"/organizations/{org_id}/users", params={"limit": 5})
        assert response.status_code == 200

    def test_list_org_users_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test listing users with invalid organization ID returns error."""
        response = api_client.get("/organizations/invalid-org-id/users")
        assert response.status_code in [400, 404, 422]

    def test_list_org_users_response_structure(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test that organization users response has expected structure."""
        response = api_client.get(f"/organizations/{org_id}/users")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))

    def test_list_org_users_pagination(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing organization users with pagination."""
        response1 = api_client.get(
            f"/organizations/{org_id}/users", params={"limit": 1, "offset": 0}
        )
        assert response1.status_code == 200
        response2 = api_client.get(
            f"/organizations/{org_id}/users", params={"limit": 1, "offset": 1}
        )
        assert response2.status_code == 200


class TestCreateOrganizationUser:
    """Tests for the Create Organization User endpoint."""

    def test_create_org_user_missing_required_fields(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test creating organization user without required fields returns error."""
        response = api_client.post(f"/organizations/{org_id}/users", json={})
        assert response.status_code in [400, 422]

    def test_create_org_user_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test creating user with invalid organization ID returns error."""
        response = api_client.post(
            "/organizations/invalid-org-id/users",
            json={"email": "test@example.com"},
        )
        assert response.status_code in [400, 404, 422]

    def test_create_org_user_invalid_email(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test creating organization user with invalid email returns error."""
        response = api_client.post(
            f"/organizations/{org_id}/users",
            json={"email": "invalid-email"},
        )
        assert response.status_code in [400, 422]


class TestUpdateOrganizationUser:
    """Tests for the Update Organization User endpoint."""

    def test_update_org_user_invalid_id(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test updating organization user with invalid ID returns error."""
        response = api_client.patch(
            f"/organizations/{org_id}/users/invalid-user-id",
            json={"name": "Updated User"},
        )
        assert response.status_code in [400, 404, 422]


class TestDeleteOrganizationUser:
    """Tests for the Delete Organization User endpoint."""

    def test_delete_org_user_invalid_id(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test deleting organization user with invalid ID returns error."""
        response = api_client.delete(f"/organizations/{org_id}/users/invalid-user-id")
        assert response.status_code in [400, 404, 422]

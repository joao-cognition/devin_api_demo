"""Tests for Service Users API endpoints.

This module tests the following endpoints:
Enterprise Service Users:
- GET /v3beta1/enterprise/service-users - List Enterprise Service Users
- POST /v3beta1/enterprise/service-users - Create Enterprise Service User
- PATCH /v3beta1/enterprise/service-users/{service_user_id} - Update Enterprise Service User
- DELETE /v3beta1/enterprise/service-users/{service_user_id} - Delete Enterprise Service User

Organization Service Users:
- GET /v3beta1/organizations/{org_id}/service-users - List Organization Service Users
- POST /v3beta1/organizations/{org_id}/service-users - Create Organization Service User
- PATCH /v3beta1/organizations/{org_id}/service-users/{service_user_id} - Update Org Service User
- DELETE /v3beta1/organizations/{org_id}/service-users/{service_user_id} - Delete Org Service User
"""


from devin_api_client import DevinAPIClient


class TestListEnterpriseServiceUsers:
    """Tests for the List Enterprise Service Users endpoint."""

    def test_list_enterprise_service_users_success(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise service users returns successful response."""
        response = api_client.get("/enterprise/service-users")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "service_users" in data or isinstance(data, list)

    def test_list_enterprise_service_users_with_limit(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise service users with limit parameter."""
        response = api_client.get("/enterprise/service-users", params={"limit": 5})
        assert response.status_code == 200

    def test_list_enterprise_service_users_with_offset(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise service users with offset parameter."""
        response = api_client.get("/enterprise/service-users", params={"offset": 0, "limit": 10})
        assert response.status_code == 200

    def test_list_enterprise_service_users_response_structure(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test that enterprise service users response has expected structure."""
        response = api_client.get("/enterprise/service-users")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))


class TestCreateEnterpriseServiceUser:
    """Tests for the Create Enterprise Service User endpoint."""

    def test_create_enterprise_service_user_missing_required_fields(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test creating enterprise service user without required fields returns error."""
        response = api_client.post("/enterprise/service-users", json={})
        assert response.status_code in [400, 422]

    def test_create_enterprise_service_user_invalid_data(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test creating enterprise service user with invalid data returns error."""
        response = api_client.post(
            "/enterprise/service-users",
            json={"invalid_field": "invalid_value"},
        )
        assert response.status_code in [400, 422]


class TestUpdateEnterpriseServiceUser:
    """Tests for the Update Enterprise Service User endpoint."""

    def test_update_enterprise_service_user_invalid_id(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test updating enterprise service user with invalid ID returns error."""
        response = api_client.patch(
            "/enterprise/service-users/invalid-service-user-id",
            json={"name": "Updated Service User"},
        )
        assert response.status_code in [400, 404, 422]

    def test_update_enterprise_service_user_nonexistent_id(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test updating enterprise service user with nonexistent ID returns error."""
        response = api_client.patch(
            "/enterprise/service-users/00000000-0000-0000-0000-000000000000",
            json={"name": "Updated Service User"},
        )
        assert response.status_code in [400, 404, 422]


class TestDeleteEnterpriseServiceUser:
    """Tests for the Delete Enterprise Service User endpoint."""

    def test_delete_enterprise_service_user_invalid_id(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test deleting enterprise service user with invalid ID returns error."""
        response = api_client.delete("/enterprise/service-users/invalid-service-user-id")
        assert response.status_code in [400, 404, 422]

    def test_delete_enterprise_service_user_nonexistent_id(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test deleting enterprise service user with nonexistent ID returns error."""
        response = api_client.delete(
            "/enterprise/service-users/00000000-0000-0000-0000-000000000000"
        )
        assert response.status_code in [400, 404, 422]


class TestListOrganizationServiceUsers:
    """Tests for the List Organization Service Users endpoint."""

    def test_list_org_service_users_success(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing organization service users returns successful response."""
        response = api_client.get(f"/organizations/{org_id}/service-users")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "service_users" in data or isinstance(data, list)

    def test_list_org_service_users_with_limit(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing organization service users with limit parameter."""
        response = api_client.get(f"/organizations/{org_id}/service-users", params={"limit": 5})
        assert response.status_code == 200

    def test_list_org_service_users_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test listing service users with invalid organization ID returns error."""
        response = api_client.get("/organizations/invalid-org-id/service-users")
        assert response.status_code in [400, 404, 422]

    def test_list_org_service_users_response_structure(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test that organization service users response has expected structure."""
        response = api_client.get(f"/organizations/{org_id}/service-users")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))


class TestCreateOrganizationServiceUser:
    """Tests for the Create Organization Service User endpoint."""

    def test_create_org_service_user_missing_required_fields(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test creating organization service user without required fields returns error."""
        response = api_client.post(f"/organizations/{org_id}/service-users", json={})
        assert response.status_code in [400, 422]

    def test_create_org_service_user_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test creating service user with invalid organization ID returns error."""
        response = api_client.post(
            "/organizations/invalid-org-id/service-users",
            json={"name": "Test Service User"},
        )
        assert response.status_code in [400, 404, 422]


class TestUpdateOrganizationServiceUser:
    """Tests for the Update Organization Service User endpoint."""

    def test_update_org_service_user_invalid_id(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test updating organization service user with invalid ID returns error."""
        response = api_client.patch(
            f"/organizations/{org_id}/service-users/invalid-service-user-id",
            json={"name": "Updated Service User"},
        )
        assert response.status_code in [400, 404, 422]


class TestDeleteOrganizationServiceUser:
    """Tests for the Delete Organization Service User endpoint."""

    def test_delete_org_service_user_invalid_id(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test deleting organization service user with invalid ID returns error."""
        response = api_client.delete(
            f"/organizations/{org_id}/service-users/invalid-service-user-id"
        )
        assert response.status_code in [400, 404, 422]

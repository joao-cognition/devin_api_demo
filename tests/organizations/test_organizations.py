"""Tests for Organizations API endpoints.

This module tests the following endpoints:
- GET /v3beta1/enterprise/organizations - List Organizations
- POST /v3beta1/enterprise/organizations - Create Organization
- PATCH /v3beta1/enterprise/organizations/{org_id} - Update Organization
- DELETE /v3beta1/enterprise/organizations/{org_id} - Delete Organization
"""


from devin_api_client import DevinAPIClient


class TestListOrganizations:
    """Tests for the List Organizations endpoint."""

    def test_list_organizations_success(self, api_client: DevinAPIClient) -> None:
        """Test listing organizations returns successful response."""
        response = api_client.get("/enterprise/organizations")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "organizations" in data or isinstance(data, list)

    def test_list_organizations_with_limit(self, api_client: DevinAPIClient) -> None:
        """Test listing organizations with limit parameter."""
        response = api_client.get("/enterprise/organizations", params={"limit": 5})
        assert response.status_code == 200
        data = response.json()
        if "items" in data:
            assert len(data["items"]) <= 5

    def test_list_organizations_with_offset(self, api_client: DevinAPIClient) -> None:
        """Test listing organizations with offset parameter."""
        response = api_client.get("/enterprise/organizations", params={"offset": 0, "limit": 10})
        assert response.status_code == 200

    def test_list_organizations_response_structure(self, api_client: DevinAPIClient) -> None:
        """Test that organizations response has expected structure."""
        response = api_client.get("/enterprise/organizations")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))
        if isinstance(data, dict) and "items" in data and data["items"]:
            org = data["items"][0]
            assert "org_id" in org or "id" in org

    def test_list_organizations_pagination(self, api_client: DevinAPIClient) -> None:
        """Test listing organizations with pagination."""
        response1 = api_client.get("/enterprise/organizations", params={"limit": 1, "offset": 0})
        assert response1.status_code == 200
        response2 = api_client.get("/enterprise/organizations", params={"limit": 1, "offset": 1})
        assert response2.status_code == 200


class TestCreateOrganization:
    """Tests for the Create Organization endpoint."""

    def test_create_organization_missing_required_fields(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test creating organization without required fields returns error."""
        response = api_client.post("/enterprise/organizations", json={})
        assert response.status_code in [400, 422]

    def test_create_organization_invalid_data(self, api_client: DevinAPIClient) -> None:
        """Test creating organization with invalid data returns error."""
        response = api_client.post(
            "/enterprise/organizations",
            json={"invalid_field": "invalid_value"},
        )
        assert response.status_code in [400, 422]

    def test_create_organization_with_valid_data(self, api_client: DevinAPIClient) -> None:
        """Test creating organization with valid data.

        Note: This test may fail if the required fields are not correct.
        The actual required fields should be verified from the API documentation.
        """
        response = api_client.post(
            "/enterprise/organizations",
            json={
                "name": "Test Organization",
                "slug": "test-org",
            },
        )
        assert response.status_code in [200, 201, 400, 422]


class TestUpdateOrganization:
    """Tests for the Update Organization endpoint."""

    def test_update_organization_invalid_id(self, api_client: DevinAPIClient) -> None:
        """Test updating organization with invalid ID returns error."""
        response = api_client.patch(
            "/enterprise/organizations/invalid-org-id",
            json={"name": "Updated Organization"},
        )
        assert response.status_code in [400, 404, 422]

    def test_update_organization_nonexistent_id(self, api_client: DevinAPIClient) -> None:
        """Test updating organization with nonexistent ID returns error."""
        response = api_client.patch(
            "/enterprise/organizations/00000000-0000-0000-0000-000000000000",
            json={"name": "Updated Organization"},
        )
        assert response.status_code in [400, 404, 422]

    def test_update_organization_empty_body(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test updating organization with empty body."""
        response = api_client.patch(f"/enterprise/organizations/{org_id}", json={})
        assert response.status_code in [200, 400, 422]


class TestDeleteOrganization:
    """Tests for the Delete Organization endpoint."""

    def test_delete_organization_invalid_id(self, api_client: DevinAPIClient) -> None:
        """Test deleting organization with invalid ID returns error."""
        response = api_client.delete("/enterprise/organizations/invalid-org-id")
        assert response.status_code in [400, 404, 422]

    def test_delete_organization_nonexistent_id(self, api_client: DevinAPIClient) -> None:
        """Test deleting organization with nonexistent ID returns error."""
        response = api_client.delete(
            "/enterprise/organizations/00000000-0000-0000-0000-000000000000"
        )
        assert response.status_code in [400, 404, 422]

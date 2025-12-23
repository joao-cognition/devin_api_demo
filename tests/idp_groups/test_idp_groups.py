"""Tests for IDP Groups API endpoints.

This module tests the following endpoints:
Enterprise IDP Groups:
- GET /v3beta1/enterprise/idp-groups - List Enterprise IDP Groups
- POST /v3beta1/enterprise/idp-groups - Create Enterprise IDP Group
- PATCH /v3beta1/enterprise/idp-groups/{group_id} - Update Enterprise IDP Group
- DELETE /v3beta1/enterprise/idp-groups/{group_id} - Delete Enterprise IDP Group

Organization IDP Groups:
- GET /v3beta1/organizations/{org_id}/idp-groups - List Organization IDP Groups
- POST /v3beta1/organizations/{org_id}/idp-groups - Create Organization IDP Group
- PATCH /v3beta1/organizations/{org_id}/idp-groups/{group_id} - Update Organization IDP Group
- DELETE /v3beta1/organizations/{org_id}/idp-groups/{group_id} - Delete Organization IDP Group
"""


from devin_api_client import DevinAPIClient


class TestListEnterpriseIDPGroups:
    """Tests for the List Enterprise IDP Groups endpoint."""

    def test_list_enterprise_idp_groups_success(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise IDP groups returns successful response."""
        response = api_client.get("/enterprise/idp-groups")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "groups" in data or isinstance(data, list)

    def test_list_enterprise_idp_groups_with_limit(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise IDP groups with limit parameter."""
        response = api_client.get("/enterprise/idp-groups", params={"limit": 5})
        assert response.status_code == 200

    def test_list_enterprise_idp_groups_with_offset(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise IDP groups with offset parameter."""
        response = api_client.get("/enterprise/idp-groups", params={"offset": 0, "limit": 10})
        assert response.status_code == 200

    def test_list_enterprise_idp_groups_response_structure(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test that enterprise IDP groups response has expected structure."""
        response = api_client.get("/enterprise/idp-groups")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))


class TestCreateEnterpriseIDPGroup:
    """Tests for the Create Enterprise IDP Group endpoint."""

    def test_create_enterprise_idp_group_missing_required_fields(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test creating enterprise IDP group without required fields returns error."""
        response = api_client.post("/enterprise/idp-groups", json={})
        assert response.status_code in [400, 422]

    def test_create_enterprise_idp_group_invalid_data(self, api_client: DevinAPIClient) -> None:
        """Test creating enterprise IDP group with invalid data returns error."""
        response = api_client.post(
            "/enterprise/idp-groups",
            json={"invalid_field": "invalid_value"},
        )
        assert response.status_code in [400, 422]


class TestUpdateEnterpriseIDPGroup:
    """Tests for the Update Enterprise IDP Group endpoint."""

    def test_update_enterprise_idp_group_invalid_id(self, api_client: DevinAPIClient) -> None:
        """Test updating enterprise IDP group with invalid ID returns error."""
        response = api_client.patch(
            "/enterprise/idp-groups/invalid-group-id",
            json={"name": "Updated Group"},
        )
        assert response.status_code in [400, 404, 422]

    def test_update_enterprise_idp_group_nonexistent_id(self, api_client: DevinAPIClient) -> None:
        """Test updating enterprise IDP group with nonexistent ID returns error."""
        response = api_client.patch(
            "/enterprise/idp-groups/00000000-0000-0000-0000-000000000000",
            json={"name": "Updated Group"},
        )
        assert response.status_code in [400, 404, 422]


class TestDeleteEnterpriseIDPGroup:
    """Tests for the Delete Enterprise IDP Group endpoint."""

    def test_delete_enterprise_idp_group_invalid_id(self, api_client: DevinAPIClient) -> None:
        """Test deleting enterprise IDP group with invalid ID returns error."""
        response = api_client.delete("/enterprise/idp-groups/invalid-group-id")
        assert response.status_code in [400, 404, 422]

    def test_delete_enterprise_idp_group_nonexistent_id(self, api_client: DevinAPIClient) -> None:
        """Test deleting enterprise IDP group with nonexistent ID returns error."""
        response = api_client.delete("/enterprise/idp-groups/00000000-0000-0000-0000-000000000000")
        assert response.status_code in [400, 404, 422]


class TestListOrganizationIDPGroups:
    """Tests for the List Organization IDP Groups endpoint."""

    def test_list_org_idp_groups_success(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing organization IDP groups returns successful response."""
        response = api_client.get(f"/organizations/{org_id}/idp-groups")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "groups" in data or isinstance(data, list)

    def test_list_org_idp_groups_with_limit(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing organization IDP groups with limit parameter."""
        response = api_client.get(f"/organizations/{org_id}/idp-groups", params={"limit": 5})
        assert response.status_code == 200

    def test_list_org_idp_groups_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test listing IDP groups with invalid organization ID returns error."""
        response = api_client.get("/organizations/invalid-org-id/idp-groups")
        assert response.status_code in [400, 404, 422]

    def test_list_org_idp_groups_response_structure(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test that organization IDP groups response has expected structure."""
        response = api_client.get(f"/organizations/{org_id}/idp-groups")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))


class TestCreateOrganizationIDPGroup:
    """Tests for the Create Organization IDP Group endpoint."""

    def test_create_org_idp_group_missing_required_fields(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test creating organization IDP group without required fields returns error."""
        response = api_client.post(f"/organizations/{org_id}/idp-groups", json={})
        assert response.status_code in [400, 422]

    def test_create_org_idp_group_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test creating IDP group with invalid organization ID returns error."""
        response = api_client.post(
            "/organizations/invalid-org-id/idp-groups",
            json={"name": "Test Group"},
        )
        assert response.status_code in [400, 404, 422]


class TestUpdateOrganizationIDPGroup:
    """Tests for the Update Organization IDP Group endpoint."""

    def test_update_org_idp_group_invalid_id(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test updating organization IDP group with invalid ID returns error."""
        response = api_client.patch(
            f"/organizations/{org_id}/idp-groups/invalid-group-id",
            json={"name": "Updated Group"},
        )
        assert response.status_code in [400, 404, 422]


class TestDeleteOrganizationIDPGroup:
    """Tests for the Delete Organization IDP Group endpoint."""

    def test_delete_org_idp_group_invalid_id(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test deleting organization IDP group with invalid ID returns error."""
        response = api_client.delete(f"/organizations/{org_id}/idp-groups/invalid-group-id")
        assert response.status_code in [400, 404, 422]

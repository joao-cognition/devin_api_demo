"""Tests for Playbooks API endpoints.

This module tests the following endpoints:
Enterprise Playbooks:
- GET /v3beta1/enterprise/playbooks - List Enterprise Playbooks
- POST /v3beta1/enterprise/playbooks - Create Enterprise Playbook
- PATCH /v3beta1/enterprise/playbooks/{playbook_id} - Update Enterprise Playbook
- DELETE /v3beta1/enterprise/playbooks/{playbook_id} - Delete Enterprise Playbook

Organization Playbooks:
- GET /v3beta1/organizations/{org_id}/playbooks - List Organization Playbooks
- POST /v3beta1/organizations/{org_id}/playbooks - Create Organization Playbook
- PATCH /v3beta1/organizations/{org_id}/playbooks/{playbook_id} - Update Organization Playbook
- DELETE /v3beta1/organizations/{org_id}/playbooks/{playbook_id} - Delete Organization Playbook
"""


from devin_api_client import DevinAPIClient


class TestListEnterprisePlaybooks:
    """Tests for the List Enterprise Playbooks endpoint."""

    def test_list_enterprise_playbooks_success(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise playbooks returns successful response."""
        response = api_client.get("/enterprise/playbooks")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "playbooks" in data or isinstance(data, list)

    def test_list_enterprise_playbooks_with_limit(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise playbooks with limit parameter."""
        response = api_client.get("/enterprise/playbooks", params={"limit": 5})
        assert response.status_code == 200

    def test_list_enterprise_playbooks_with_offset(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise playbooks with offset parameter."""
        response = api_client.get("/enterprise/playbooks", params={"offset": 0, "limit": 10})
        assert response.status_code == 200

    def test_list_enterprise_playbooks_response_structure(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test that enterprise playbooks response has expected structure."""
        response = api_client.get("/enterprise/playbooks")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))


class TestCreateEnterprisePlaybook:
    """Tests for the Create Enterprise Playbook endpoint."""

    def test_create_enterprise_playbook_missing_required_fields(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test creating enterprise playbook without required fields returns error."""
        response = api_client.post("/enterprise/playbooks", json={})
        assert response.status_code in [400, 422]

    def test_create_enterprise_playbook_invalid_data(self, api_client: DevinAPIClient) -> None:
        """Test creating enterprise playbook with invalid data returns error."""
        response = api_client.post(
            "/enterprise/playbooks",
            json={"invalid_field": "invalid_value"},
        )
        assert response.status_code in [400, 422]


class TestUpdateEnterprisePlaybook:
    """Tests for the Update Enterprise Playbook endpoint."""

    def test_update_enterprise_playbook_invalid_id(self, api_client: DevinAPIClient) -> None:
        """Test updating enterprise playbook with invalid ID returns error."""
        response = api_client.patch(
            "/enterprise/playbooks/invalid-playbook-id",
            json={"name": "Updated Playbook"},
        )
        assert response.status_code in [400, 404, 422]

    def test_update_enterprise_playbook_nonexistent_id(self, api_client: DevinAPIClient) -> None:
        """Test updating enterprise playbook with nonexistent ID returns error."""
        response = api_client.patch(
            "/enterprise/playbooks/00000000-0000-0000-0000-000000000000",
            json={"name": "Updated Playbook"},
        )
        assert response.status_code in [400, 404, 422]


class TestDeleteEnterprisePlaybook:
    """Tests for the Delete Enterprise Playbook endpoint."""

    def test_delete_enterprise_playbook_invalid_id(self, api_client: DevinAPIClient) -> None:
        """Test deleting enterprise playbook with invalid ID returns error."""
        response = api_client.delete("/enterprise/playbooks/invalid-playbook-id")
        assert response.status_code in [400, 404, 422]

    def test_delete_enterprise_playbook_nonexistent_id(self, api_client: DevinAPIClient) -> None:
        """Test deleting enterprise playbook with nonexistent ID returns error."""
        response = api_client.delete(
            "/enterprise/playbooks/00000000-0000-0000-0000-000000000000"
        )
        assert response.status_code in [400, 404, 422]


class TestListOrganizationPlaybooks:
    """Tests for the List Organization Playbooks endpoint."""

    def test_list_org_playbooks_success(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing organization playbooks returns successful response."""
        response = api_client.get(f"/organizations/{org_id}/playbooks")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "playbooks" in data or isinstance(data, list)

    def test_list_org_playbooks_with_limit(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing organization playbooks with limit parameter."""
        response = api_client.get(f"/organizations/{org_id}/playbooks", params={"limit": 5})
        assert response.status_code == 200

    def test_list_org_playbooks_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test listing playbooks with invalid organization ID returns error."""
        response = api_client.get("/organizations/invalid-org-id/playbooks")
        assert response.status_code in [400, 404, 422]

    def test_list_org_playbooks_response_structure(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test that organization playbooks response has expected structure."""
        response = api_client.get(f"/organizations/{org_id}/playbooks")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))


class TestCreateOrganizationPlaybook:
    """Tests for the Create Organization Playbook endpoint."""

    def test_create_org_playbook_missing_required_fields(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test creating organization playbook without required fields returns error."""
        response = api_client.post(f"/organizations/{org_id}/playbooks", json={})
        assert response.status_code in [400, 422]

    def test_create_org_playbook_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test creating playbook with invalid organization ID returns error."""
        response = api_client.post(
            "/organizations/invalid-org-id/playbooks",
            json={"name": "Test Playbook", "content": "Test content"},
        )
        assert response.status_code in [400, 404, 422]


class TestUpdateOrganizationPlaybook:
    """Tests for the Update Organization Playbook endpoint."""

    def test_update_org_playbook_invalid_id(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test updating organization playbook with invalid ID returns error."""
        response = api_client.patch(
            f"/organizations/{org_id}/playbooks/invalid-playbook-id",
            json={"name": "Updated Playbook"},
        )
        assert response.status_code in [400, 404, 422]


class TestDeleteOrganizationPlaybook:
    """Tests for the Delete Organization Playbook endpoint."""

    def test_delete_org_playbook_invalid_id(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test deleting organization playbook with invalid ID returns error."""
        response = api_client.delete(f"/organizations/{org_id}/playbooks/invalid-playbook-id")
        assert response.status_code in [400, 404, 422]

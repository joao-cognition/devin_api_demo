"""Tests for Knowledge Notes API endpoints.

This module tests the following endpoints:
Enterprise Knowledge Notes:
- GET /v3beta1/enterprise/knowledge-notes - List Enterprise Knowledge Notes
- POST /v3beta1/enterprise/knowledge-notes - Create Enterprise Knowledge Note
- PATCH /v3beta1/enterprise/knowledge-notes/{note_id} - Update Enterprise Knowledge Note
- DELETE /v3beta1/enterprise/knowledge-notes/{note_id} - Delete Enterprise Knowledge Note

Organization Knowledge Notes:
- GET /v3beta1/organizations/{org_id}/knowledge-notes - List Org Knowledge Notes
- POST /v3beta1/organizations/{org_id}/knowledge-notes - Create Org Knowledge Note
- PATCH /v3beta1/organizations/{org_id}/knowledge-notes/{note_id} - Update Org Note
- DELETE /v3beta1/organizations/{org_id}/knowledge-notes/{note_id} - Delete Org Note
"""


from devin_api_client import DevinAPIClient


class TestListEnterpriseKnowledgeNotes:
    """Tests for the List Enterprise Knowledge Notes endpoint."""

    def test_list_enterprise_knowledge_notes_success(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise knowledge notes returns successful response."""
        response = api_client.get("/enterprise/knowledge-notes")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "notes" in data or isinstance(data, list)

    def test_list_enterprise_knowledge_notes_with_limit(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise knowledge notes with limit parameter."""
        response = api_client.get("/enterprise/knowledge-notes", params={"limit": 5})
        assert response.status_code == 200

    def test_list_enterprise_knowledge_notes_with_offset(self, api_client: DevinAPIClient) -> None:
        """Test listing enterprise knowledge notes with offset parameter."""
        response = api_client.get("/enterprise/knowledge-notes", params={"offset": 0, "limit": 10})
        assert response.status_code == 200

    def test_list_enterprise_knowledge_notes_response_structure(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test that enterprise knowledge notes response has expected structure."""
        response = api_client.get("/enterprise/knowledge-notes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))


class TestCreateEnterpriseKnowledgeNote:
    """Tests for the Create Enterprise Knowledge Note endpoint."""

    def test_create_enterprise_knowledge_note_missing_required_fields(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test creating enterprise knowledge note without required fields returns error."""
        response = api_client.post("/enterprise/knowledge-notes", json={})
        assert response.status_code in [400, 422]

    def test_create_enterprise_knowledge_note_invalid_data(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test creating enterprise knowledge note with invalid data returns error."""
        response = api_client.post(
            "/enterprise/knowledge-notes",
            json={"invalid_field": "invalid_value"},
        )
        assert response.status_code in [400, 422]


class TestUpdateEnterpriseKnowledgeNote:
    """Tests for the Update Enterprise Knowledge Note endpoint."""

    def test_update_enterprise_knowledge_note_invalid_id(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test updating enterprise knowledge note with invalid ID returns error."""
        response = api_client.patch(
            "/enterprise/knowledge-notes/invalid-note-id",
            json={"content": "Updated content"},
        )
        assert response.status_code in [400, 404, 422]

    def test_update_enterprise_knowledge_note_nonexistent_id(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test updating enterprise knowledge note with nonexistent ID returns error."""
        response = api_client.patch(
            "/enterprise/knowledge-notes/00000000-0000-0000-0000-000000000000",
            json={"content": "Updated content"},
        )
        assert response.status_code in [400, 404, 422]


class TestDeleteEnterpriseKnowledgeNote:
    """Tests for the Delete Enterprise Knowledge Note endpoint."""

    def test_delete_enterprise_knowledge_note_invalid_id(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test deleting enterprise knowledge note with invalid ID returns error."""
        response = api_client.delete("/enterprise/knowledge-notes/invalid-note-id")
        assert response.status_code in [400, 404, 422]

    def test_delete_enterprise_knowledge_note_nonexistent_id(
        self, api_client: DevinAPIClient
    ) -> None:
        """Test deleting enterprise knowledge note with nonexistent ID returns error."""
        response = api_client.delete(
            "/enterprise/knowledge-notes/00000000-0000-0000-0000-000000000000"
        )
        assert response.status_code in [400, 404, 422]


class TestListOrganizationKnowledgeNotes:
    """Tests for the List Organization Knowledge Notes endpoint."""

    def test_list_org_knowledge_notes_success(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing organization knowledge notes returns successful response."""
        response = api_client.get(f"/organizations/{org_id}/knowledge-notes")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "notes" in data or isinstance(data, list)

    def test_list_org_knowledge_notes_with_limit(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test listing organization knowledge notes with limit parameter."""
        response = api_client.get(f"/organizations/{org_id}/knowledge-notes", params={"limit": 5})
        assert response.status_code == 200

    def test_list_org_knowledge_notes_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test listing knowledge notes with invalid organization ID returns error."""
        response = api_client.get("/organizations/invalid-org-id/knowledge-notes")
        assert response.status_code in [400, 404, 422]

    def test_list_org_knowledge_notes_response_structure(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test that organization knowledge notes response has expected structure."""
        response = api_client.get(f"/organizations/{org_id}/knowledge-notes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))


class TestCreateOrganizationKnowledgeNote:
    """Tests for the Create Organization Knowledge Note endpoint."""

    def test_create_org_knowledge_note_missing_required_fields(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test creating organization knowledge note without required fields returns error."""
        response = api_client.post(f"/organizations/{org_id}/knowledge-notes", json={})
        assert response.status_code in [400, 422]

    def test_create_org_knowledge_note_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test creating knowledge note with invalid organization ID returns error."""
        response = api_client.post(
            "/organizations/invalid-org-id/knowledge-notes",
            json={"name": "Test Note", "content": "Test content"},
        )
        assert response.status_code in [400, 404, 422]


class TestUpdateOrganizationKnowledgeNote:
    """Tests for the Update Organization Knowledge Note endpoint."""

    def test_update_org_knowledge_note_invalid_id(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test updating organization knowledge note with invalid ID returns error."""
        response = api_client.patch(
            f"/organizations/{org_id}/knowledge-notes/invalid-note-id",
            json={"content": "Updated content"},
        )
        assert response.status_code in [400, 404, 422]


class TestDeleteOrganizationKnowledgeNote:
    """Tests for the Delete Organization Knowledge Note endpoint."""

    def test_delete_org_knowledge_note_invalid_id(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test deleting organization knowledge note with invalid ID returns error."""
        response = api_client.delete(f"/organizations/{org_id}/knowledge-notes/invalid-note-id")
        assert response.status_code in [400, 404, 422]

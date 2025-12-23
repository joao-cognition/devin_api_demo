"""Tests for Tags API endpoints.

This module tests the following endpoints:
- GET /v3beta1/enterprise/organizations/{org_id}/tags - Get Organization Allowed Tags
- POST /v3beta1/enterprise/organizations/{org_id}/tags - Append Organization Tags
- PUT /v3beta1/enterprise/organizations/{org_id}/tags - Replace Organization Allowed Tags
- DELETE /v3beta1/enterprise/organizations/{org_id}/tags - Clear Organization Tags
- DELETE /v3beta1/enterprise/organizations/{org_id}/tags/{tag} - Remove Organization Tag
"""


from devin_api_client import DevinAPIClient


class TestGetOrganizationAllowedTags:
    """Tests for the Get Organization Allowed Tags endpoint."""

    def test_get_org_allowed_tags_success(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test getting organization allowed tags returns successful response."""
        response = api_client.get(f"/enterprise/organizations/{org_id}/tags")
        assert response.status_code == 200
        data = response.json()
        assert "tags" in data or isinstance(data, list)

    def test_get_org_allowed_tags_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test getting allowed tags with invalid organization ID returns error."""
        response = api_client.get("/enterprise/organizations/invalid-org-id/tags")
        assert response.status_code in [400, 404, 422]

    def test_get_org_allowed_tags_response_structure(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test that organization allowed tags response has expected structure."""
        response = api_client.get(f"/enterprise/organizations/{org_id}/tags")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))
        if isinstance(data, dict):
            assert "tags" in data


class TestAppendOrganizationTags:
    """Tests for the Append Organization Tags endpoint."""

    def test_append_org_tags_missing_required_fields(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test appending organization tags without required fields returns error."""
        response = api_client.post(f"/enterprise/organizations/{org_id}/tags", json={})
        assert response.status_code in [400, 422]

    def test_append_org_tags_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test appending tags with invalid organization ID returns error."""
        response = api_client.post(
            "/enterprise/organizations/invalid-org-id/tags",
            json={"tags": ["test-tag"]},
        )
        assert response.status_code in [400, 404, 422]

    def test_append_org_tags_with_valid_data(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test appending organization tags with valid data."""
        response = api_client.post(
            f"/enterprise/organizations/{org_id}/tags",
            json={"tags": ["test-tag-append"]},
        )
        assert response.status_code in [200, 201, 400, 422]

    def test_append_org_tags_empty_tags_list(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test appending organization tags with empty tags list."""
        response = api_client.post(
            f"/enterprise/organizations/{org_id}/tags",
            json={"tags": []},
        )
        assert response.status_code in [200, 400, 422]


class TestReplaceOrganizationAllowedTags:
    """Tests for the Replace Organization Allowed Tags endpoint."""

    def test_replace_org_allowed_tags_missing_required_fields(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test replacing organization allowed tags without required fields returns error."""
        response = api_client.put(f"/enterprise/organizations/{org_id}/tags", json={})
        assert response.status_code in [400, 422]

    def test_replace_org_allowed_tags_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test replacing allowed tags with invalid organization ID returns error."""
        response = api_client.put(
            "/enterprise/organizations/invalid-org-id/tags",
            json={"tags": ["test-tag"]},
        )
        assert response.status_code in [400, 404, 422]

    def test_replace_org_allowed_tags_with_valid_data(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test replacing organization allowed tags with valid data."""
        response = api_client.put(
            f"/enterprise/organizations/{org_id}/tags",
            json={"tags": ["test-tag-replace"]},
        )
        assert response.status_code in [200, 400, 422]

    def test_replace_org_allowed_tags_empty_tags_list(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test replacing organization allowed tags with empty tags list."""
        response = api_client.put(
            f"/enterprise/organizations/{org_id}/tags",
            json={"tags": []},
        )
        assert response.status_code in [200, 400, 422]


class TestClearOrganizationTags:
    """Tests for the Clear Organization Tags endpoint."""

    def test_clear_org_tags_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test clearing tags with invalid organization ID returns error."""
        response = api_client.delete("/enterprise/organizations/invalid-org-id/tags")
        assert response.status_code in [400, 404, 422]

    def test_clear_org_tags_nonexistent_org_id(self, api_client: DevinAPIClient) -> None:
        """Test clearing tags with nonexistent organization ID returns error."""
        response = api_client.delete(
            "/enterprise/organizations/00000000-0000-0000-0000-000000000000/tags"
        )
        assert response.status_code in [400, 404, 422]


class TestRemoveOrganizationTag:
    """Tests for the Remove Organization Tag endpoint."""

    def test_remove_org_tag_invalid_org_id(self, api_client: DevinAPIClient) -> None:
        """Test removing tag with invalid organization ID returns error."""
        response = api_client.delete("/enterprise/organizations/invalid-org-id/tags/test-tag")
        assert response.status_code in [400, 404, 422]

    def test_remove_org_tag_nonexistent_tag(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test removing nonexistent tag returns appropriate response."""
        response = api_client.delete(
            f"/enterprise/organizations/{org_id}/tags/nonexistent-tag-12345"
        )
        assert response.status_code in [200, 204, 400, 404, 422]

    def test_remove_org_tag_empty_tag_name(
        self, api_client: DevinAPIClient, org_id: str
    ) -> None:
        """Test removing tag with empty tag name."""
        response = api_client.delete(f"/enterprise/organizations/{org_id}/tags/")
        assert response.status_code in [400, 404, 405, 422]

"""Shared pytest fixtures for Devin API tests."""

import pytest
from devin_api_client import DevinAPIClient, DevinAPIConfig


@pytest.fixture(scope="session")
def api_config() -> DevinAPIConfig:
    """Create API configuration from environment."""
    return DevinAPIConfig.from_env()


@pytest.fixture(scope="session")
def api_client(api_config: DevinAPIConfig) -> DevinAPIClient:
    """Create API client for testing."""
    return DevinAPIClient(api_config)


@pytest.fixture(scope="session")
def org_id(api_client: DevinAPIClient) -> str:
    """Get the first organization ID for testing."""
    response = api_client.get("/enterprise/organizations")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data and data["items"]
    return data["items"][0].get("org_id") or data["items"][0].get("id")

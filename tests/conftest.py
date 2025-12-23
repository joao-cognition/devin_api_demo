"""Shared pytest fixtures for Devin API tests."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from devin_api_client import DevinAPIClient, DevinAPIConfig


@pytest.fixture
def api_config() -> DevinAPIConfig:
    """Create API configuration from environment variables.

    Returns:
        DevinAPIConfig instance.
    """
    return DevinAPIConfig.from_env()


@pytest.fixture
def api_client(api_config: DevinAPIConfig) -> DevinAPIClient:
    """Create API client instance.

    Args:
        api_config: The API configuration.

    Yields:
        DevinAPIClient instance.
    """
    with DevinAPIClient(api_config) as client:
        yield client


@pytest.fixture
def org_id(api_client: DevinAPIClient) -> str:
    """Get an organization ID for testing.

    Args:
        api_client: The API client.

    Returns:
        An organization ID string.
    """
    response = api_client.get("/enterprise/organizations")
    response.raise_for_status()
    data = response.json()
    items = data.get("items", [])
    if not items:
        pytest.skip("No organizations available for testing")
    return items[0]["org_id"]


@pytest.fixture
def user_id(api_client: DevinAPIClient) -> str:
    """Get a user ID for testing.

    Args:
        api_client: The API client.

    Returns:
        A user ID string.
    """
    response = api_client.get("/enterprise/users")
    response.raise_for_status()
    data = response.json()
    items = data.get("items", [])
    if not items:
        pytest.skip("No users available for testing")
    return items[0]["user_id"]


@pytest.fixture
def session_id(api_client: DevinAPIClient, org_id: str) -> str:
    """Get a session ID for testing.

    Args:
        api_client: The API client.
        org_id: The organization ID.

    Returns:
        A session ID string.
    """
    response = api_client.get(f"/organizations/{org_id}/sessions")
    response.raise_for_status()
    data = response.json()
    items = data.get("items", [])
    if not items:
        pytest.skip("No sessions available for testing")
    return items[0]["session_id"]

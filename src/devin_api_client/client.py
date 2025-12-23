"""Base API client for Devin API."""

from typing import Any

import httpx

from .config import DevinAPIConfig


class DevinAPIClient:
    """HTTP client for interacting with the Devin API.

    Attributes:
        config: The API configuration.
        _client: The underlying HTTP client.
    """

    def __init__(self, config: DevinAPIConfig) -> None:
        """Initialize the Devin API client.

        Args:
            config: The API configuration containing credentials and base URL.
        """
        self.config = config
        self._client = httpx.Client(
            base_url=config.base_url,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "DevinAPIClient":
        """Enter context manager."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Exit context manager."""
        self.close()

    def get(self, path: str, params: dict[str, Any] | None = None) -> httpx.Response:
        """Make a GET request to the API.

        Args:
            path: The API endpoint path.
            params: Optional query parameters.

        Returns:
            The HTTP response.
        """
        return self._client.get(path, params=params)

    def post(
        self, path: str, json: dict[str, Any] | None = None, params: dict[str, Any] | None = None
    ) -> httpx.Response:
        """Make a POST request to the API.

        Args:
            path: The API endpoint path.
            json: Optional JSON body.
            params: Optional query parameters.

        Returns:
            The HTTP response.
        """
        return self._client.post(path, json=json, params=params)

    def put(
        self, path: str, json: dict[str, Any] | None = None, params: dict[str, Any] | None = None
    ) -> httpx.Response:
        """Make a PUT request to the API.

        Args:
            path: The API endpoint path.
            json: Optional JSON body.
            params: Optional query parameters.

        Returns:
            The HTTP response.
        """
        return self._client.put(path, json=json, params=params)

    def patch(
        self, path: str, json: dict[str, Any] | None = None, params: dict[str, Any] | None = None
    ) -> httpx.Response:
        """Make a PATCH request to the API.

        Args:
            path: The API endpoint path.
            json: Optional JSON body.
            params: Optional query parameters.

        Returns:
            The HTTP response.
        """
        return self._client.patch(path, json=json, params=params)

    def delete(self, path: str, params: dict[str, Any] | None = None) -> httpx.Response:
        """Make a DELETE request to the API.

        Args:
            path: The API endpoint path.
            params: Optional query parameters.

        Returns:
            The HTTP response.
        """
        return self._client.delete(path, params=params)

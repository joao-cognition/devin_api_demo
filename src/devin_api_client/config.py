"""Configuration module for Devin API client."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class DevinAPIConfig:
    """Configuration for the Devin API client.

    Attributes:
        api_key: The API key for authentication.
        base_url: The base URL for the Devin API.
    """

    api_key: str
    base_url: str = "https://api.devin.ai/v3beta1"

    @classmethod
    def from_env(cls) -> "DevinAPIConfig":
        """Create configuration from environment variables.

        Returns:
            DevinAPIConfig instance with values from environment.

        Raises:
            ValueError: If DEVIN_API_KEY environment variable is not set.
        """
        api_key = os.environ.get("DEVIN_API_KEY")
        if not api_key:
            raise ValueError("DEVIN_API_KEY environment variable is required")

        base_url = os.environ.get("DEVIN_API_BASE_URL", "https://api.devin.ai/v3beta1")
        return cls(api_key=api_key, base_url=base_url)

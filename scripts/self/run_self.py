#!/usr/bin/env python3
"""Self API - GET /enterprise/self"""

import json
from devin_api_client import DevinAPIClient, DevinAPIConfig


def get_self(client: DevinAPIClient):
    """Get authenticated service user info."""
    return client.get("/enterprise/self")


def main():
    client = DevinAPIClient(DevinAPIConfig.from_env())
    response = get_self(client)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    main()

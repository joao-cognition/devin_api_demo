#!/usr/bin/env python3
"""Script to run ALL Roles API endpoints and display output.

Available operations:
- GET /enterprise/roles - List Roles
"""

import json
import sys
from devin_api_client import DevinAPIClient, DevinAPIConfig


def print_section(title: str):
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print("=" * 70)


def print_response(response):
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
        return data
    except:
        print(f"Response: {response.text[:500]}")
        return None


def list_roles(client):
    """List all available roles."""
    print_section("GET /enterprise/roles - List Roles")
    response = client.get("/enterprise/roles")
    return print_response(response)


def main():
    """Run Roles API endpoints based on command line arguments."""
    config = DevinAPIConfig.from_env()
    client = DevinAPIClient(config)

    if len(sys.argv) < 2:
        print("Usage: python run_roles.py <command>")
        print("\nCommands:")
        print("  list  - List all available roles")
        print("  all   - Run all operations (same as list)")
        print("\nExamples:")
        print('  python run_roles.py list')
        return

    command = sys.argv[1]

    if command == "list" or command == "all":
        list_roles(client)

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()

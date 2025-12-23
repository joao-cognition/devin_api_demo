#!/usr/bin/env python3
"""Script to run ALL Git Connections API endpoints and display output.

Available operations:
- GET /enterprise/git-connections - List Git Connections
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


def list_git_connections(client):
    """List all git connections."""
    print_section("GET /enterprise/git-connections - List Git Connections")
    response = client.get("/enterprise/git-connections")
    return print_response(response)


def main():
    """Run Git Connections API endpoints based on command line arguments."""
    config = DevinAPIConfig.from_env()
    client = DevinAPIClient(config)

    if len(sys.argv) < 2:
        print("Usage: python run_git_connections.py <command>")
        print("\nCommands:")
        print("  list  - List all git connections")
        print("  all   - Run all operations (same as list)")
        print("\nExamples:")
        print('  python run_git_connections.py list')
        return

    command = sys.argv[1]

    if command == "list" or command == "all":
        list_git_connections(client)

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()

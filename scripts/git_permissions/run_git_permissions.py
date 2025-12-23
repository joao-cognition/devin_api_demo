#!/usr/bin/env python3
"""Script to run ALL Git Permissions API endpoints and display output.

Available operations:
- GET /organizations/{org_id}/git-providers/{provider}/permissions - List Permissions
- POST /organizations/{org_id}/git-providers/{provider}/permissions - Add Permission
- DELETE /organizations/{org_id}/git-providers/{provider}/permissions/{id} - Remove Permission
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


def get_org_id(client):
    """Get the first organization ID."""
    response = client.get("/enterprise/organizations")
    if response.status_code == 200:
        data = response.json()
        if "items" in data and data["items"]:
            return data["items"][0].get("org_id") or data["items"][0].get("id")
    return None


def list_permissions(client, org_id: str, provider: str = "github"):
    """List git permissions for an organization."""
    print_section(f"GET /organizations/{org_id}/git-providers/{provider}/permissions - List")
    response = client.get(f"/organizations/{org_id}/git-providers/{provider}/permissions")
    return print_response(response)


def add_permission(client, org_id: str, provider: str, repo_url: str, permission_type: str = "read"):
    """Add a git permission."""
    print_section(f"POST /organizations/{org_id}/git-providers/{provider}/permissions - Add")
    response = client.post(f"/organizations/{org_id}/git-providers/{provider}/permissions", json={
        "repo_url": repo_url,
        "permission_type": permission_type
    })
    return print_response(response)


def remove_permission(client, org_id: str, provider: str, permission_id: str):
    """Remove a git permission."""
    print_section(f"DELETE /organizations/{org_id}/git-providers/{provider}/permissions/{permission_id}")
    response = client.delete(f"/organizations/{org_id}/git-providers/{provider}/permissions/{permission_id}")
    return print_response(response)


def main():
    """Run Git Permissions API endpoints based on command line arguments."""
    config = DevinAPIConfig.from_env()
    client = DevinAPIClient(config)

    org_id = get_org_id(client)
    if not org_id:
        print("No organization found")
        return

    if len(sys.argv) < 2:
        print("Usage: python run_git_permissions.py <command> [args]")
        print("\nCommands:")
        print("  list [provider]                        - List git permissions (default: github)")
        print("  add <provider> <repo_url> [perm_type]  - Add git permission")
        print("  remove <provider> <permission_id>      - Remove git permission")
        print("  all                                    - Run list operation")
        print("\nProviders: github, gitlab, bitbucket")
        print("\nExamples:")
        print('  python run_git_permissions.py list')
        print('  python run_git_permissions.py list github')
        print('  python run_git_permissions.py add github "https://github.com/org/repo" read')
        return

    command = sys.argv[1]

    if command == "list" or command == "all":
        provider = sys.argv[2] if len(sys.argv) > 2 else "github"
        list_permissions(client, org_id, provider)

    elif command == "add":
        if len(sys.argv) < 4:
            print("Usage: python run_git_permissions.py add <provider> <repo_url> [perm_type]")
            return
        provider = sys.argv[2]
        repo_url = sys.argv[3]
        perm_type = sys.argv[4] if len(sys.argv) > 4 else "read"
        add_permission(client, org_id, provider, repo_url, perm_type)

    elif command == "remove":
        if len(sys.argv) < 4:
            print("Usage: python run_git_permissions.py remove <provider> <permission_id>")
            return
        remove_permission(client, org_id, sys.argv[2], sys.argv[3])

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Script to run ALL IDP Groups API endpoints and display output.

Available operations:
- GET /enterprise/members/idp-groups - List Enterprise Groups
- POST /enterprise/members/idp-groups - Add Enterprise Group
- GET /enterprise/organizations/{org_id}/members/idp-groups - List Org Groups
- POST /enterprise/organizations/{org_id}/members/idp-groups - Add Org Group
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


def list_enterprise_groups(client):
    """List all enterprise IDP groups."""
    print_section("GET /enterprise/members/idp-groups - List Enterprise Groups")
    response = client.get("/enterprise/members/idp-groups")
    return print_response(response)


def add_enterprise_group(client, group_id: str, role_id: str = "enterprise_member"):
    """Add an IDP group to the enterprise."""
    print_section("POST /enterprise/members/idp-groups - Add Enterprise Group")
    response = client.post("/enterprise/members/idp-groups", json={
        "group_id": group_id,
        "role_id": role_id
    })
    return print_response(response)


def list_org_groups(client, org_id: str):
    """List all IDP groups in an organization."""
    print_section(f"GET /enterprise/organizations/{org_id}/members/idp-groups - List Org Groups")
    response = client.get(f"/enterprise/organizations/{org_id}/members/idp-groups")
    return print_response(response)


def add_org_group(client, org_id: str, group_id: str, role_id: str = "org_member"):
    """Add an IDP group to an organization."""
    print_section(f"POST /enterprise/organizations/{org_id}/members/idp-groups - Add Org Group")
    response = client.post(f"/enterprise/organizations/{org_id}/members/idp-groups", json={
        "group_id": group_id,
        "role_id": role_id
    })
    return print_response(response)


def main():
    """Run IDP Groups API endpoints based on command line arguments."""
    config = DevinAPIConfig.from_env()
    client = DevinAPIClient(config)

    if len(sys.argv) < 2:
        print("Usage: python run_idp_groups.py <command> [args]")
        print("\nCommands:")
        print("  list                         - List enterprise IDP groups")
        print("  add <group_id> [role_id]     - Add enterprise IDP group")
        print("  list-org                     - List organization IDP groups")
        print("  add-org <group_id> [role_id] - Add IDP group to organization")
        print("  all                          - Run all list operations")
        print("\nExamples:")
        print('  python run_idp_groups.py list')
        print('  python run_idp_groups.py add "group-123" "enterprise_admin"')
        return

    command = sys.argv[1]
    org_id = get_org_id(client)

    if command == "list":
        list_enterprise_groups(client)

    elif command == "add":
        if len(sys.argv) < 3:
            print("Usage: python run_idp_groups.py add <group_id> [role_id]")
            return
        role_id = sys.argv[3] if len(sys.argv) > 3 else "enterprise_member"
        add_enterprise_group(client, sys.argv[2], role_id)

    elif command == "list-org":
        if not org_id:
            print("No organization found")
            return
        list_org_groups(client, org_id)

    elif command == "add-org":
        if not org_id:
            print("No organization found")
            return
        if len(sys.argv) < 3:
            print("Usage: python run_idp_groups.py add-org <group_id> [role_id]")
            return
        role_id = sys.argv[3] if len(sys.argv) > 3 else "org_member"
        add_org_group(client, org_id, sys.argv[2], role_id)

    elif command == "all":
        list_enterprise_groups(client)
        if org_id:
            list_org_groups(client, org_id)

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()

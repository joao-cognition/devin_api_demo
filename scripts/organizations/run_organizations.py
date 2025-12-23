#!/usr/bin/env python3
"""Organizations API - list, create, update, delete"""

import json
import sys
from devin_api_client import DevinAPIClient, DevinAPIConfig


def list_organizations(client: DevinAPIClient):
    """List all organizations."""
    return client.get("/enterprise/organizations")


def create_organization(client: DevinAPIClient, name: str):
    """Create a new organization."""
    return client.post("/enterprise/organizations", json={"name": name})


def update_organization(client: DevinAPIClient, org_id: str, name: str):
    """Update an organization."""
    return client.patch(f"/enterprise/organizations/{org_id}", json={"name": name})


def delete_organization(client: DevinAPIClient, org_id: str):
    """Delete an organization."""
    return client.delete(f"/enterprise/organizations/{org_id}")


def main():
    client = DevinAPIClient(DevinAPIConfig.from_env())
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if cmd == "list":
        r = list_organizations(client)
    elif cmd == "create" and len(sys.argv) > 2:
        r = create_organization(client, sys.argv[2])
    elif cmd == "update" and len(sys.argv) > 3:
        r = update_organization(client, sys.argv[2], sys.argv[3])
    elif cmd == "delete" and len(sys.argv) > 2:
        r = delete_organization(client, sys.argv[2])
    else:
        print("Usage: run_organizations.py [list|create <name>|update <id> <name>|delete <id>]")
        return
    
    print(f"Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2))


if __name__ == "__main__":
    main()

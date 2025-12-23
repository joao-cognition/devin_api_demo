#!/usr/bin/env python3
"""Service Users API - list, create, delete"""

import json
import sys
from devin_api_client import DevinAPIClient, DevinAPIConfig


def list_service_users(client: DevinAPIClient):
    """List service users."""
    return client.get("/enterprise/members/service-users")


def create_service_user(client: DevinAPIClient, name: str):
    """Create a service user."""
    return client.post("/enterprise/members/service-users", json={"name": name})


def delete_service_user(client: DevinAPIClient, service_user_id: str):
    """Delete a service user."""
    return client.delete(f"/enterprise/members/service-users/{service_user_id}")


def main():
    client = DevinAPIClient(DevinAPIConfig.from_env())
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if cmd == "list":
        r = list_service_users(client)
    elif cmd == "create" and len(sys.argv) > 2:
        r = create_service_user(client, sys.argv[2])
    elif cmd == "delete" and len(sys.argv) > 2:
        r = delete_service_user(client, sys.argv[2])
    else:
        print("Usage: run_service_users.py [list|create <name>|delete <id>]")
        return
    
    print(f"Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2))


if __name__ == "__main__":
    main()

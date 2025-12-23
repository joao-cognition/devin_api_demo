#!/usr/bin/env python3
"""Users API - list, add, update, remove (enterprise and org level)"""

import json
import sys
from devin_api_client import DevinAPIClient, DevinAPIConfig


def get_org_id(client: DevinAPIClient):
    r = client.get("/enterprise/organizations")
    if r.status_code == 200 and r.json().get("items"):
        return r.json()["items"][0].get("org_id") or r.json()["items"][0].get("id")
    return None


def list_enterprise_users(client: DevinAPIClient):
    """List enterprise users."""
    return client.get("/enterprise/members/users")


def list_org_users(client: DevinAPIClient, org_id: str):
    """List organization users."""
    return client.get(f"/enterprise/organizations/{org_id}/members/users")


def add_user(client: DevinAPIClient, email: str):
    """Add a user to enterprise."""
    return client.post("/enterprise/members/users", json={"email": email})


def remove_user(client: DevinAPIClient, user_id: str):
    """Remove a user from enterprise."""
    return client.delete(f"/enterprise/members/users/{user_id}")


def main():
    client = DevinAPIClient(DevinAPIConfig.from_env())
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if cmd == "list":
        r = list_enterprise_users(client)
    elif cmd == "list-org":
        org_id = get_org_id(client)
        r = list_org_users(client, org_id)
    elif cmd == "add" and len(sys.argv) > 2:
        r = add_user(client, sys.argv[2])
    elif cmd == "remove" and len(sys.argv) > 2:
        r = remove_user(client, sys.argv[2])
    else:
        print("Usage: run_users.py [list|list-org|add <email>|remove <user_id>]")
        return
    
    print(f"Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2))


if __name__ == "__main__":
    main()

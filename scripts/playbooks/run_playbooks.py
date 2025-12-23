#!/usr/bin/env python3
"""Playbooks API - list, create (enterprise and org level)"""

import json
import sys
from devin_api_client import DevinAPIClient, DevinAPIConfig


def get_org_id(client: DevinAPIClient):
    r = client.get("/enterprise/organizations")
    if r.status_code == 200 and r.json().get("items"):
        return r.json()["items"][0].get("org_id") or r.json()["items"][0].get("id")
    return None


def list_enterprise_playbooks(client: DevinAPIClient):
    """List enterprise playbooks."""
    return client.get("/enterprise/playbooks")


def list_org_playbooks(client: DevinAPIClient, org_id: str):
    """List organization playbooks."""
    return client.get(f"/organizations/{org_id}/playbooks")


def create_playbook(client: DevinAPIClient, name: str, body: str):
    """Create an enterprise playbook."""
    return client.post("/enterprise/playbooks", json={"name": name, "body": body})


def main():
    client = DevinAPIClient(DevinAPIConfig.from_env())
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if cmd == "list":
        r = list_enterprise_playbooks(client)
    elif cmd == "list-org":
        r = list_org_playbooks(client, get_org_id(client))
    elif cmd == "create" and len(sys.argv) > 3:
        r = create_playbook(client, sys.argv[2], sys.argv[3])
    else:
        print("Usage: run_playbooks.py [list|list-org|create <name> <body>]")
        return
    
    print(f"Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Tags API - get, add, replace, delete"""

import json
import sys
from devin_api_client import DevinAPIClient, DevinAPIConfig


def get_org_id(client: DevinAPIClient):
    r = client.get("/enterprise/organizations")
    if r.status_code == 200 and r.json().get("items"):
        return r.json()["items"][0].get("org_id") or r.json()["items"][0].get("id")
    return None


def get_tags(client: DevinAPIClient, org_id: str):
    """Get organization tags."""
    return client.get(f"/enterprise/organizations/{org_id}/tags")


def add_tags(client: DevinAPIClient, org_id: str, tags: list):
    """Add tags to organization."""
    return client.post(f"/enterprise/organizations/{org_id}/tags", json={"tags": tags})


def replace_tags(client: DevinAPIClient, org_id: str, tags: list):
    """Replace all tags for organization."""
    return client.put(f"/enterprise/organizations/{org_id}/tags", json={"tags": tags})


def delete_tag(client: DevinAPIClient, org_id: str, tag: str):
    """Delete a tag from organization."""
    return client.delete(f"/enterprise/organizations/{org_id}/tags/{tag}")


def main():
    client = DevinAPIClient(DevinAPIConfig.from_env())
    org_id = get_org_id(client)
    cmd = sys.argv[1] if len(sys.argv) > 1 else "get"
    
    if cmd == "get":
        r = get_tags(client, org_id)
    elif cmd == "add" and len(sys.argv) > 2:
        r = add_tags(client, org_id, sys.argv[2:])
    elif cmd == "replace" and len(sys.argv) > 2:
        r = replace_tags(client, org_id, sys.argv[2:])
    elif cmd == "delete" and len(sys.argv) > 2:
        r = delete_tag(client, org_id, sys.argv[2])
    else:
        print("Usage: run_tags.py [get|add <tags...>|replace <tags...>|delete <tag>]")
        return
    
    print(f"Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Sessions API - list, create, terminate, archive"""

import json
import sys
from devin_api_client import DevinAPIClient, DevinAPIConfig


def get_org_id(client: DevinAPIClient):
    r = client.get("/enterprise/organizations")
    if r.status_code == 200 and r.json().get("items"):
        return r.json()["items"][0].get("org_id") or r.json()["items"][0].get("id")
    return None


def list_sessions(client: DevinAPIClient, org_id: str):
    """List sessions for an organization."""
    return client.get(f"/organizations/{org_id}/sessions")


def create_session(client: DevinAPIClient, org_id: str, prompt: str):
    """Create a new session."""
    return client.post(f"/organizations/{org_id}/sessions", json={"prompt": prompt})


def terminate_session(client: DevinAPIClient, session_id: str):
    """Terminate a session."""
    return client.delete(f"/sessions/{session_id}")


def archive_session(client: DevinAPIClient, session_id: str):
    """Archive a session."""
    return client.post(f"/sessions/{session_id}/archive")


def main():
    client = DevinAPIClient(DevinAPIConfig.from_env())
    org_id = get_org_id(client)
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if cmd == "list":
        r = list_sessions(client, org_id)
    elif cmd == "create" and len(sys.argv) > 2:
        r = create_session(client, org_id, sys.argv[2])
    elif cmd == "terminate" and len(sys.argv) > 2:
        r = terminate_session(client, sys.argv[2])
    elif cmd == "archive" and len(sys.argv) > 2:
        r = archive_session(client, sys.argv[2])
    else:
        print("Usage: run_sessions.py [list|create <prompt>|terminate <id>|archive <id>]")
        return
    
    print(f"Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2))


if __name__ == "__main__":
    main()

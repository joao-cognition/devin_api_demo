#!/usr/bin/env python3
"""Script to run ALL Knowledge Notes API endpoints and display output.

Available operations:
- GET /enterprise/knowledge/notes - List Enterprise Notes
- POST /enterprise/knowledge/notes - Create Enterprise Note
- GET /organizations/{org_id}/knowledge/notes - List Org Notes
- POST /organizations/{org_id}/knowledge/notes - Create Org Note
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


def list_enterprise_notes(client):
    """List all enterprise knowledge notes."""
    print_section("GET /enterprise/knowledge/notes - List Enterprise Notes")
    response = client.get("/enterprise/knowledge/notes")
    return print_response(response)


def create_enterprise_note(client, name: str, body: str, trigger: str = None):
    """Create an enterprise knowledge note."""
    print_section("POST /enterprise/knowledge/notes - Create Enterprise Note")
    payload = {"name": name, "body": body}
    if trigger:
        payload["trigger"] = trigger
    response = client.post("/enterprise/knowledge/notes", json=payload)
    return print_response(response)


def list_org_notes(client, org_id: str):
    """List all knowledge notes in an organization."""
    print_section(f"GET /organizations/{org_id}/knowledge/notes - List Org Notes")
    response = client.get(f"/organizations/{org_id}/knowledge/notes")
    return print_response(response)


def create_org_note(client, org_id: str, name: str, body: str, trigger: str = None):
    """Create an organization knowledge note."""
    print_section(f"POST /organizations/{org_id}/knowledge/notes - Create Org Note")
    payload = {"name": name, "body": body}
    if trigger:
        payload["trigger"] = trigger
    response = client.post(f"/organizations/{org_id}/knowledge/notes", json=payload)
    return print_response(response)


def main():
    """Run Knowledge Notes API endpoints based on command line arguments."""
    config = DevinAPIConfig.from_env()
    client = DevinAPIClient(config)

    if len(sys.argv) < 2:
        print("Usage: python run_knowledge_notes.py <command> [args]")
        print("\nCommands:")
        print("  list                           - List enterprise notes")
        print("  create <name> <body> [trigger] - Create enterprise note")
        print("  list-org                       - List organization notes")
        print("  create-org <name> <body>       - Create organization note")
        print("  all                            - Run all list operations")
        print("\nExamples:")
        print('  python run_knowledge_notes.py list')
        print('  python run_knowledge_notes.py create "Code Style" "Always use TypeScript"')
        return

    command = sys.argv[1]
    org_id = get_org_id(client)

    if command == "list":
        list_enterprise_notes(client)

    elif command == "create":
        if len(sys.argv) < 4:
            print("Usage: python run_knowledge_notes.py create <name> <body> [trigger]")
            return
        trigger = sys.argv[4] if len(sys.argv) > 4 else None
        create_enterprise_note(client, sys.argv[2], sys.argv[3], trigger)

    elif command == "list-org":
        if not org_id:
            print("No organization found")
            return
        list_org_notes(client, org_id)

    elif command == "create-org":
        if not org_id:
            print("No organization found")
            return
        if len(sys.argv) < 4:
            print("Usage: python run_knowledge_notes.py create-org <name> <body>")
            return
        create_org_note(client, org_id, sys.argv[2], sys.argv[3])

    elif command == "all":
        list_enterprise_notes(client)
        if org_id:
            list_org_notes(client, org_id)

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()

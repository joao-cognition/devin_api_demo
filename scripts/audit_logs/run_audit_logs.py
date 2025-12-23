#!/usr/bin/env python3
"""Script to run ALL Audit Logs API endpoints and display output.

Available operations:
- GET /enterprise/audit-logs - Enterprise Audit Logs
- GET /organizations/{org_id}/audit-logs - Organization Audit Logs
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


def list_enterprise_logs(client, limit: int = 10, action: str = None):
    """List enterprise audit logs."""
    print_section("GET /enterprise/audit-logs - Enterprise Audit Logs")
    params = {"limit": limit}
    if action:
        params["action"] = action
    response = client.get("/enterprise/audit-logs", params=params)
    return print_response(response)


def list_org_logs(client, org_id: str, limit: int = 10, action: str = None):
    """List organization audit logs."""
    print_section(f"GET /organizations/{org_id}/audit-logs - Organization Audit Logs")
    params = {"limit": limit}
    if action:
        params["action"] = action
    response = client.get(f"/organizations/{org_id}/audit-logs", params=params)
    return print_response(response)


def main():
    """Run Audit Logs API endpoints based on command line arguments."""
    config = DevinAPIConfig.from_env()
    client = DevinAPIClient(config)

    if len(sys.argv) < 2:
        print("Usage: python run_audit_logs.py <command> [args]")
        print("\nCommands:")
        print("  list [limit] [action]     - List enterprise audit logs")
        print("  list-org [limit] [action] - List organization audit logs")
        print("  all                       - Run all list operations")
        print("\nExamples:")
        print('  python run_audit_logs.py list')
        print('  python run_audit_logs.py list 20')
        print('  python run_audit_logs.py list 10 "session.created"')
        print('  python run_audit_logs.py list-org')
        return

    command = sys.argv[1]
    org_id = get_org_id(client)

    if command == "list":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        action = sys.argv[3] if len(sys.argv) > 3 else None
        list_enterprise_logs(client, limit, action)

    elif command == "list-org":
        if not org_id:
            print("No organization found")
            return
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        action = sys.argv[3] if len(sys.argv) > 3 else None
        list_org_logs(client, org_id, limit, action)

    elif command == "all":
        list_enterprise_logs(client)
        if org_id:
            list_org_logs(client, org_id)

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()

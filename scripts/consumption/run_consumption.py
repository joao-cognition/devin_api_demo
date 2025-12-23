#!/usr/bin/env python3
"""Script to run ALL Consumption API endpoints and display output.

Available operations:
- GET /enterprise/consumption/cycles - Consumption Cycles
- GET /enterprise/consumption/daily - Daily Consumption
- GET /organizations/{org_id}/consumption/daily - By Organization
- GET /enterprise/members/users/{user_id}/consumption/daily - By User
- GET /sessions/{session_id}/consumption/daily - By Session
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


def get_user_id(client):
    """Get the first user ID."""
    response = client.get("/enterprise/members/users")
    if response.status_code == 200:
        data = response.json()
        if "items" in data and data["items"]:
            return data["items"][0].get("user_id") or data["items"][0].get("id")
    return None


def get_session_id(client, org_id: str):
    """Get the first session ID."""
    response = client.get(f"/organizations/{org_id}/sessions")
    if response.status_code == 200:
        data = response.json()
        if "items" in data and data["items"]:
            return data["items"][0].get("session_id") or data["items"][0].get("id")
    return None


def list_cycles(client):
    """List consumption cycles."""
    print_section("GET /enterprise/consumption/cycles - Consumption Cycles")
    response = client.get("/enterprise/consumption/cycles")
    return print_response(response)


def get_daily(client):
    """Get daily consumption."""
    print_section("GET /enterprise/consumption/daily - Daily Consumption")
    response = client.get("/enterprise/consumption/daily")
    return print_response(response)


def get_org_daily(client, org_id: str):
    """Get organization daily consumption."""
    print_section(f"GET /organizations/{org_id}/consumption/daily - By Organization")
    response = client.get(f"/organizations/{org_id}/consumption/daily")
    return print_response(response)


def get_user_daily(client, user_id: str):
    """Get user daily consumption."""
    print_section(f"GET /enterprise/members/users/{user_id}/consumption/daily - By User")
    response = client.get(f"/enterprise/members/users/{user_id}/consumption/daily")
    return print_response(response)


def get_session_daily(client, session_id: str):
    """Get session daily consumption."""
    print_section(f"GET /sessions/{session_id}/consumption/daily - By Session")
    response = client.get(f"/sessions/{session_id}/consumption/daily")
    return print_response(response)


def main():
    """Run Consumption API endpoints based on command line arguments."""
    config = DevinAPIConfig.from_env()
    client = DevinAPIClient(config)

    if len(sys.argv) < 2:
        print("Usage: python run_consumption.py <command> [args]")
        print("\nCommands:")
        print("  cycles                  - List consumption cycles")
        print("  daily                   - Get daily consumption")
        print("  by-org                  - Get consumption by organization")
        print("  by-user <user_id>       - Get consumption by user")
        print("  by-session <session_id> - Get consumption by session")
        print("  all                     - Run cycles and daily operations")
        print("\nExamples:")
        print('  python run_consumption.py cycles')
        print('  python run_consumption.py daily')
        print('  python run_consumption.py by-org')
        return

    command = sys.argv[1]
    org_id = get_org_id(client)

    if command == "cycles":
        list_cycles(client)

    elif command == "daily":
        get_daily(client)

    elif command == "by-org":
        if not org_id:
            print("No organization found")
            return
        get_org_daily(client, org_id)

    elif command == "by-user":
        if len(sys.argv) < 3:
            user_id = get_user_id(client)
            if not user_id:
                print("No user found. Usage: python run_consumption.py by-user <user_id>")
                return
        else:
            user_id = sys.argv[2]
        get_user_daily(client, user_id)

    elif command == "by-session":
        if len(sys.argv) < 3:
            if not org_id:
                print("No organization found")
                return
            session_id = get_session_id(client, org_id)
            if not session_id:
                print("No session found. Usage: python run_consumption.py by-session <session_id>")
                return
        else:
            session_id = sys.argv[2]
        get_session_daily(client, session_id)

    elif command == "all":
        list_cycles(client)
        get_daily(client)
        if org_id:
            get_org_daily(client, org_id)

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()

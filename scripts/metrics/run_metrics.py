#!/usr/bin/env python3
"""Script to run ALL Metrics API endpoints and display output.

Available operations:
- GET /enterprise/metrics/usage - Enterprise Usage Metrics
- GET /organizations/{org_id}/metrics/usage - Organization Usage Metrics
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


def get_enterprise_metrics(client):
    """Get enterprise usage metrics."""
    print_section("GET /enterprise/metrics/usage - Enterprise Usage Metrics")
    response = client.get("/enterprise/metrics/usage")
    return print_response(response)


def get_org_metrics(client, org_id: str):
    """Get organization usage metrics."""
    print_section(f"GET /organizations/{org_id}/metrics/usage - Organization Usage Metrics")
    response = client.get(f"/organizations/{org_id}/metrics/usage")
    return print_response(response)


def main():
    """Run Metrics API endpoints based on command line arguments."""
    config = DevinAPIConfig.from_env()
    client = DevinAPIClient(config)

    if len(sys.argv) < 2:
        print("Usage: python run_metrics.py <command>")
        print("\nCommands:")
        print("  enterprise  - Get enterprise usage metrics")
        print("  org         - Get organization usage metrics")
        print("  all         - Run all metrics operations")
        print("\nExamples:")
        print('  python run_metrics.py enterprise')
        print('  python run_metrics.py org')
        print('  python run_metrics.py all')
        return

    command = sys.argv[1]
    org_id = get_org_id(client)

    if command == "enterprise":
        get_enterprise_metrics(client)

    elif command == "org":
        if not org_id:
            print("No organization found")
            return
        get_org_metrics(client, org_id)

    elif command == "all":
        get_enterprise_metrics(client)
        if org_id:
            get_org_metrics(client, org_id)

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()

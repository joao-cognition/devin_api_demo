#!/usr/bin/env python3
"""Script to run all major Devin API endpoints and display output.

This script calls all API endpoints that are tested in the tests/ folder.
For individual endpoint scripts, see the corresponding folders under scripts/.

Available scripts:
  scripts/self/run_self.py                     - Self API
  scripts/organizations/run_organizations.py   - Organizations API
  scripts/users/run_users.py                   - Users API
  scripts/service_users/run_service_users.py   - Service Users API
  scripts/sessions/run_sessions.py             - Sessions API
  scripts/audit_logs/run_audit_logs.py         - Audit Logs API
  scripts/consumption/run_consumption.py       - Consumption API
  scripts/git_connections/run_git_connections.py - Git Connections API
  scripts/git_permissions/run_git_permissions.py - Git Permissions API
  scripts/hypervisors/run_hypervisors.py       - Hypervisors API
  scripts/idp_groups/run_idp_groups.py         - IDP Groups API
  scripts/knowledge_notes/run_knowledge_notes.py - Knowledge Notes API
  scripts/metrics/run_metrics.py               - Metrics API
  scripts/playbooks/run_playbooks.py           - Playbooks API
  scripts/roles/run_roles.py                   - Roles API
  scripts/tags/run_tags.py                     - Tags API
"""

import json
from devin_api_client import DevinAPIClient, DevinAPIConfig


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print("=" * 70)


def print_response(response):
    """Print API response details."""
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(f"Response:")
        print(json.dumps(data, indent=2))
        return data
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(f"Raw response: {response.text[:500]}")
        return None


def main():
    """Run all major API endpoints."""
    config = DevinAPIConfig.from_env()
    client = DevinAPIClient(config)

    # 1. Self
    print_section("GET /enterprise/self - Get Self Information")
    self_response = client.get("/enterprise/self")
    print_response(self_response)

    # 2. Organizations
    print_section("GET /enterprise/organizations - List Organizations")
    orgs_response = client.get("/enterprise/organizations")
    orgs_data = print_response(orgs_response)

    org_id = None
    if orgs_data and "items" in orgs_data and orgs_data["items"]:
        org_id = orgs_data["items"][0].get("org_id") or orgs_data["items"][0].get("id")
        print(f"\n  → Using Organization ID: {org_id}")

    # 3. Enterprise Users
    print_section("GET /enterprise/members/users - List Enterprise Users")
    users_response = client.get("/enterprise/members/users")
    users_data = print_response(users_response)

    user_id = None
    if users_data and "items" in users_data and users_data["items"]:
        user_id = users_data["items"][0].get("user_id") or users_data["items"][0].get("id")
        print(f"\n  → First User ID: {user_id}")

    # 4. Enterprise Service Users
    print_section("GET /enterprise/members/service-users - List Enterprise Service Users")
    service_users_response = client.get("/enterprise/members/service-users")
    print_response(service_users_response)

    # 5. Sessions (requires org_id)
    if org_id:
        print_section(f"GET /organizations/{org_id}/sessions - List Sessions")
        sessions_response = client.get(f"/organizations/{org_id}/sessions")
        sessions_data = print_response(sessions_response)

        session_id = None
        if sessions_data and "items" in sessions_data and sessions_data["items"]:
            session_id = sessions_data["items"][0].get("session_id") or sessions_data["items"][0].get("id")
            print(f"\n  → First Session ID: {session_id}")

    # 6. Audit Logs
    print_section("GET /enterprise/audit-logs - List Audit Logs")
    audit_response = client.get("/enterprise/audit-logs", params={"limit": 5})
    print_response(audit_response)

    # 7. Consumption Cycles
    print_section("GET /enterprise/consumption/cycles - List Consumption Cycles")
    consumption_response = client.get("/enterprise/consumption/cycles")
    print_response(consumption_response)

    # 8. Enterprise Playbooks
    print_section("GET /enterprise/playbooks - List Enterprise Playbooks")
    playbooks_response = client.get("/enterprise/playbooks")
    print_response(playbooks_response)

    # 9. Enterprise Knowledge Notes
    print_section("GET /enterprise/knowledge/notes - List Enterprise Knowledge Notes")
    notes_response = client.get("/enterprise/knowledge/notes")
    print_response(notes_response)

    # 10. Enterprise Metrics
    print_section("GET /enterprise/metrics/usage - Get Usage Metrics")
    metrics_response = client.get("/enterprise/metrics/usage")
    print_response(metrics_response)

    # 11. IDP Groups
    print_section("GET /enterprise/members/idp-groups - List Enterprise IDP Groups")
    idp_response = client.get("/enterprise/members/idp-groups")
    print_response(idp_response)

    # 12. Roles
    print_section("GET /enterprise/roles - List Enterprise Roles")
    roles_response = client.get("/enterprise/roles")
    print_response(roles_response)

    # 13. Hypervisors
    print_section("GET /enterprise/hypervisors - List Hypervisors")
    hypervisors_response = client.get("/enterprise/hypervisors")
    print_response(hypervisors_response)

    # 14. Git Connections
    print_section("GET /enterprise/git-connections - List Git Connections")
    git_conn_response = client.get("/enterprise/git-connections")
    print_response(git_conn_response)

    # 15. Git Permissions
    print_section("GET /enterprise/git-permissions - List Git Permissions")
    git_perm_response = client.get("/enterprise/git-permissions")
    print_response(git_perm_response)

    # 16. Organization-level endpoints (if org_id available)
    if org_id:
        print_section(f"GET /enterprise/organizations/{org_id}/members/users - List Organization Users")
        org_users_response = client.get(f"/enterprise/organizations/{org_id}/members/users")
        print_response(org_users_response)

        print_section(f"GET /organizations/{org_id}/playbooks - List Organization Playbooks")
        org_playbooks_response = client.get(f"/organizations/{org_id}/playbooks")
        print_response(org_playbooks_response)

        print_section(f"GET /enterprise/organizations/{org_id}/tags - Get Organization Tags")
        tags_response = client.get(f"/enterprise/organizations/{org_id}/tags")
        print_response(tags_response)

    print_section("API Demo Complete")
    print("All API endpoints have been called successfully!")


if __name__ == "__main__":
    main()

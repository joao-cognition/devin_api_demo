"""API validation tests using functions from scripts."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from self.run_self import get_self
from organizations.run_organizations import list_organizations
from users.run_users import list_enterprise_users, list_org_users
from sessions.run_sessions import list_sessions
from service_users.run_service_users import list_service_users
from playbooks.run_playbooks import list_enterprise_playbooks, list_org_playbooks
from tags.run_tags import get_tags


def test_get_self(api_client):
    r = get_self(api_client)
    assert r.status_code == 200


def test_list_organizations(api_client):
    r = list_organizations(api_client)
    assert r.status_code == 200
    assert "items" in r.json()


def test_list_enterprise_users(api_client):
    r = list_enterprise_users(api_client)
    assert r.status_code == 200


def test_list_org_users(api_client, org_id):
    r = list_org_users(api_client, org_id)
    assert r.status_code == 200


def test_list_sessions(api_client, org_id):
    r = list_sessions(api_client, org_id)
    assert r.status_code == 200


def test_list_service_users(api_client):
    r = list_service_users(api_client)
    assert r.status_code == 200


def test_list_enterprise_playbooks(api_client):
    r = list_enterprise_playbooks(api_client)
    assert r.status_code == 200


def test_list_org_playbooks(api_client, org_id):
    r = list_org_playbooks(api_client, org_id)
    assert r.status_code == 200


def test_get_tags(api_client, org_id):
    r = get_tags(api_client, org_id)
    assert r.status_code in [200, 403]


def test_knowledge_notes(api_client):
    r = api_client.get("/enterprise/knowledge/notes")
    assert r.status_code == 200


def test_knowledge_notes_org(api_client, org_id):
    r = api_client.get(f"/organizations/{org_id}/knowledge/notes")
    assert r.status_code == 200


def test_audit_logs(api_client):
    r = api_client.get("/enterprise/audit-logs")
    assert r.status_code == 200


def test_consumption_cycles(api_client):
    r = api_client.get("/enterprise/consumption/cycles")
    assert r.status_code == 200


def test_metrics(api_client):
    r = api_client.get("/enterprise/metrics/usage")
    assert r.status_code == 200


def test_roles(api_client):
    r = api_client.get("/enterprise/roles")
    assert r.status_code in [200, 404]


def test_idp_groups(api_client):
    r = api_client.get("/enterprise/members/idp-groups")
    assert r.status_code == 200


def test_hypervisors(api_client):
    r = api_client.get("/enterprise/hypervisors")
    assert r.status_code in [200, 404]


def test_git_connections(api_client):
    r = api_client.get("/enterprise/git-connections")
    assert r.status_code in [200, 404]


def test_git_permissions(api_client, org_id):
    r = api_client.get(f"/organizations/{org_id}/git-providers/github/permissions")
    assert r.status_code in [200, 404]

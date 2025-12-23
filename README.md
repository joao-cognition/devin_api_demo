# Devin API Demo

Standalone Python scripts for interacting with the Devin API v3.

## Quick Start

```bash
# 1. Clone and setup
git clone <repo>
cd devin_api_demo
python3 -m venv venv
source venv/bin/activate
pip install -e .

# 2. Add your API key
echo "DEVIN_API_KEY=your_key_here" > .env

# 3. Run a script
python scripts/self/run_self.py
```

## Available Scripts

Each script is standalone and can be run directly:

| Script | Commands | Description |
|--------|----------|-------------|
| `scripts/self/run_self.py` | (none) | Get authenticated user info |
| `scripts/organizations/run_organizations.py` | `list`, `create <name>`, `update <id> <name>`, `delete <id>` | Manage organizations |
| `scripts/users/run_users.py` | `list`, `list-org`, `add <email>`, `remove <id>` | Manage users |
| `scripts/sessions/run_sessions.py` | `list`, `create <prompt>`, `terminate <id>`, `archive <id>` | Manage sessions |
| `scripts/service_users/run_service_users.py` | `list`, `create <name>`, `delete <id>` | Manage service users |
| `scripts/playbooks/run_playbooks.py` | `list`, `list-org`, `create <name> <body>` | Manage playbooks |
| `scripts/tags/run_tags.py` | `get`, `add <tags...>`, `replace <tags...>`, `delete <tag>` | Manage tags |
| `scripts/knowledge_notes/run_knowledge_notes.py` | `list`, `create <name> <body>`, `list-org`, `create-org` | Manage knowledge notes |
| `scripts/audit_logs/run_audit_logs.py` | `list`, `list-org` | View audit logs |
| `scripts/consumption/run_consumption.py` | `cycles`, `daily`, `by-org`, `by-user`, `by-session` | View consumption |
| `scripts/metrics/run_metrics.py` | `enterprise`, `org` | View metrics |
| `scripts/idp_groups/run_idp_groups.py` | `list`, `add <group_id>`, `list-org`, `add-org` | Manage IDP groups |
| `scripts/git_permissions/run_git_permissions.py` | `list`, `add`, `remove` | Manage git permissions |
| `scripts/roles/run_roles.py` | `list` | List roles |
| `scripts/hypervisors/run_hypervisors.py` | `list` | List hypervisors |
| `scripts/git_connections/run_git_connections.py` | `list` | List git connections |
| `scripts/run_all_apis.py` | (none) | Run all list endpoints |

## Examples

```bash
# List all organizations
python scripts/organizations/run_organizations.py list

# Create a new session
python scripts/sessions/run_sessions.py create "Fix the bug in main.py"

# Add tags to an organization
python scripts/tags/run_tags.py add "frontend" "backend" "urgent"

# View consumption cycles
python scripts/consumption/run_consumption.py cycles

# Run all endpoints at once
python scripts/run_all_apis.py
```

## Run Tests

```bash
pytest
```

## Project Structure

```
devin_api_demo/
├── scripts/           # 17 standalone API scripts
│   ├── self/
│   ├── organizations/
│   ├── users/
│   ├── sessions/
│   ├── ...
│   └── run_all_apis.py
├── src/devin_api_client/  # API client library
│   ├── client.py
│   └── config.py
├── tests/             # API validation tests
├── .env               # Your API key (create this)
└── pyproject.toml     # Project config
```

## Troubleshooting

**ModuleNotFoundError: No module named 'devin_api_client'**
→ Run `pip install -e .` in the project root

**ValueError: DEVIN_API_KEY environment variable is required**
→ Create `.env` file with `DEVIN_API_KEY=your_key_here`

**401/403 errors**
→ Check your API key is valid and has required permissions

## License

MIT

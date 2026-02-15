# Installation & Configuration

This page covers the full workflow for managing MCP server configurations with the DevSync CLI: creating a config repository, installing it, configuring credentials, and syncing to your AI tools.

---

## Workflow Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Create MCP     │────>│  Install to      │────>│  Configure      │────>│  Sync to AI     │
│  config repo    │     │  local library   │     │  credentials    │     │  tools          │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
   templatekit.yaml      devsync mcp install     devsync mcp configure   devsync mcp sync
```

## Step 1: Create an MCP Config Repository

An MCP config repository is a Git repo containing a `templatekit.yaml` file that defines your MCP servers.

### Minimal Example

```yaml title="templatekit.yaml"
name: Backend Servers
version: 1.0.0
description: MCP servers for backend development

mcp_servers:
  - name: github
    command: uvx
    args: [mcp-server-github]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: null  # (1)!
```

1. `null` means this credential is required -- the user must configure it before syncing.

### Full Example

```yaml title="templatekit.yaml"
name: Backend Development Servers
version: 2.1.0
description: MCP servers for the backend team
author: Backend Team <backend@example.com>

mcp_servers:
  - name: github
    command: uvx
    args: [mcp-server-github]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: null
    tags: [github, scm]

  - name: postgres
    command: python
    args: [-m, mcp_server_postgres]
    env:
      DATABASE_URL: null
      DATABASE_POOL_SIZE: "10"  # (1)!
    tags: [database]

  - name: filesystem
    command: npx
    args: [-y, "@modelcontextprotocol/server-filesystem", "/workspace"]
    env: {}  # (2)!
    tags: [filesystem]

  - name: slack
    command: python
    args: [-m, mcp_server_slack]
    env:
      SLACK_BOT_TOKEN: null
      SLACK_SIGNING_SECRET: null
    tags: [communication]

mcp_sets:
  - name: backend-dev
    description: Core servers for backend work
    servers: [github, postgres, filesystem]

  - name: full-stack
    description: Everything including communication
    servers: [github, postgres, filesystem, slack]
```

1. A string value provides a default. The user can override it during configuration.
2. Empty `env` means no credentials are needed.

### Field Reference

**mcp_servers**

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `name` | `string` | Yes | Unique server identifier |
| `command` | `string` | Yes | Executable to launch the server (`uvx`, `npx`, `python`) |
| `args` | `list[string]` | Yes | Command-line arguments |
| `env` | `dict` | No | Environment variables. `null` = required credential, string = default value |
| `tags` | `list[string]` | No | Organizational tags |

**mcp_sets**

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `name` | `string` | Yes | Set identifier |
| `description` | `string` | No | Human-readable description |
| `servers` | `list[string]` | Yes | Server names to include |
| `tags` | `list[string]` | No | Organizational tags |

## Step 2: Install to Local Library

```bash
# Install from a Git repository
devsync mcp install https://github.com/acme/mcp-servers --as backend

# Install from a specific branch or tag
devsync mcp install https://github.com/acme/mcp-servers --as backend --ref v2.0.0

# Install from a local directory
devsync mcp install ./my-mcp-servers --as backend

# Force reinstall (overwrite existing)
devsync mcp install https://github.com/acme/mcp-servers --as backend --force
```

The `--as` flag sets the namespace. Servers are referenced as `<namespace>.<server>` (e.g., `backend.github`, `backend.postgres`).

### Scopes

| Scope | Library Location | Credentials Location | Use Case |
|-------|-----------------|---------------------|----------|
| **Project** (default) | `~/.devsync/library/` | `.devsync/.env` | Project-specific servers |
| **Global** | `~/.devsync/library/global/` | `~/.devsync/global/.env` | Personal or company-wide servers |

```bash
# Install at global scope
devsync mcp install https://github.com/acme/mcp-servers --as company --scope global
```

When syncing, project credentials take precedence over global credentials for the same variable.

## Step 3: Configure Credentials

### Interactive Mode

```bash
# Configure all servers in a namespace
devsync mcp configure backend

# Configure a specific server
devsync mcp configure backend.github
```

The CLI prompts for each required credential:

```
Configuring MCP server: backend.github
Required environment variables: 1

Enter value for GITHUB_PERSONAL_ACCESS_TOKEN:
  GITHUB_PERSONAL_ACCESS_TOKEN: ****

Credentials saved to: /home/dev/my-project/.devsync/.env
(This file is automatically gitignored)
```

### Non-Interactive Mode

For CI/CD or scripted setups:

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxx
export DATABASE_URL=postgresql://localhost/mydb
devsync mcp configure backend --non-interactive
```

### Viewing Current Credentials

```bash
devsync mcp configure backend.github --show-current
```

Output shows masked values:

```
Current Credentials (project scope)
Server              Variable                         Value          Status
backend.github      GITHUB_PERSONAL_ACCESS_TOKEN     ****abc123     configured
```

### Where Credentials Are Stored

Credentials are written to `.devsync/.env` in the project root:

```text title=".devsync/.env"
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxx
DATABASE_URL=postgresql://user:pass@localhost/mydb
SLACK_BOT_TOKEN=xoxb-xxxxx
```

!!! warning "Gitignore"
    DevSync automatically adds `.devsync/.env` to your `.gitignore`. Verify this is in place before committing:

    ```bash
    git status
    # .devsync/.env should NOT appear in untracked files
    ```

!!! danger "Never commit credentials"
    Do not put credential values in `templatekit.yaml`. Use `null` for required credentials and let each developer configure their own values locally.

## Step 4: Sync to AI Tools

```bash
# Sync to all detected AI tools
devsync mcp sync --tool all

# Sync to a specific tool
devsync mcp sync --tool claude
devsync mcp sync --tool cursor
devsync mcp sync --tool windsurf
```

Output:

```
Syncing MCP servers to AI tools
Scope: project
Tools: all

Synced to 3 tool(s):
  claude, cursor, copilot

Server Summary:
  Synced: 3 server(s)
  Skipped: 1 server(s)

Skipped Servers:
  backend.postgres -- Missing credentials: DATABASE_URL

Tip: Run 'devsync mcp configure backend' to configure missing credentials
```

### Dry Run

Preview changes without writing any files:

```bash
devsync mcp sync --tool all --dry-run
```

### Skip Backup

By default, DevSync backs up existing config files before modifying them. To skip:

```bash
devsync mcp sync --tool all --no-backup
```

See [Backups & Recovery](backups-and-recovery.md) for more on the backup system.

## Managing Installed Servers

### List

```bash
# List all installed MCP templates
devsync mcp list

# Filter by namespace
devsync mcp list backend

# JSON output
devsync mcp list --json
```

### Update

```bash
# Update a specific namespace (pulls latest from Git)
devsync mcp update backend

# Update all
devsync mcp update --all
```

Updates pull latest changes from the source repository. Your local credentials are preserved.

### Uninstall

```bash
devsync mcp uninstall backend
```

This removes the template from your library. It does not remove credentials or already-synced configurations from AI tools.

### Validate

```bash
# Check if all required credentials are configured
devsync mcp validate
devsync mcp validate backend
```

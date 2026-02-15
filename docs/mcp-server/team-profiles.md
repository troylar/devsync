# Team Profiles

Team profiles let you define standardized configurations that apply across an entire team or organization. A `devsync-profile.yaml` file specifies which templates, MCP servers, packages, and settings each role should use.

!!! note "Forward-looking feature"
    Team profiles are in the design phase. The schema and commands described here represent the planned direction. Implementation details may change.

---

## The Problem

As teams scale, configuration management becomes fragmented:

- Different developers install different subsets of instructions
- New hires miss critical MCP server configs
- Roles with different needs (backend, frontend, SRE) need different tool setups
- There is no single source of truth for "what should a backend developer have installed?"

## The Solution

A `devsync-profile.yaml` file in your team's config repository defines roles and their required configurations. DevSync reads this profile and installs everything a developer needs based on their role.

```bash
# Apply a team profile
devsync profile apply --role backend

# Check compliance with your profile
devsync profile check
```

---

## Profile Schema

```yaml title="devsync-profile.yaml"
name: Acme Engineering
version: 1.0.0
description: Standard development configurations for Acme Corp

defaults:
  templates:
    - repo: https://github.com/acme/coding-standards
      namespace: acme
  mcp_servers:
    - repo: https://github.com/acme/mcp-shared
      namespace: shared
  packages:
    - repo: https://github.com/acme/base-package

roles:
  backend:
    description: Backend engineers working on APIs and services
    extends: []
    templates:
      - repo: https://github.com/acme/backend-standards
        namespace: backend
    mcp_servers:
      - repo: https://github.com/acme/mcp-backend
        namespace: backend
        servers: [postgres, redis, github]
    packages:
      - repo: https://github.com/acme/python-dev-setup

  frontend:
    description: Frontend engineers working on web applications
    extends: []
    templates:
      - repo: https://github.com/acme/frontend-standards
        namespace: frontend
    mcp_servers:
      - repo: https://github.com/acme/mcp-frontend
        namespace: frontend
        servers: [github, figma, storybook]

  sre:
    description: Site reliability engineers
    extends: [backend]
    templates:
      - repo: https://github.com/acme/sre-standards
        namespace: sre
    mcp_servers:
      - repo: https://github.com/acme/mcp-infra
        namespace: infra
        servers: [aws, terraform, datadog]

settings:
  require_mcp_credentials: true
  auto_sync_on_install: true
  backup_before_apply: true
```

### Schema Reference

**Top-level fields**

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `name` | `string` | Yes | Organization or team name |
| `version` | `string` | Yes | Profile version (semver) |
| `description` | `string` | No | What this profile covers |
| `defaults` | `object` | No | Configurations applied to all roles |
| `roles` | `object` | Yes | Role definitions (keyed by role name) |
| `settings` | `object` | No | Profile-wide settings |

**Role fields**

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `description` | `string` | No | What this role is for |
| `extends` | `list[string]` | No | Other roles to inherit from |
| `templates` | `list[object]` | No | Template repositories to install |
| `mcp_servers` | `list[object]` | No | MCP server repositories and selected servers |
| `packages` | `list[object]` | No | Packages to install |

---

## Planned Commands

```bash
# Apply a profile to the current project
devsync profile apply --role backend

# Apply from a specific profile file
devsync profile apply --role backend --profile ./devsync-profile.yaml

# Check if current project matches the profile
devsync profile check

# Check a specific role
devsync profile check --role sre

# List available roles
devsync profile roles
```

### Example: Applying a Profile

```
$ devsync profile apply --role backend

Applying profile: Acme Engineering v1.0.0
Role: backend

Installing defaults...
  Template: acme/coding-standards -> namespace 'acme'
  MCP: acme/mcp-shared -> namespace 'shared'
  Package: acme/base-package

Installing role-specific configs...
  Template: acme/backend-standards -> namespace 'backend'
  MCP: acme/mcp-backend -> namespace 'backend' (postgres, redis, github)
  Package: acme/python-dev-setup

Configure credentials:
  3 MCP servers require credentials
  Run: devsync mcp configure backend

Applied 3 templates, 4 MCP servers, 2 packages
```

---

## Inheritance

Roles can extend other roles using the `extends` field. The SRE role in the example above extends `backend`, meaning an SRE gets everything a backend developer gets, plus SRE-specific additions.

Inheritance is additive. If the same namespace appears in both a parent and child role, the child's definition takes precedence.

# Onboard a New Developer

**Time to complete**: 15 minutes
**Difficulty**: Beginner
**Prerequisites**:

- Python 3.10+ installed
- Git configured with access to your organization's repositories
- At least one AI coding assistant installed (Claude Code, Cursor, Windsurf, etc.)

## The Scenario

A new developer is joining your team. They need their AI coding assistants configured with:

- **Company-wide standards** that apply to every project (global scope)
- **Project-specific templates** for the codebase they will work on
- **MCP server configurations** for shared tooling (GitHub, database access, etc.)

This tutorial walks through the complete setup from a clean machine to a fully configured development environment.

## What You Will Learn

- How to install and verify DevSync
- How to detect which AI tools are available
- How to install global and project-scoped templates
- How to install and configure MCP servers
- How to verify the complete setup

---

## Step 1: Install DevSync

Install DevSync from PyPI:

```bash
pip install devsync
```

Verify the installation:

```bash
devsync --version
```

!!! tip "Virtual environments"
    If your organization uses virtual environments or `pipx`, adjust accordingly:

    ```bash
    # With pipx (recommended for CLI tools)
    pipx install devsync

    # With a virtual environment
    python -m venv ~/.venvs/devsync
    ~/.venvs/devsync/bin/pip install devsync
    alias devsync="~/.venvs/devsync/bin/devsync"
    ```

---

## Step 2: Check Detected AI Tools

DevSync auto-detects which AI coding assistants are installed on your machine. Run:

```bash
devsync tools
```

Expected output (varies by machine):

```
Detected AI Tools:

Tool              Status     Install Path
Claude Code       detected   .claude/rules/
Cursor            detected   .cursor/rules/
Windsurf          detected   .windsurf/rules/
GitHub Copilot    detected   .github/instructions/
Cline             not found
Roo Code          not found
Codex CLI         not found
Kiro              not found

4 tool(s) detected.
```

!!! note "At least one tool required"
    DevSync needs at least one detected tool to install configurations. If no tools appear, install one of the supported AI coding assistants first.

---

## Step 3: Install Company-Wide Global Standards

Global standards apply to every project on your machine. These typically include company coding conventions, security policies, and communication guidelines.

```bash
devsync template install https://github.com/your-company/global-standards --as company --scope global
```

Expected output:

```
Installing templates from https://github.com/your-company/global-standards...
Namespace: company
Scope: global

Installed:
  company.coding-conventions  -> ~/.claude/rules/company.coding-conventions.md
  company.security-policy     -> ~/.claude/rules/company.security-policy.md
  company.commit-standards    -> ~/.claude/rules/company.commit-standards.md

3 templates installed to global scope.
```

The `--scope global` flag installs templates to your home directory (`~/.claude/rules/`) rather than a specific project. This means these standards are active in every project you open.

Verify the global installation:

```bash
devsync template list
```

```
Installed Templates:

Namespace   Name                   Type         Scope    Source
company     coding-conventions     instruction  global   github.com/your-company/global-standards
company     security-policy        instruction  global   github.com/your-company/global-standards
company     commit-standards       instruction  global   github.com/your-company/global-standards
```

---

## Step 4: Clone the Project Repository

Clone the project you will be working on:

```bash
cd ~/projects
git clone https://github.com/your-company/backend-api
cd backend-api
```

---

## Step 5: Install Project-Specific Templates

Project-specific templates contain conventions unique to this codebase: API design patterns, database conventions, deployment procedures, and so on.

```bash
devsync template install https://github.com/your-company/backend-templates --as backend
```

Expected output:

```
Installing templates from https://github.com/your-company/backend-templates...
Namespace: backend

Installed:
  backend.api-design        -> .claude/rules/backend.api-design.md
  backend.database-patterns -> .claude/rules/backend.database-patterns.md
  backend.review-pr         -> .claude/commands/backend.review-pr.md
  backend.run-migrations    -> .claude/commands/backend.run-migrations.md

4 templates installed successfully.
```

!!! info "Project scope is the default"
    Without `--scope global`, templates install at the project level. They are stored in the project's `.claude/rules/` and `.claude/commands/` directories, scoped to that project only.

---

## Step 6: Install MCP Server Configurations

MCP (Model Context Protocol) servers extend your AI assistant with additional capabilities like GitHub API access, database queries, or file system operations. Your team distributes MCP configurations via Git, and DevSync handles installation and credential management.

```bash
devsync mcp install https://github.com/your-company/mcp-servers --as team-mcp
```

Expected output:

```
Installing MCP template from https://github.com/your-company/mcp-servers...
Namespace: team-mcp

MCP servers found:
  team-mcp.github       (requires: GITHUB_PERSONAL_ACCESS_TOKEN)
  team-mcp.postgres     (requires: DATABASE_URL)
  team-mcp.filesystem   (no credentials required)

3 MCP server(s) installed.

Next step: Configure credentials with 'devsync mcp configure team-mcp'
```

---

## Step 7: Configure MCP Credentials

MCP servers that access external services need credentials. DevSync prompts for each one interactively and stores them in a gitignored `.env` file.

```bash
devsync mcp configure team-mcp
```

Interactive prompts:

```
Configuring MCP servers for namespace: team-mcp

--- team-mcp.github ---
Required: GITHUB_PERSONAL_ACCESS_TOKEN
  Description: GitHub personal access token with repo scope
  Enter value: ****

--- team-mcp.postgres ---
Required: DATABASE_URL
  Description: PostgreSQL connection string for the development database
  Enter value: ****

--- team-mcp.filesystem ---
No credentials required.

Credentials saved to: /Users/you/projects/backend-api/.devsync/.env
(This file is automatically gitignored)

3/3 servers configured.
```

!!! warning "Never commit credentials"
    DevSync automatically adds `.devsync/.env` to `.gitignore`. Verify this by running `git status` -- the `.env` file should not appear as an untracked file. If it does, add it to `.gitignore` manually before committing anything.

To verify credentials were saved (values are masked):

```bash
devsync mcp configure team-mcp --show-current
```

```
Current Credentials (project scope)

Server                Variable                          Value          Status
team-mcp.github       GITHUB_PERSONAL_ACCESS_TOKEN      ****abc123     configured
team-mcp.postgres     DATABASE_URL                      ****mydb       configured
team-mcp.filesystem   (none required)                   --             ready
```

---

## Step 8: Sync MCP to AI Tools

With credentials configured, sync the MCP server definitions to all detected AI tools:

```bash
devsync mcp sync --tool all
```

Expected output:

```
Syncing MCP servers to AI tools...
Scope: project
Tools: all

Synced to 2 tool(s):
  claude  -- 3 server(s) written to claude_desktop_config.json
  cursor  -- 3 server(s) written to mcp_config.json

Server Summary:
  Synced: 3 server(s)
  Skipped: 0 server(s)
```

To sync to a single tool:

```bash
devsync mcp sync --tool claude
```

!!! tip "Dry run"
    Preview what would be written without making changes:

    ```bash
    devsync mcp sync --tool all --dry-run
    ```

---

## Step 9: Verify Everything

Run a series of checks to confirm the setup is complete.

### Check installed templates

```bash
devsync template list
```

Expected output:

```
Installed Templates:

Namespace   Name                   Type         Scope    Source
company     coding-conventions     instruction  global   github.com/your-company/global-standards
company     security-policy        instruction  global   github.com/your-company/global-standards
company     commit-standards       instruction  global   github.com/your-company/global-standards
backend     api-design             instruction  project  github.com/your-company/backend-templates
backend     database-patterns      instruction  project  github.com/your-company/backend-templates
backend     review-pr              command      project  github.com/your-company/backend-templates
backend     run-migrations         command      project  github.com/your-company/backend-templates
```

### Check installed packages (if any)

```bash
devsync list installed
```

### Check MCP server status

```bash
devsync mcp list
```

### Check project file structure

```bash
ls -la .claude/rules/
ls -la .claude/commands/
```

Expected files:

```
.claude/rules/
  backend.api-design.md
  backend.database-patterns.md

.claude/commands/
  backend.review-pr.md
  backend.run-migrations.md
```

Global templates are in `~/.claude/rules/`:

```bash
ls -la ~/.claude/rules/
```

```
~/.claude/rules/
  company.coding-conventions.md
  company.security-policy.md
  company.commit-standards.md
```

---

## Complete Onboarding Script

For organizations that onboard developers frequently, combine all steps into a script:

```bash
#!/usr/bin/env bash
set -e

echo "=== DevSync Developer Onboarding ==="

# Step 1: Install DevSync
pip install --upgrade devsync

# Step 2: Show detected tools
echo ""
echo "--- Detected AI Tools ---"
devsync tools

# Step 3: Install global standards
echo ""
echo "--- Installing company-wide standards ---"
devsync template install https://github.com/your-company/global-standards \
  --as company --scope global --force

# Step 4: Project setup (run from within the project directory)
echo ""
echo "--- Installing project templates ---"
devsync template install https://github.com/your-company/backend-templates \
  --as backend --force

# Step 5: Install MCP servers
echo ""
echo "--- Installing MCP servers ---"
devsync mcp install https://github.com/your-company/mcp-servers \
  --as team-mcp --force

# Step 6: Configure credentials (interactive)
echo ""
echo "--- Configuring MCP credentials ---"
devsync mcp configure team-mcp

# Step 7: Sync MCP to tools
echo ""
echo "--- Syncing MCP to AI tools ---"
devsync mcp sync --tool all

# Step 8: Verify
echo ""
echo "--- Verification ---"
devsync template list
devsync mcp list

echo ""
echo "=== Onboarding complete ==="
```

Save this as `scripts/onboard.sh` in your project repository and add it to your onboarding documentation.

---

## Troubleshooting

### "No AI tools detected"

Install at least one supported AI coding assistant. Run `devsync tools` after installation to confirm detection.

### "Template namespace already exists"

The developer may have a partial installation from a previous attempt. Use `--force` to overwrite:

```bash
devsync template install <url> --as <namespace> --force
```

### "Missing credentials" when syncing MCP

One or more MCP servers need credentials that have not been configured. Run:

```bash
devsync mcp configure <namespace>
```

This prompts for any unconfigured values.

### Credentials file appears in `git status`

The `.devsync/.env` file should be gitignored automatically. If it appears as untracked:

```bash
echo ".devsync/.env" >> .gitignore
git add .gitignore
git commit -m "chore: gitignore devsync credentials"
```

### Templates not taking effect in AI assistant

Some AI tools require a restart to pick up new configuration files. Close and reopen your IDE or restart the AI assistant process.

---

## Next Steps

- [Create a Team Configuration Repository](team-config-repo.md) -- Set up and maintain your own template repository
- [Build and Distribute a Custom Package](custom-packages.md) -- Bundle instructions, MCP servers, hooks, and more
- [AI-Assisted Configuration Merging](ai-merge-workflow.md) -- Use AI to manage configuration drift

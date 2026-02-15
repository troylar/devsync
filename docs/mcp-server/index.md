# MCP Server Management

DevSync provides two distinct MCP capabilities:

1. **MCP Configuration Management** -- The DevSync CLI distributes and syncs MCP server configurations across 15+ AI tools for your entire team.
2. **devsync-mcp** -- A separate MCP server package (`pip install devsync-mcp`) that gives AI assistants direct access to DevSync operations for intelligent config merging.

This section covers both.

---

## What Is MCP?

Model Context Protocol (MCP) is an open standard that lets AI coding assistants connect to external tools and data sources. An MCP server exposes capabilities -- database queries, API calls, file operations -- that the AI can invoke during a conversation.

The problem: every AI tool stores MCP configurations differently. Claude Code uses `.claude/settings.local.json`. Cursor uses `.cursor/mcp.json`. Windsurf uses `~/.codeium/windsurf/mcp_config.json`. When your team uses multiple tools, keeping MCP configs in sync becomes a maintenance burden.

## Why Managed MCP Configs Matter

Without centralized management:

- Team members manually edit tool-specific JSON files
- Credentials end up committed to Git
- Configuration drift accumulates across machines
- Onboarding requires documenting 15 different config file locations
- Updating a server version means touching every developer's setup

With DevSync:

```bash
# Share MCP configs via Git (no credentials in repo)
devsync mcp install https://github.com/acme/mcp-servers --as backend

# Each developer configures their own credentials locally
devsync mcp configure backend

# Sync to all detected AI tools at once
devsync mcp sync --tool all
```

Credentials stay in `.devsync/.env` (gitignored). Configurations propagate to every supported tool with a single command.

## Supported IDEs

DevSync can sync MCP server configurations to these AI tools:

| IDE | Config Location | Tool Limit |
|-----|----------------|:----------:|
| Amazon Q | `.amazonq/mcp.json` | -- |
| Antigravity | `.mcp.json` | -- |
| Augment | `.augment/mcp.json` | -- |
| Claude Code | `.claude/settings.local.json` | -- |
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` | -- |
| Continue.dev | `.continue/config.json` | -- |
| Cursor | `.cursor/mcp.json` | 40 |
| Gemini CLI | `~/.gemini/settings.json` | -- |
| GitHub Copilot | `.vscode/mcp.json` | 128 |
| JetBrains AI | `.aiassistant/mcp.json` | -- |
| OpenHands | `.openhands/mcp.json` | -- |
| Tabnine | `.tabnine/mcp.json` | -- |
| Trae | `.mcp.json` | -- |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` | 100 |
| Zed | `.zed/settings.json` | -- |

See [IDE Setup](ide-setup.md) for per-tool configuration details.

## The devsync-mcp Package

`devsync-mcp` is a separate package that exposes DevSync operations as MCP tools. This allows AI assistants to directly read, compare, and merge configurations during a conversation.

```bash
pip install devsync-mcp
```

This is useful for AI-assisted workflows where the assistant needs to understand your current config state, detect conflicts, and propose intelligent merges. See [Tools Reference](tools-reference.md) and [AI Merge Flow](ai-merge-flow.md) for details.

!!! note "Separate package"
    `devsync-mcp` is installed independently from the main `devsync` CLI. You need the CLI for config management commands. You need `devsync-mcp` only if you want AI assistants to interact with DevSync programmatically.

## Documentation Map

| Page | What It Covers |
|------|---------------|
| [Installation & Configuration](installation.md) | Installing MCP repos, configuring credentials, syncing to tools |
| [IDE Setup](ide-setup.md) | Per-IDE config file locations and JSON formats |
| [Tools Reference](tools-reference.md) | The devsync-mcp package's MCP tool APIs |
| [Team Profiles](team-profiles.md) | Defining team-wide configurations with `devsync-profile.yaml` |
| [AI Merge Flow](ai-merge-flow.md) | Using AI assistants to intelligently merge config changes |
| [Backups & Recovery](backups-and-recovery.md) | Automatic backups, restore, and cleanup |

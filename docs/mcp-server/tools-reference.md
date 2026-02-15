# devsync-mcp Tools Reference

`devsync-mcp` is a separate Python package that exposes DevSync operations as MCP tools. AI assistants connected to this server can read your current configurations, detect conflicts, and perform intelligent merges.

```bash
pip install devsync-mcp
```

!!! info "Early-stage package"
    `devsync-mcp` is under active development. The tools listed below represent the planned API surface. Specific parameter names, return types, and behavior may change as the package matures. This reference will be updated as the API stabilizes.

---

## Server Configuration

Register `devsync-mcp` with your AI tool like any other MCP server.

=== "Claude Code"

    ```json title=".claude/settings.local.json"
    {
      "mcpServers": {
        "devsync": {
          "command": "uvx",
          "args": ["devsync-mcp"],
          "env": {}
        }
      }
    }
    ```

=== "Cursor"

    ```json title=".cursor/mcp.json"
    {
      "mcpServers": {
        "devsync": {
          "command": "uvx",
          "args": ["devsync-mcp"],
          "env": {}
        }
      }
    }
    ```

=== "Claude Desktop"

    ```json title="claude_desktop_config.json"
    {
      "mcpServers": {
        "devsync": {
          "command": "uvx",
          "args": ["devsync-mcp"],
          "env": {}
        }
      }
    }
    ```

---

## Available Tools

### `devsync_read_config`

Read the current DevSync configuration for a project.

**Parameters:**

| Name | Type | Required | Description |
|------|------|:--------:|-------------|
| `project_path` | `string` | Yes | Path to the project root |
| `scope` | `string` | No | `"project"` or `"global"`. Default: `"project"` |

**Returns:** <!-- TODO: Document return schema when API is finalized -->

Project configuration including installed instructions, MCP servers, packages, and their current state.

---

### `devsync_list_instructions`

List all instructions available in the local library.

**Parameters:**

| Name | Type | Required | Description |
|------|------|:--------:|-------------|
| `namespace` | `string` | No | Filter by namespace |
| `tags` | `list[string]` | No | Filter by tags |

**Returns:** <!-- TODO: Document return schema when API is finalized -->

List of available instructions with metadata (name, description, tags, source repository).

---

### `devsync_compare_configs`

Compare current project configuration against incoming changes from a template or package.

**Parameters:**

| Name | Type | Required | Description |
|------|------|:--------:|-------------|
| `project_path` | `string` | Yes | Path to the project root |
| `source` | `string` | Yes | Template namespace or package path to compare against |
| `component_type` | `string` | No | Filter by component type: `"instructions"`, `"mcp"`, `"hooks"`, `"commands"` |

**Returns:** <!-- TODO: Document return schema when API is finalized -->

Diff-style comparison showing additions, removals, modifications, and conflicts.

---

### `devsync_merge_config`

Apply a merge strategy to resolve configuration differences.

**Parameters:**

| Name | Type | Required | Description |
|------|------|:--------:|-------------|
| `project_path` | `string` | Yes | Path to the project root |
| `source` | `string` | Yes | Template namespace or package path |
| `strategy` | `string` | No | `"skip"`, `"overwrite"`, or `"rename"`. Default: `"skip"` |
| `dry_run` | `boolean` | No | Preview changes without applying. Default: `false` |

**Returns:** <!-- TODO: Document return schema when API is finalized -->

Merge result including applied changes, skipped items, and any remaining conflicts.

---

### `devsync_list_mcp_servers`

List MCP server configurations from the local library.

**Parameters:**

| Name | Type | Required | Description |
|------|------|:--------:|-------------|
| `namespace` | `string` | No | Filter by namespace |
| `include_credentials` | `boolean` | No | Include credential status (configured/missing). Default: `false` |

**Returns:** <!-- TODO: Document return schema when API is finalized -->

List of MCP servers with their command, args, required credentials, and configuration status.

---

### `devsync_sync_status`

Check the sync status between library and installed configurations.

**Parameters:**

| Name | Type | Required | Description |
|------|------|:--------:|-------------|
| `project_path` | `string` | Yes | Path to the project root |
| `tool` | `string` | No | Specific AI tool to check, or `"all"` |

**Returns:** <!-- TODO: Document return schema when API is finalized -->

Per-tool sync status showing which servers are synced, outdated, or missing.

---

## Error Handling

All tools return structured errors with a `code` and `message` field when operations fail.

| Error Code | Meaning |
|-----------|---------|
| `PROJECT_NOT_FOUND` | The specified project path does not exist or has no DevSync configuration |
| `NAMESPACE_NOT_FOUND` | The requested namespace is not installed in the library |
| `CREDENTIALS_MISSING` | Required credentials have not been configured |
| `MERGE_CONFLICT` | Automatic merge failed and requires manual resolution |

<!-- TODO: Expand error codes as the API stabilizes -->

---

## Roadmap

Planned additions to the `devsync-mcp` tool surface:

- **`devsync_install_package`** -- Install a package directly from an AI conversation
- **`devsync_create_backup`** -- Trigger a manual backup of current configurations
- **`devsync_restore_backup`** -- Restore from a specific backup timestamp
- **`devsync_validate_manifest`** -- Validate a `templatekit.yaml` or `ai-config-kit-package.yaml` file

Check the [devsync-mcp changelog](https://github.com/troylar/devsync-mcp/releases) for the latest updates.

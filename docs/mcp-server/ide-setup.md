# IDE Setup for MCP

This page documents the MCP configuration file location and JSON format for each AI tool that DevSync supports. Use this as a reference when debugging sync issues or when you need to manually inspect tool configs.

After running `devsync mcp sync --tool <tool>`, DevSync writes to these files automatically. The formats shown here are what DevSync produces.

---

## IDE Configuration Reference

=== "Claude Code"

    **Config file:** `.claude/settings.local.json` (project-level)

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        },
        "postgres": {
          "command": "python",
          "args": ["-m", "mcp_server_postgres"],
          "env": {
            "DATABASE_URL": "postgresql://localhost/mydb"
          }
        }
      }
    }
    ```

    **Notes:**

    - Project-level file, lives in the repository root
    - No known tool limit
    - Supports all component types (instructions, MCP, hooks, commands, resources)

=== "Cursor"

    **Config file:** `.cursor/mcp.json` (project-level) or `~/.cursor/mcp.json` (global)

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        }
      }
    }
    ```

    **Notes:**

    - **Tool limit: 40 MCP servers**
    - Project-level config takes precedence over global
    - DevSync writes to the project-level file by default

=== "Windsurf"

    **Config file:** `~/.codeium/windsurf/mcp_config.json` (global)

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        }
      }
    }
    ```

    **Notes:**

    - **Tool limit: 100 MCP servers**
    - Global config only -- shared across all projects
    - Located in the Codeium application data directory

=== "GitHub Copilot"

    **Config file:** `.vscode/mcp.json` (project-level)

    ```json
    {
      "servers": {
        "github": {
          "type": "stdio",
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        }
      }
    }
    ```

    **Notes:**

    - **Tool limit: 128 MCP servers**
    - Uses `servers` key (not `mcpServers`)
    - Requires `type` field (typically `"stdio"`)
    - Shared with VS Code workspace settings directory

=== "Claude Desktop"

    **Config file:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

    Other platforms:

    - **Linux:** `~/.config/Claude/claude_desktop_config.json`
    - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        }
      }
    }
    ```

    **Notes:**

    - Global config, applies to all conversations
    - Requires restarting Claude Desktop after config changes

=== "Amazon Q"

    **Config file:** `.amazonq/mcp.json` (project-level)

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        }
      }
    }
    ```

=== "Augment"

    **Config file:** `.augment/mcp.json` (project-level)

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        }
      }
    }
    ```

=== "Continue.dev"

    **Config file:** `.continue/config.json` (project-level)

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        }
      }
    }
    ```

    **Notes:**

    - MCP servers are defined alongside other Continue.dev configuration
    - DevSync merges into the existing `config.json` without overwriting other settings

=== "Gemini CLI"

    **Config file:** `~/.gemini/settings.json` (global)

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        }
      }
    }
    ```

    **Notes:**

    - Global config, applies to all Gemini CLI sessions

=== "JetBrains AI"

    **Config file:** `.aiassistant/mcp.json` (project-level)

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        }
      }
    }
    ```

    **Notes:**

    - Works with all JetBrains IDEs (IntelliJ, PyCharm, WebStorm, etc.)

=== "OpenHands"

    **Config file:** `.openhands/mcp.json` (project-level)

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        }
      }
    }
    ```

=== "Tabnine"

    **Config file:** `.tabnine/mcp.json` (project-level)

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        }
      }
    }
    ```

=== "Trae"

    **Config file:** `.mcp.json` (project root)

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        }
      }
    }
    ```

    **Notes:**

    - Antigravity also uses `.mcp.json` at the project root
    - If both tools are in use, they share the same config file

=== "Antigravity"

    **Config file:** `.mcp.json` (project root)

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        }
      }
    }
    ```

    **Notes:**

    - Shares `.mcp.json` with Trae

=== "Zed"

    **Config file:** `.zed/settings.json` (project-level)

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "uvx",
          "args": ["mcp-server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
          }
        }
      }
    }
    ```

    **Notes:**

    - MCP config is nested within Zed's settings file
    - DevSync merges into existing settings without overwriting other Zed configuration

---

## Quick Reference Table

| IDE | Config File | Scope | Tool Limit |
|-----|------------|-------|:----------:|
| Amazon Q | `.amazonq/mcp.json` | Project | -- |
| Antigravity | `.mcp.json` | Project | -- |
| Augment | `.augment/mcp.json` | Project | -- |
| Claude Code | `.claude/settings.local.json` | Project | -- |
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` | Global | -- |
| Continue.dev | `.continue/config.json` | Project | -- |
| Cursor | `.cursor/mcp.json` | Project/Global | 40 |
| Gemini CLI | `~/.gemini/settings.json` | Global | -- |
| GitHub Copilot | `.vscode/mcp.json` | Project | 128 |
| JetBrains AI | `.aiassistant/mcp.json` | Project | -- |
| OpenHands | `.openhands/mcp.json` | Project | -- |
| Tabnine | `.tabnine/mcp.json` | Project | -- |
| Trae | `.mcp.json` | Project | -- |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` | Global | 100 |
| Zed | `.zed/settings.json` | Project | -- |

---

## Troubleshooting

### Config file not created

If `devsync mcp sync` reports success but the config file does not exist, DevSync may not have detected the tool. Run:

```bash
devsync tools
```

This lists which AI tools DevSync detects on your system. If your tool is missing, verify that it is installed and that its standard directories exist.

### Changes not taking effect

Some tools require a restart after MCP config changes:

- **Claude Desktop**: Restart the application
- **Cursor**: Reload the window (Cmd+Shift+P > "Reload Window")
- **VS Code / Copilot**: Reload the window
- **JetBrains**: Restart the IDE

### Tool limit exceeded

If you have more MCP servers than a tool supports (e.g., more than 40 for Cursor), DevSync will warn you during sync. Consider using MCP sets to install only the servers relevant to each project:

```bash
# Install only the backend-dev set
devsync mcp sync --tool cursor --set backend-dev
```

### Shared config files

Trae and Antigravity both use `.mcp.json` at the project root. Syncing to either tool writes to the same file. DevSync handles this by merging configurations rather than overwriting.

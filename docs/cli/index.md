# CLI Reference

DevSync provides the `devsync` command for managing AI coding assistant configurations across your projects.

## Usage

```
$ devsync <command> [options]
```

## Commands

### Core Workflow

| Command | Description |
|---------|-------------|
| [`download`](download.md) | Download instruction repositories to your local library |
| [`install`](install.md) | Install instructions to AI tools (interactive TUI or named) |
| [`uninstall`](uninstall.md) | Remove instructions from AI tools at project level |
| [`update`](update.md) | Update downloaded instructions to latest versions |
| [`delete`](delete.md) | Remove a source from your local library |

### Listing & Discovery

| Command | Description |
|---------|-------------|
| [`list available`](list.md#list-available) | List instructions from a remote source without downloading |
| [`list installed`](list.md#list-installed) | List instructions installed in your AI tools |
| [`list library`](list.md#list-library) | List sources and instructions in your local library |

### Template Management

| Command | Description |
|---------|-------------|
| `template init` | Create a new template repository |
| `template install` | Install a template repository |
| `template list` | List installed templates |
| `template update` | Update installed templates |
| `template uninstall` | Uninstall a template repository |
| `template validate` | Validate a template repository structure |
| `template backup list` | List template backups |
| `template backup cleanup` | Clean up old template backups |
| `template backup restore` | Restore a template from backup |

### MCP Server Management

| Command | Description |
|---------|-------------|
| `mcp install` | Install MCP server configurations |
| `mcp configure` | Configure credentials for MCP servers |
| `mcp sync` | Sync MCP servers to AI tool configuration files |

### Package Management

| Command | Description |
|---------|-------------|
| [`package install`](package.md#package-install) | Install a configuration package to a project |
| [`package list`](package.md#package-list) | List installed packages |
| [`package uninstall`](package.md#package-uninstall) | Remove a package from a project |
| [`package create`](package.md#package-create) | Create a shareable package from project components |

### Utilities

| Command | Description |
|---------|-------------|
| [`tools`](tools.md) | Show detected AI coding tools |
| `version` | Show DevSync version |

## Global Options

```
$ devsync --help       # Show help
$ devsync --version    # Show version (via `devsync version`)
```

Every command supports `--help` for detailed usage:

```
$ devsync download --help
$ devsync list available --help
$ devsync package install --help
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LOGLEVEL` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | `INFO` |

```
$ LOGLEVEL=DEBUG devsync install
```

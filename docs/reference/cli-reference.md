# CLI Reference

Complete reference for all `devsync` commands. Install with `pip install devsync`.

## Top-Level Commands

### `devsync install`

Install instructions from your library or directly from a source.

```
devsync install [NAMES...] [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--from` | `-f` | `TEXT` | -- | Source URL or path for direct install (bypasses library) |
| `--tool` | `-t` | `TEXT` | -- | AI tool(s) to install to. Repeatable. Values: `cursor`, `copilot`, `windsurf`, `claude`, `kiro`, `cline`, `roo`, `codex`, `gemini`, etc. |
| `--conflict` | `-c` | `TEXT` | `prompt` | Conflict resolution strategy: `prompt`, `skip`, `rename`, `overwrite` |
| `--bundle` | `-b` | flag | `False` | Install as bundle (multiple instructions) |

When called without arguments, launches the interactive TUI for browsing and selecting instructions.

```bash
# Interactive TUI
devsync install

# Install specific instruction from library
devsync install python-style

# Install from specific source (namespace/name)
devsync install company/python-style

# Install multiple instructions
devsync install python-style testing-guide api-design

# Install to specific tools
devsync install python-style --tool cursor --tool windsurf

# Direct install from source URL
devsync install python-style --from https://github.com/company/instructions

# Install bundle directly
devsync install python-backend --bundle --from https://github.com/company/instructions
```

---

### `devsync download`

Download instructions from a source into your local library.

```
devsync download [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--from` | `-f` | `TEXT` | *required* | Source URL or local directory path |
| `--ref` | `-r` | `TEXT` | -- | Git reference (tag, branch, or commit) to download |
| `--as` | `-a` | `TEXT` | -- | Friendly alias for this source (auto-generated if omitted) |
| `--force` | -- | flag | `False` | Re-download even if already in library |

```bash
# Download from GitHub
devsync download --from github.com/company/instructions

# Download specific version
devsync download --from github.com/company/instructions --ref v1.0.0

# Download with custom alias
devsync download --from github.com/company/instructions --as company

# Download from local folder
devsync download --from ./my-instructions --as local

# Force re-download
devsync download --from github.com/company/instructions --force
```

---

### `devsync update`

Update downloaded instructions to their latest versions.

```
devsync update [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--namespace` | `-n` | `TEXT` | -- | Repository namespace to update |
| `--all` | `-a` | flag | `False` | Update all repositories in library |

```bash
devsync update --namespace github.com_company_instructions
devsync update --all
```

---

### `devsync delete`

Delete a source from your local library.

```
devsync delete NAMESPACE [OPTIONS]
```

| Argument | Type | Description |
|----------|------|-------------|
| `NAMESPACE` | `TEXT` | Repository namespace to delete |

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--force` | `-f` | flag | `False` | Skip confirmation prompt |

!!! note
    This removes the downloaded source from your library but does **not** uninstall instructions from your AI tools. Use `devsync uninstall` for that.

```bash
devsync delete github.com_company_instructions
devsync delete github.com_company_instructions --force
```

---

### `devsync uninstall`

Uninstall an instruction from your AI tools.

```
devsync uninstall NAME [OPTIONS]
```

| Argument | Type | Description |
|----------|------|-------------|
| `NAME` | `TEXT` | Instruction name to uninstall |

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--tool` | `-t` | `TEXT` | -- | Uninstall from specific AI tool only |
| `--force` | `-f` | flag | `False` | Skip confirmation prompt |

```bash
devsync uninstall python-best-practices
devsync uninstall python-best-practices --tool cursor
devsync uninstall python-best-practices --force
```

---

### `devsync tools`

Show detected AI coding tools installed on your system.

```
devsync tools
```

No options. Displays a table of detected tools and their configuration directories.

---

### `devsync version`

Show the installed DevSync version.

```
devsync version
```

---

## List Commands

### `devsync list available`

List available instructions from a source without downloading.

```
devsync list available [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--from` | `-f` | `TEXT` | *required* | Source URL or local directory path |
| `--tag` | `-t` | `TEXT` | -- | Filter by tag |
| `--bundles-only` | -- | flag | `False` | Show only bundles |
| `--instructions-only` | -- | flag | `False` | Show only instructions |

```bash
devsync list available --from github.com/company/instructions
devsync list available --from github.com/company/instructions --tag python
devsync list available --from github.com/company/instructions --bundles-only
```

---

### `devsync list installed`

List instructions installed in your AI tools.

```
devsync list installed [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--tool` | `-t` | `TEXT` | -- | Filter by AI tool |
| `--source` | `-s` | `TEXT` | -- | Filter by source alias or name |

```bash
devsync list installed
devsync list installed --tool cursor
devsync list installed --source company
```

---

### `devsync list library`

List sources and instructions in your local library.

```
devsync list library [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--source` | `-s` | `TEXT` | -- | Filter by source alias |
| `--instructions` | `-i` | flag | `False` | Show individual instructions instead of repositories |

```bash
devsync list library
devsync list library --instructions
devsync list library --source company
```

---

## Template Commands

### `devsync template init`

Create a new template repository with scaffolded structure.

```
devsync template init NAME
```

| Argument | Type | Description |
|----------|------|-------------|
| `NAME` | `TEXT` | Name for the new template repository |

---

### `devsync template install`

Install templates from a source.

```
devsync template install SOURCE [OPTIONS]
```

| Argument | Type | Description |
|----------|------|-------------|
| `SOURCE` | `TEXT` | Source URL or local path |

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--as` | `-a` | `TEXT` | -- | Custom namespace alias |
| `--scope` | `-s` | `TEXT` | `project` | Installation scope: `project` or `global` |
| `--conflict` | `-c` | `TEXT` | `prompt` | Conflict resolution: `prompt`, `skip`, `overwrite`, `rename` |

```bash
devsync template install https://github.com/company/templates
devsync template install ./local-templates --as company
devsync template install https://github.com/company/templates --conflict overwrite
```

---

### `devsync template list`

List available templates.

```
devsync template list [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--scope` | `-s` | `TEXT` | `project` | Scope to list: `project` or `global` |

---

### `devsync template update`

Update installed templates to their latest versions.

```
devsync template update NAMESPACE [OPTIONS]
```

| Argument | Type | Description |
|----------|------|-------------|
| `NAMESPACE` | `TEXT` | Template namespace to update |

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--all` | `-a` | flag | `False` | Update all installed templates |

---

### `devsync template uninstall`

Remove installed templates.

```
devsync template uninstall NAMESPACE [OPTIONS]
```

| Argument | Type | Description |
|----------|------|-------------|
| `NAMESPACE` | `TEXT` | Template namespace to uninstall |

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--force` | `-f` | flag | `False` | Skip confirmation prompt |

---

### `devsync template validate`

Validate installed templates for integrity issues.

```
devsync template validate [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--scope` | `-s` | `TEXT` | `project` | Scope to validate: `project` or `global` |
| `--fix` | -- | flag | `False` | Auto-fix detected issues |
| `--verbose` | `-v` | flag | `False` | Show detailed diagnostic output |

---

### `devsync template backup list`

List available template backups.

```
devsync template backup list [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--scope` | `-s` | `TEXT` | `project` | Scope: `project` or `global` |

---

### `devsync template backup restore`

Restore files from a backup.

```
devsync template backup restore [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--scope` | `-s` | `TEXT` | `project` | Scope: `project` or `global` |

---

### `devsync template backup cleanup`

Remove old backups.

```
devsync template backup cleanup [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--days` | `-d` | `INT` | `30` | Remove backups older than this many days |
| `--scope` | `-s` | `TEXT` | `project` | Scope: `project` or `global` |

---

## MCP Commands

### `devsync mcp install`

Install MCP server definitions from a template repository.

```
devsync mcp install SOURCE [OPTIONS]
```

| Argument | Type | Description |
|----------|------|-------------|
| `SOURCE` | `TEXT` | Source URL or local path containing MCP definitions |

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--as` | `-a` | `TEXT` | -- | Custom namespace alias |

---

### `devsync mcp configure`

Configure credentials for installed MCP servers.

```
devsync mcp configure NAMESPACE
```

| Argument | Type | Description |
|----------|------|-------------|
| `NAMESPACE` | `TEXT` | MCP template namespace to configure |

---

### `devsync mcp sync`

Sync MCP server configurations to AI tools.

```
devsync mcp sync [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--tool` | `-t` | `TEXT` | -- | Specific AI tool to sync to |

---

## Package Commands

### `devsync package install`

Install a configuration package to a project.

```
devsync package install PATH [OPTIONS]
```

| Argument | Type | Description |
|----------|------|-------------|
| `PATH` | `TEXT` | Path to package directory containing `ai-config-kit-package.yaml` |

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--ide` | `-i` | `TEXT` | `claude` | Target IDE: `claude`, `cursor`, `windsurf`, `copilot`, etc. |
| `--project` | `-p` | `TEXT` | -- | Project root directory (defaults to auto-detected) |
| `--conflict` | `-c` | `TEXT` | `skip` | Conflict resolution: `skip`, `overwrite`, `rename` |
| `--force` | `-f` | flag | `False` | Force reinstallation even if already installed |
| `--quiet` | `-q` | flag | `False` | Minimal output |
| `--json` | -- | flag | `False` | Output results as JSON |

```bash
devsync package install ./python-dev-setup --ide claude
devsync package install ~/packages/my-package --ide cursor --conflict overwrite
devsync package install ./my-package --force --json
```

---

### `devsync package list`

List installed packages in a project.

```
devsync package list [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--project` | `-p` | `TEXT` | -- | Project root directory (defaults to auto-detected) |
| `--json` | -- | flag | `False` | Output as JSON |

```bash
devsync package list
devsync package list --json
devsync package list --project ~/my-project
```

---

### `devsync package uninstall`

Uninstall a package from a project.

```
devsync package uninstall NAME [OPTIONS]
```

| Argument | Type | Description |
|----------|------|-------------|
| `NAME` | `TEXT` | Package name to uninstall |

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--project` | `-p` | `TEXT` | -- | Project root directory (defaults to auto-detected) |
| `--yes` | `-y` | flag | `False` | Skip confirmation prompt |

```bash
devsync package uninstall test-package
devsync package uninstall my-org/my-package --yes
```

---

### `devsync package create`

Create a package from existing project configurations.

```
devsync package create [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--name` | `-n` | `TEXT` | -- | Package name |

Scans the current project for existing configurations (instructions, MCP servers, hooks, commands, skills, workflows, memory files, resources) and generates an `ai-config-kit-package.yaml` manifest.

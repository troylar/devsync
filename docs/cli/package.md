# devsync package

Manage multi-component configuration packages containing instructions, MCP servers, hooks, commands, and resources.

## Usage

```
$ devsync package <subcommand> [options]
```

For details on the package format and manifest schema, see the [Packages documentation](../packages/index.md).

---

## package install

Install a configuration package to a project.

### Usage

```
$ devsync package install <path> --ide <ide> [options]
```

### Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `path` | Path to package directory containing `ai-config-kit-package.yaml` | Yes |

### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--ide` | `-i` | Target IDE (`claude`, `cursor`, `windsurf`, `copilot`, etc.) | `claude` |
| `--project` | `-p` | Project root directory | Current directory |
| `--conflict` | `-c` | Conflict strategy: `skip`, `overwrite`, `rename` | `skip` |
| `--force` | `-f` | Force reinstallation if already installed | `false` |
| `--quiet` | `-q` | Minimal output | `false` |
| `--json` | | Output results as JSON | `false` |

### IDE Capabilities

Different IDEs support different component types. Unsupported components are automatically skipped.

| IDE | Instructions | MCP | Hooks | Commands | Resources |
|-----|:---:|:---:|:---:|:---:|:---:|
| Claude Code | Yes | Yes | Yes | Yes | Yes |
| Roo Code | Yes | Yes | No | Yes | Yes |
| Cline | Yes | No | No | No | Yes |
| Cursor | Yes | No | No | No | Yes |
| Kiro | Yes | No | No | No | Yes |
| Windsurf | Yes | No | No | No | Yes |
| Codex CLI | Yes | No | No | No | Yes |
| GitHub Copilot | Yes | No | No | No | No |

### Examples

Install a package for Claude Code:

```
$ devsync package install ./python-dev-setup --ide claude
```

Install for Cursor with conflict handling:

```
$ devsync package install ./python-dev-setup --ide cursor --conflict overwrite
```

Force reinstall:

```
$ devsync package install ./python-dev-setup --ide claude --force
```

Install to a specific project:

```
$ devsync package install ./python-dev-setup --ide claude --project ~/my-app
```

JSON output for scripting:

```
$ devsync package install ./python-dev-setup --ide claude --json
```

!!! tip
    Use `--force` combined with `--conflict overwrite` to completely refresh a package installation.

---

## package list

List packages installed in a project.

### Usage

```
$ devsync package list [options]
```

### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--project` | `-p` | Project root directory | Current directory |
| `--json` | | Output as JSON | `false` |

### Examples

List packages in the current project:

```
$ devsync package list
```

List packages in another project:

```
$ devsync package list --project ~/other-project
```

JSON output for scripting:

```
$ devsync package list --json
```

Count installed packages:

```
$ devsync package list --json | jq 'length'
```

### Output

The table shows package name, version, status, component count, and installation date. Status indicators:

- **complete** -- All components installed successfully
- **partial** -- Some components skipped (IDE filtering or conflicts)
- **failed** -- Installation encountered errors
- **pending_credentials** -- MCP servers need credential configuration

---

## package uninstall

Remove an installed package from a project.

### Usage

```
$ devsync package uninstall <name> [options]
```

### Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `name` | Package name to uninstall | Yes |

### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--project` | `-p` | Project root directory | Current directory |
| `--yes` | `-y` | Skip confirmation prompt | `false` |

### Examples

Uninstall with confirmation:

```
$ devsync package uninstall python-dev-setup
```

Uninstall without confirmation:

```
$ devsync package uninstall python-dev-setup --yes
```

Uninstall from a specific project:

```
$ devsync package uninstall python-dev-setup --project ~/my-app --yes
```

!!! warning
    Uninstalling removes all component files that the package installed (instructions, MCP configs, hooks, commands, resources) and deletes the tracking record.

---

## package create

Create a shareable configuration package by scanning your project for AI coding assistant components.

### Usage

```
$ devsync package create [options]
```

### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--name` | `-n` | Package name (lowercase, hyphens allowed) | Prompted |
| `--version` | `-v` | Package version (semver) | `1.0.0` |
| `--description` | `-d` | Package description | Prompted |
| `--author` | `-a` | Package author | Git `user.name` |
| `--license` | `-l` | Package license | `MIT` |
| `--output` | `-o` | Output directory | `.` |
| `--project` | `-p` | Project root to scan | Current directory |
| `--interactive/--no-interactive` | | Interactive component selection | `true` |
| `--scrub-secrets/--keep-secrets` | | Template secrets in MCP configs | Scrub |
| `--force` | `-f` | Overwrite existing package directory | `false` |
| `--quiet` | `-q` | Minimal output | `false` |
| `--json` | | Output results as JSON | `false` |

### Examples

Create a package interactively:

```
$ devsync package create --name my-package
```

Create non-interactively with all options:

```
$ devsync package create --name dev-setup --description "Dev environment" --no-interactive
```

Create to a specific output directory:

```
$ devsync package create --name my-package --output ~/packages
```

!!! tip
    The `create` command scans for instructions, MCP configs, hooks, commands, and resources in your project. In interactive mode, you can select which components to include. Use `--scrub-secrets` (the default) to replace credential values with placeholders.

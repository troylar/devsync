# Installing Packages

## Basic Installation

```bash
devsync package install <package-path> --ide <ide-name>
```

The `<package-path>` is the directory containing `ai-config-kit-package.yaml`. The `--ide` flag specifies which AI coding tool to target.

```bash
# From the project directory
cd ~/my-project
devsync package install ./python-dev-setup --ide claude

# Absolute path
devsync package install /home/user/packages/python-dev-setup --ide claude

# Parent directory
devsync package install ../shared-packages/security --ide cursor
```

## Command Options

```bash
devsync package install <package-path> \
  --ide <ide-name> \
  [--project <path>] \
  [--conflict <strategy>] \
  [--force] \
  [--quiet] \
  [--json]
```

### `--ide, -i` (required)

Target IDE. This determines which components are installed and where files are placed.

=== "Claude Code"

    ```bash
    devsync package install ./pkg --ide claude
    ```

    Installs all component types. Files go to `.claude/rules/`, `.claude/hooks/`, `.claude/commands/`, `.claude/skills/`, and `CLAUDE.md`.

=== "Cursor"

    ```bash
    devsync package install ./pkg --ide cursor
    ```

    Installs instructions (as `.mdc` files), MCP servers, and resources. Hooks, commands, skills, workflows, and memory files are skipped.

=== "Windsurf"

    ```bash
    devsync package install ./pkg --ide windsurf
    ```

    Installs instructions, MCP servers, workflows, and resources. Files go to `.windsurf/rules/` and `.windsurf/workflows/`.

=== "GitHub Copilot"

    ```bash
    devsync package install ./pkg --ide copilot
    ```

    Installs instructions (as `.instructions.md` files) and MCP servers. Files go to `.github/instructions/` and `.vscode/mcp.json`.

=== "Roo Code"

    ```bash
    devsync package install ./pkg --ide roo
    ```

    Installs instructions, MCP servers, commands, and resources. Files go to `.roo/rules/`, `.roo/mcp.json`, and `.roo/commands/`.

=== "Other IDEs"

    ```bash
    devsync package install ./pkg --ide kiro
    devsync package install ./pkg --ide cline
    devsync package install ./pkg --ide codex
    devsync package install ./pkg --ide gemini
    # ... and more
    ```

    Each IDE receives only the component types it supports. Use `devsync/ai_tools/capability_registry.py` as the definitive reference.

### `--project, -p` (optional)

Override the project root directory. By default, DevSync detects the project root by searching for `.git/`, `pyproject.toml`, `package.json`, or similar markers.

```bash
# Install to a different project
devsync package install ./pkg --ide claude --project ~/other-project

# Install same package to multiple projects
devsync package install ./pkg --ide claude --project ~/project-a
devsync package install ./pkg --ide claude --project ~/project-b
```

### `--conflict, -c` (optional)

Conflict resolution strategy when files already exist. Default: `skip`.

```bash
--conflict skip       # Keep existing files, do not install conflicting components
--conflict overwrite  # Replace existing files with package versions
--conflict rename     # Install with a numbered suffix (e.g., style-guide-1.md)
```

See [Conflict Resolution](#conflict-resolution) below for detailed behavior.

### `--force, -f` (optional)

Force reinstallation even if the package is already tracked in `.devsync/packages.json`.

```bash
devsync package install ./pkg --ide claude --force
```

Without `--force`, reinstalling an already-installed package still proceeds but records the operation as a reinstall. Use `--force` combined with `--conflict overwrite` for a clean reset.

### `--quiet, -q` (optional)

Suppress informational output. Only errors and the final result are printed.

```bash
devsync package install ./pkg --ide claude --quiet
```

### `--json` (optional)

Output results as JSON for scripting and CI/CD integration.

```bash
devsync package install ./pkg --ide claude --json
```

```json
{
  "success": true,
  "status": "complete",
  "package_name": "python-dev-setup",
  "version": "2.0.0",
  "installed_count": 6,
  "skipped_count": 0,
  "failed_count": 0,
  "components_installed": {
    "instruction": 2,
    "mcp_server": 1,
    "hook": 1,
    "command": 2
  },
  "is_reinstall": false,
  "error_message": null
}
```

## Conflict Resolution

When a package component targets a file that already exists in the project, the conflict strategy determines behavior.

### Skip (Default)

Existing files are preserved. The conflicting component is not installed.

```bash
devsync package install ./pkg --ide claude --conflict skip
```

```
Installed: 4
Skipped: 1    <- existing file kept
Failed: 0
```

Use `skip` when you have local customizations you want to preserve.

### Overwrite

Existing files are replaced with the package version.

```bash
devsync package install ./pkg --ide claude --conflict overwrite
```

```
Installed: 5    <- all files written, including replacements
Skipped: 0
Failed: 0
```

!!! warning
    Overwrite permanently replaces local changes. There is no undo. Consider committing your changes to version control before using this option.

### Rename

Both versions are kept. The new file receives a numbered suffix.

```bash
devsync package install ./pkg --ide claude --conflict rename
```

After installation:

```
.claude/rules/code-quality.md      <- original, untouched
.claude/rules/code-quality-1.md    <- from package
```

Subsequent installs with `rename` increment the suffix:

```
.claude/rules/code-quality-2.md
.claude/rules/code-quality-3.md
```

### Comparison

| Strategy | Existing File | Package File | Result |
|----------|--------------|--------------|--------|
| `skip` | Preserved | Not installed | Original unchanged |
| `overwrite` | Replaced | Installed | Package version wins |
| `rename` | Preserved | Installed with suffix | Both versions exist |

## IDE Filtering in Practice

A package with 7 components (2 instructions, 1 MCP server, 1 hook, 1 command, 1 workflow, 1 resource) installs differently per IDE:

=== "Claude Code"

    ```bash
    $ devsync package install ./pkg --ide claude

    Successfully installed pkg v1.0.0
      Installed: 6    # instructions, MCP, hook, command, resource
      Skipped: 1      # workflow (Windsurf-only)
    ```

=== "Cursor"

    ```bash
    $ devsync package install ./pkg --ide cursor

    Partially installed pkg v1.0.0
      Installed: 4    # instructions, MCP, resource
      Skipped: 3      # hook, command, workflow
    ```

=== "Windsurf"

    ```bash
    $ devsync package install ./pkg --ide windsurf

    Partially installed pkg v1.0.0
      Installed: 5    # instructions, MCP, workflow, resource
      Skipped: 2      # hook, command
    ```

The installation status is `complete` when all package components are installed, and `partial` when some are filtered by IDE capability.

## Listing Installed Packages

```bash
devsync package list
```

```
Installed packages in /home/user/my-project:

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Package                        ┃ Version ┃ Status     ┃ Components ┃ Installed       ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ acme/python-dev-setup          │ 2.0.0   │ complete   │          6 │ 2025-01-14 10:30│
│ security/compliance-pack       │ 1.1.0   │ partial    │          3 │ 2025-01-15 09:00│
└────────────────────────────────┴─────────┴────────────┴────────────┴─────────────────┘

Total: 2 package(s)
```

### List for a specific project

```bash
devsync package list --project ~/other-project
```

### JSON output

```bash
devsync package list --json
```

```json
[
  {
    "name": "python-dev-setup",
    "namespace": "acme/python-packages",
    "version": "2.0.0",
    "status": "complete",
    "scope": "project",
    "installed_at": "2025-01-14T10:30:00",
    "updated_at": "2025-01-14T10:30:00",
    "component_count": 6
  }
]
```

## Uninstalling Packages

```bash
devsync package uninstall <package-name>
```

This removes all component files installed by the package and deletes the tracking record from `.devsync/packages.json`.

### Interactive (default)

```bash
$ devsync package uninstall python-dev-setup

Package to uninstall:
  Name: python-dev-setup
  Version: 2.0.0
  Components: 6

Are you sure you want to uninstall this package? [y/N]: y

  Removed: .claude/rules/python-style.md
  Removed: .claude/rules/testing-strategy.md
  Removed: .claude/hooks/pre-commit.sh
  Removed: .claude/commands/test.sh
  Removed: .claude/commands/lint.sh
  Removed: .gitignore

Uninstalled python-dev-setup v2.0.0
  Removed 6 file(s)
```

### Non-interactive

Skip the confirmation prompt:

```bash
devsync package uninstall python-dev-setup --yes
```

### Specifying project

```bash
devsync package uninstall python-dev-setup --project ~/other-project
```

## Troubleshooting

### "Manifest not found"

Point to the package directory, not the YAML file:

```bash
# Correct
devsync package install ./my-package --ide claude

# Wrong
devsync package install ./my-package/ai-config-kit-package.yaml --ide claude
```

### "Missing required field"

The manifest must include `name`, `version`, `description`, `author`, `license`, and `namespace`. Check the error message for which field is missing.

### Components not appearing in IDE

1. Verify the IDE supports the component type (see [IDE Compatibility](index.md#ide-compatibility))
2. Some IDEs require a restart to load new configuration files
3. Check that files were installed to the expected paths:

```bash
ls -la .claude/rules/     # Claude Code
ls -la .cursor/rules/     # Cursor
ls -la .windsurf/rules/   # Windsurf
```

### Package shows "partial" status

This is expected when the target IDE does not support all component types in the package. The `partial` status indicates that some components were filtered out by IDE capability, not that the installation failed.

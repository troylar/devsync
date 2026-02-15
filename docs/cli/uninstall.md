# devsync uninstall

Remove an installed instruction from your AI tools at the project level.

## Usage

```
$ devsync uninstall <name> [options]
```

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `name` | Instruction name to uninstall | Yes |

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--tool` | `-t` | Uninstall from a specific AI tool only (`cursor`, `copilot`, `windsurf`, `claude`, etc.) |
| `--force` | `-f` | Skip the confirmation prompt |

## How It Works

The `uninstall` command removes instruction files from your project's AI tool configuration directories and updates the installation tracker. It only affects project-level installations.

Before removing, DevSync shows what will be uninstalled and asks for confirmation (unless `--force` is used).

## Examples

### Uninstall from all tools

```
$ devsync uninstall python-best-practices
```

This removes the instruction from every AI tool it was installed to in the current project.

### Uninstall from a specific tool

```
$ devsync uninstall python-best-practices --tool cursor
```

Only removes from Cursor, leaving other tools untouched.

### Uninstall without confirmation

```
$ devsync uninstall python-best-practices --force
```

### Typical workflow

```
$ devsync list installed                           # See what's installed
$ devsync uninstall python-best-practices          # Remove it
$ devsync list installed                           # Verify removal
```

!!! tip
    Uninstalling removes the file from your AI tool's directory (e.g., `.cursor/rules/`) but does not remove the instruction from your local library. You can reinstall it later with `devsync install`.

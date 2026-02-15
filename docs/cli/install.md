# devsync install

Install instructions from your library or directly from a source into your AI coding tools.

## Usage

```
$ devsync install [names...] [options]
```

## Options

| Option | Short | Description | Required |
|--------|-------|-------------|----------|
| `names` | | Instruction name(s) to install (positional, multiple allowed) | No |
| `--from` | `-f` | Source URL or path for direct install (bypasses library) | No |
| `--tool` | `-t` | AI tool(s) to install to (can specify multiple times) | No |
| `--conflict` | `-c` | Conflict resolution: `prompt`, `skip`, `rename`, `overwrite` | No (default: `prompt`) |
| `--bundle` | `-b` | Install as a bundle (group of instructions) | No |

## Modes

### Interactive TUI Mode

Run `devsync install` with no arguments to open the interactive terminal UI. The TUI lets you browse your library, select instructions, and choose which AI tools to install to.

```
$ devsync install
```

!!! tip
    The TUI requires instructions in your local library. Run `devsync download` first to populate it.

### Named Install from Library

Specify one or more instruction names to install directly from your library:

```
$ devsync install python-best-practices
```

If multiple sources contain an instruction with the same name, use the `source/name` format:

```
$ devsync install company/python-best-practices
```

### Direct Source Install

Use `--from` to install directly from a URL or path without downloading to your library first:

```
$ devsync install python-style --from https://github.com/company/instructions
```

## Conflict Resolution

When an instruction with the same name already exists in the target tool:

| Strategy | Behavior |
|----------|----------|
| `prompt` | Ask what to do (default) |
| `skip` | Keep existing file, do not install |
| `rename` | Install with a numeric suffix (e.g., `instruction-1.md`) |
| `overwrite` | Replace the existing file |

## Examples

### Install with interactive TUI

```
$ devsync install
```

### Install a specific instruction

```
$ devsync install python-best-practices
```

### Install multiple instructions at once

```
$ devsync install python-style testing-guide api-design
```

### Install to specific AI tools

```
$ devsync install python-style --tool cursor --tool claude
```

### Install with conflict handling

```
$ devsync install python-style --conflict overwrite
```

### Install directly from a source

```
$ devsync install python-style --from https://github.com/company/instructions
```

### Install a bundle

```
$ devsync install python-backend --bundle --from https://github.com/company/instructions
```

A bundle installs a group of related instructions defined in the source repository's `ai-config-kit.yaml`.

## AI Tool Detection

If `--tool` is not specified, DevSync auto-detects installed AI tools and installs to the primary detected tool. Use `devsync tools` to see which tools are detected on your system.

All installations are project-scoped. Instruction files are written to the tool-specific directory within your project root (e.g., `.cursor/rules/`, `.claude/rules/`).

# Core Concepts

Key ideas behind how DevSync works.

## Library

The **library** is your local cache of downloaded instruction repositories, stored at `~/.devsync/library/`. Think of it like a local package cache -- you download once, install many times.

```
~/.devsync/library/
├── company/               # namespace: "company"
│   ├── ai-config-kit.yaml
│   └── instructions/
│       ├── python-style.md
│       └── security-checklist.md
└── personal/              # namespace: "personal"
    ├── ai-config-kit.yaml
    └── instructions/
        └── my-preferences.md
```

Commands:

- `devsync download` -- add a repo to your library
- `devsync list library` -- see what's downloaded
- `devsync update` -- pull latest from upstream
- `devsync delete` -- remove from library

## Namespaces

Every downloaded repository gets a **namespace** -- a unique identifier used to organize instructions in the library. By default, the namespace is derived from the Git URL (e.g., `github.com_company_instructions`). Use `--as` to set a friendly alias:

```bash
$ devsync download --from github.com/company/standards --as company
```

Now you can reference instructions as `company/python-style` instead of the full URL-based namespace.

## Instructions

An **instruction** is a single markdown file containing guidance for an AI coding assistant. Instructions are defined in `ai-config-kit.yaml`:

```yaml
name: Python Standards
version: 1.0.0

instructions:
  - name: python-style
    description: Python coding style guide
    file: instructions/python-style.md
    tags: [python, style]
```

When installed, the instruction file is copied to the IDE-specific location (e.g., `.cursor/rules/python-style.mdc` for Cursor).

## Bundles

A **bundle** groups related instructions together for batch installation:

```yaml
bundles:
  - name: python-backend
    description: All Python backend standards
    instructions: [python-style, error-handling, api-design]
```

Install a bundle to get all its instructions at once:

```bash
$ devsync install python-backend --bundle
```

## Installation Scope

DevSync supports two scopes:

| Scope | Location | Active | Best for |
|-------|----------|--------|----------|
| **Project** (default) | `<project>/.claude/rules/` | This project only | Team standards, project-specific rules |
| **Global** | `~/.claude/rules/` | All projects | Personal preferences, company-wide policies |

```bash
# Project scope (default)
$ devsync template install https://github.com/team/standards --as team

# Global scope
$ devsync template install https://github.com/personal/prefs --as mine --scope global
```

Global and project instructions stack -- your IDE sees both.

## Conflict Resolution

When installing an instruction that already exists at the target path, DevSync offers three strategies:

| Strategy | Behavior |
|----------|----------|
| **skip** | Leave the existing file, don't install |
| **rename** | Install with a suffix (e.g., `python-style-1.md`) |
| **overwrite** | Replace the existing file |

By default, DevSync prompts you interactively. Use `--conflict` to choose automatically:

```bash
$ devsync install python-style --conflict overwrite
```

See [Conflict Resolution](../advanced/conflict-resolution.md) for details.

## Templates

The **template system** provides richer functionality than basic instructions:

- **IDE-targeted files** -- different content per IDE
- **Slash commands** -- install commands accessible as `/command-name`
- **Hooks** -- pre-prompt and post-prompt automation
- **Backups** -- automatic backup before updates
- **Validation** -- verify template structure before installation

Templates are installed from Git repos containing a specific directory structure. See the [CLI template commands](../cli/index.md#template-management) for usage.

## Packages

**Packages** are the most comprehensive distribution unit. A package bundles multiple component types:

| Component | Description |
|-----------|-------------|
| Instructions | AI assistant guidance files |
| MCP Servers | Model Context Protocol server configs |
| Hooks | Pre/post prompt automation scripts |
| Commands | Custom slash commands |
| Resources | Supporting files (configs, data) |

Packages are defined by an `ai-config-kit-package.yaml` manifest. See the [Packages guide](../packages/index.md).

## Project Root Detection

DevSync automatically detects your project root by looking for markers like `.git/`, `pyproject.toml`, `package.json`, `Cargo.toml`, and others. This lets you run `devsync` from any subdirectory within a project.

See [Project Root Detection](../advanced/project-root-detection.md) for the full list of markers.

## AI Tool Detection

DevSync scans your system for installed AI tools by checking for their CLI commands and configuration directories. Run `devsync tools` to see what's detected. Each tool has its own file format, directory structure, and feature set -- DevSync handles the translation automatically.

See [IDE Integrations](../ide-integrations/index.md) for the full comparison.

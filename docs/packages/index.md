# Configuration Packages

## What Are Packages?

A configuration package is a directory containing multiple related components that configure AI coding assistants as a unit. Instead of installing instructions, MCP servers, hooks, and commands individually, a package bundles them together with a manifest that declares what is included and how components relate to each other.

A package can contain any combination of these component types:

| Component Type | Description |
|----------------|-------------|
| **Instructions** | Markdown guidelines that shape AI behavior |
| **MCP Servers** | Model Context Protocol server configurations |
| **Hooks** | Scripts triggered by IDE lifecycle events |
| **Commands** | Reusable slash commands and shell scripts |
| **Skills** | Claude Code skill directories (SKILL.md format) |
| **Workflows** | Windsurf multi-step automated processes |
| **Memory Files** | CLAUDE.md persistent context files |
| **Resources** | Configuration files, templates, .gitignore, etc. |

## Why Packages Instead of Individual Instructions?

Individual instructions work well for standalone guidelines. Packages solve a different problem: coordinating multiple components that work together.

**Without packages:**

```bash
# Install instructions one at a time
devsync install python-style-guide
devsync install testing-strategy

# Manually configure MCP servers
# Manually create hooks
# Manually set up commands
# Hope the pieces work together
```

**With packages:**

```bash
devsync package install ./python-dev-setup --ide claude
```

One command installs all components, translates them to the correct IDE format, and tracks everything for later management.

Packages provide:

- **Atomicity** -- install or uninstall an entire configuration as one unit
- **IDE adaptation** -- components are automatically filtered and translated per IDE
- **Tracking** -- installed packages are recorded in `.devsync/packages.json`
- **Conflict handling** -- skip, overwrite, or rename files that already exist
- **Reproducibility** -- share a package directory and anyone gets the same setup

## Installation Workflow

When you run `devsync package install`, the system executes these steps in order:

```
1. Parse Manifest
   Read ai-config-kit-package.yaml, validate required fields,
   resolve component file references

2. Check Existing Installation
   Query .devsync/packages.json to determine if this package
   is already installed (enables reinstall detection)

3. Filter by IDE Capability
   Remove components the target IDE does not support
   (e.g., hooks are skipped for Cursor)

4. Translate Components
   Convert each component to the IDE-specific format
   (file extension, directory path, content structure)

5. Install Files
   Write files to the project, applying the chosen
   conflict resolution strategy (skip/overwrite/rename)

6. Track Installation
   Record the package name, version, component paths,
   checksums, and timestamps in .devsync/packages.json
```

## IDE Compatibility

Different AI coding tools support different component types. When installing a package, DevSync automatically skips components that the target IDE cannot use.

| Component | Claude Code | Cursor | Windsurf | Copilot | Kiro | Cline | Roo Code | Codex CLI |
|-----------|:-----------:|:------:|:--------:|:-------:|:----:|:-----:|:--------:|:---------:|
| Instructions | Y | Y | Y | Y | Y | Y | Y | Y |
| MCP Servers | Y | Y | Y | Y | -- | -- | Y | -- |
| Hooks | Y | -- | -- | -- | -- | -- | -- | -- |
| Commands | Y | -- | -- | -- | -- | -- | Y | -- |
| Skills | Y | -- | -- | -- | -- | -- | -- | -- |
| Workflows | -- | -- | Y | -- | -- | -- | -- | -- |
| Memory Files | Y | -- | -- | -- | -- | -- | -- | -- |
| Resources | Y | Y | Y | -- | Y | Y | Y | Y |

!!! info "Additional IDEs"
    DevSync also supports Gemini CLI, Antigravity, Amazon Q, JetBrains AI, Junie, Zed, Continue.dev, Aider, Trae, Augment, Tabnine, OpenHands, Amp, and OpenCode. All support instructions and resources. MCP support varies -- check `devsync/ai_tools/capability_registry.py` for the full matrix.

### Translation Paths

Components are installed to IDE-specific locations:

=== "Claude Code"

    ```
    Instructions  -> .claude/rules/*.md
    MCP Servers   -> .claude/settings.local.json
    Hooks         -> .claude/hooks/*.sh
    Commands      -> .claude/commands/*.sh
    Skills        -> .claude/skills/<name>/SKILL.md
    Memory Files  -> CLAUDE.md (project root or subdirectories)
    Resources     -> specified install_path
    ```

=== "Cursor"

    ```
    Instructions  -> .cursor/rules/*.mdc
    MCP Servers   -> .cursor/mcp.json
    Resources     -> specified install_path
    ```

=== "Windsurf"

    ```
    Instructions  -> .windsurf/rules/*.md
    MCP Servers   -> ~/.codeium/windsurf/mcp_config.json
    Workflows     -> .windsurf/workflows/*.md
    Resources     -> specified install_path
    ```

=== "GitHub Copilot"

    ```
    Instructions  -> .github/instructions/*.instructions.md
    MCP Servers   -> .vscode/mcp.json
    ```

=== "Roo Code"

    ```
    Instructions  -> .roo/rules/*.md
    MCP Servers   -> .roo/mcp.json
    Commands      -> .roo/commands/*.md
    Resources     -> specified install_path
    ```

## Package Structure

Every package is a directory with an `ai-config-kit-package.yaml` manifest and one or more component directories:

```
my-package/
├── ai-config-kit-package.yaml    # Required manifest
├── README.md                     # Recommended documentation
├── instructions/                 # Instruction .md files
├── mcp/                          # MCP server .json configs
├── hooks/                        # Hook shell scripts
├── commands/                     # Command shell scripts
├── skills/                       # Skill directories (SKILL.md)
├── workflows/                    # Workflow files
├── memory_files/                 # CLAUDE.md files
└── resources/                    # Any additional files
```

## Next Steps

- [Creating Packages](creating.md) -- build your own package from scratch or from an existing project
- [Component Types](components.md) -- detailed reference for each component type
- [Installing Packages](installing.md) -- install, list, and uninstall packages
- [Examples](examples.md) -- complete real-world package examples

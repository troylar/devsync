# YAML Schema Reference

DevSync uses three YAML manifest formats for different purposes.

## ai-config-kit.yaml

The instruction repository manifest. Placed at the root of an instruction repository to define available instructions and bundles.

### Schema

```yaml
# Required fields
name: string              # Repository display name
description: string       # Repository description
version: string           # Semantic version (e.g., "1.0.0")

# Optional fields
author: string            # Author or team name

# Instruction definitions (at least one required)
instructions:
  - name: string          # Unique identifier (lowercase, hyphenated)
    description: string   # What this instruction does
    file: string          # Relative path to instruction file
    tags:                 # Optional categorization tags
      - string

# Bundle definitions (optional)
bundles:
  - name: string          # Bundle identifier
    description: string   # What this bundle provides
    instructions:         # List of instruction names (must reference defined instructions)
      - string
    tags:                 # Optional tags
      - string
```

### Field Details

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Human-readable repository name |
| `description` | Yes | What this repository provides |
| `version` | Yes | Semantic version string |
| `author` | No | Author or team name |
| `instructions` | Yes | At least one instruction must be defined |
| `instructions[].name` | Yes | Unique identifier within the repository |
| `instructions[].description` | Yes | Non-empty description |
| `instructions[].file` | Yes | Relative path from repository root to the instruction file |
| `instructions[].tags` | No | List of string tags for filtering |
| `bundles` | No | Predefined groups of instructions |
| `bundles[].name` | Yes | Unique bundle identifier |
| `bundles[].description` | Yes | Non-empty description |
| `bundles[].instructions` | Yes | Must reference at least one defined instruction by name |
| `bundles[].tags` | No | List of string tags |

### Example

```yaml
name: Python Best Practices
description: Curated Python development instructions for AI coding assistants
version: 2.0.0
author: DevOps Team

instructions:
  - name: python-style
    description: PEP 8 style guide enforcement
    file: instructions/python-style.md
    tags: [python, style, formatting]

  - name: testing-guide
    description: pytest testing conventions and patterns
    file: instructions/testing-guide.md
    tags: [python, testing, pytest]

  - name: api-design
    description: REST API design principles
    file: instructions/api-design.md
    tags: [python, api, rest]

  - name: security-rules
    description: OWASP-based security guidelines
    file: instructions/security-rules.md
    tags: [python, security, owasp]

bundles:
  - name: python-backend
    description: Complete Python backend development setup
    instructions:
      - python-style
      - testing-guide
      - api-design
      - security-rules
    tags: [python, backend, full-stack]

  - name: python-minimal
    description: Minimal Python style and testing
    instructions:
      - python-style
      - testing-guide
    tags: [python, minimal]
```

---

## ai-config-kit-package.yaml

The package manifest. Placed at the root of a package directory to define multi-component configuration bundles.

### Schema

```yaml
# Required fields
name: string              # Package identifier (lowercase, alphanumeric, hyphens)
version: string           # Semantic version
description: string       # Package description

# Optional metadata
author: string            # Package author
license: string           # License identifier (e.g., "MIT", "Apache-2.0")
namespace: string         # Repository namespace (e.g., "org/repo")

# Components (at least one section must be non-empty)
components:
  # Instruction files
  instructions:
    - name: string        # Instruction identifier
      file: string        # Relative path to file
      description: string # What the instruction does
      tags:               # Optional tags
        - string
      ide_support:        # Optional: restrict to specific IDEs
        - string          # e.g., "claude", "cursor"

  # MCP server configurations
  mcp_servers:
    - name: string        # Server identifier
      file: string        # Relative path to JSON config template
      description: string # What the server provides
      ide_support:        # IDEs that support MCP
        - string
      credentials:        # Required environment variables
        - name: string    # Env var name (UPPER_SNAKE_CASE)
          description: string
          required: boolean    # Default: true
          default: string      # Default value (only if not required)
          example: string      # Example value for guidance

  # Lifecycle hooks
  hooks:
    - name: string        # Hook identifier
      file: string        # Relative path to hook script
      description: string # What the hook does
      hook_type: string   # Trigger type: "PreToolUse", "PostToolUse", etc.
      ide_support:        # Default: ["claude"]
        - string

  # Slash commands and scripts
  commands:
    - name: string        # Command identifier
      file: string        # Relative path to command file
      description: string # What the command does
      command_type: string # "slash" or "shell"
      ide_support:
        - string

  # Claude skills (directories with SKILL.md)
  skills:
    - name: string        # Skill identifier (directory name)
      file: string        # Relative path to skill directory
      description: string # What the skill does
      ide_support:        # Default: ["claude"]
        - string

  # Windsurf workflows
  workflows:
    - name: string        # Workflow identifier
      file: string        # Relative path to workflow file
      description: string # What the workflow does
      ide_support:        # Default: ["windsurf"]
        - string

  # CLAUDE.md memory files
  memory_files:
    - name: string        # File identifier
      file: string        # Relative path to CLAUDE.md
      description: string # What context it provides
      ide_support:        # Default: ["claude"]
        - string

  # Arbitrary resource files
  resources:
    - name: string        # Resource identifier
      file: string        # Relative path to file
      description: string # What the resource is
      install_path: string # Where to install (defaults to file path)
      checksum: string    # SHA-256 checksum (sha256:...)
      size: integer       # File size in bytes
```

### Component Type Support by IDE

Not all IDEs support all component types. Unsupported components are automatically skipped during installation.

| Component | Claude | Cursor | Windsurf | Copilot | Kiro | Cline | Roo | Codex | Gemini |
|-----------|--------|--------|----------|---------|------|-------|-----|-------|--------|
| Instructions | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| MCP Servers | Yes | Yes | Yes | Yes | -- | -- | Yes | -- | -- |
| Hooks | Yes | -- | -- | -- | -- | -- | -- | -- | -- |
| Commands | Yes | -- | -- | -- | -- | -- | Yes | -- | -- |
| Skills | Yes | -- | -- | -- | -- | -- | -- | -- | -- |
| Workflows | -- | -- | Yes | -- | -- | -- | -- | -- | -- |
| Memory Files | Yes | -- | -- | -- | -- | -- | -- | -- | -- |
| Resources | Yes | Yes | Yes | -- | Yes | Yes | Yes | Yes | Yes |

### Example

```yaml
name: python-dev-setup
version: 1.0.0
description: Complete Python development configuration for AI assistants
author: Platform Team
license: MIT
namespace: myorg/python-dev-setup

components:
  instructions:
    - name: python-style
      file: instructions/python-style.md
      description: PEP 8 and project-specific style rules
      tags: [python, style]

    - name: testing-guide
      file: instructions/testing-guide.md
      description: pytest conventions and patterns
      tags: [python, testing]

  mcp_servers:
    - name: postgres-explorer
      file: mcp/postgres-explorer.json
      description: Read-only database exploration for AI assistants
      ide_support: [claude, cursor]
      credentials:
        - name: DATABASE_URL
          description: PostgreSQL connection string
          required: true
          example: postgresql://user:pass@localhost:5432/mydb

  hooks:
    - name: lint-check
      file: hooks/lint-check.sh
      description: Run ruff check before AI tool modifications
      hook_type: PreToolUse
      ide_support: [claude]

  commands:
    - name: run-tests
      file: commands/run-tests.md
      description: Execute test suite with coverage
      command_type: slash
      ide_support: [claude]

  skills:
    - name: deploy
      file: skills/deploy/
      description: Production deployment skill
      ide_support: [claude]

  workflows:
    - name: code-review
      file: workflows/code-review.md
      description: Automated code review workflow
      ide_support: [windsurf]

  memory_files:
    - name: project-context
      file: memory/CLAUDE.md
      description: Project architecture and conventions
      ide_support: [claude]

  resources:
    - name: schema-diagram
      file: resources/schema.png
      description: Database schema diagram
      install_path: .devsync/resources/schema.png
      checksum: sha256:abc123...
      size: 45678
```

---

## templatekit.yaml

The template repository manifest. Placed at the root of a template repository for use with `devsync template` commands.

### Schema

```yaml
# Required fields
name: string              # Repository name
description: string       # Repository description
version: string           # Semantic version

# Optional fields
author: string            # Author or team name

# Template definitions (at least one required)
templates:
  - name: string          # Template identifier
    description: string   # What this template provides
    files:                # At least one file required
      - path: string      # Relative path to template file
        ide: string       # Target IDE: "all", "cursor", "claude", "windsurf", etc.
    tags:                 # Optional tags
      - string
    dependencies:         # Optional: other templates this one requires
      - string

# Bundle definitions (optional, minimum 2 templates per bundle)
bundles:
  - name: string          # Bundle identifier
    description: string   # What this bundle provides
    templates:            # Template names (must reference defined templates)
      - string
    tags:
      - string

# MCP server definitions (optional)
mcp_servers:
  - name: string          # Server identifier (alphanumeric, hyphens, underscores)
    command: string       # Executable command
    args:                 # Command-line arguments
      - string
    env:                  # Environment variables (null value = requires user config)
      VAR_NAME: string | null

# MCP sets (optional, named collections of servers)
mcp_sets:
  - name: string          # Set identifier
    description: string   # Set purpose
    servers:              # Server names from mcp_servers
      - string
```

### File Entry Formats

Template files can be specified in two formats:

```yaml
# Simple format (applies to all IDEs)
files:
  - instructions/python-style.md

# Detailed format (IDE-specific)
files:
  - path: instructions/python-style.md
    ide: cursor
  - path: instructions/python-style-claude.md
    ide: claude
```

Valid `ide` values: `all`, `cursor`, `claude`, `windsurf`, `copilot`, `kiro`, `cline`, `roo`, `codex`, `gemini`, `antigravity`, `amazonq`, `jetbrains`, `junie`, `zed`, `continue`, `aider`, `trae`, `augment`, `tabnine`, `openhands`, `amp`, `opencode`.

### Validation Rules

- `name`, `description`, and `version` are required and must be non-empty
- At least one template must be defined
- Each template must have at least one file
- All referenced files must exist in the repository
- Bundle `templates` must reference defined template names
- Bundles must contain at least 2 templates
- Dependencies must reference defined template names (circular dependencies are rejected)
- MCP server names must match `^[a-zA-Z0-9_-]+$`
- MCP environment variable names must match `^[A-Z][A-Z0-9_]*$`

### Example

```yaml
name: Company Standards
description: Shared development standards and MCP servers
version: 1.2.0
author: Platform Engineering

templates:
  - name: code-style
    description: Language-agnostic code style rules
    files:
      - path: templates/code-style.md
        ide: all
    tags: [style, universal]

  - name: security-rules
    description: OWASP-based security guidelines
    files:
      - path: templates/security-cursor.mdc
        ide: cursor
      - path: templates/security.md
        ide: claude
    tags: [security, owasp]
    dependencies:
      - code-style

bundles:
  - name: full-stack
    description: Complete development standards
    templates:
      - code-style
      - security-rules
    tags: [full-stack]

mcp_servers:
  - name: internal-api
    command: npx
    args: ["-y", "@company/mcp-api-server"]
    env:
      API_TOKEN: null
      API_BASE_URL: "https://api.internal.company.com"

mcp_sets:
  - name: backend-dev
    description: Backend development servers
    servers:
      - internal-api
```

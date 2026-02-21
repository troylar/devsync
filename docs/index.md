# DevSync

**Distribute and sync AI coding assistant configurations across your team.**

DevSync is a CLI tool that manages instructions, MCP servers, and configuration packages for 22+ AI coding assistants. Download shared configs from Git repos, install them to any IDE, and keep your team aligned with a single command.

---

<div class="feature-grid" markdown>

<div class="feature-card" markdown>

### Instructions

Share coding standards, style guides, and AI prompts across your team. Works with all 22 supported IDEs.

[Get started](getting-started/quickstart.md){ .md-button }

</div>

<div class="feature-card" markdown>

### MCP Servers

Distribute Model Context Protocol server configurations with secure credential management.

[MCP docs](mcp-server/index.md){ .md-button }

</div>

<div class="feature-card" markdown>

### Configuration Packages

Bundle instructions, MCP servers, hooks, commands, and resources into installable packages.

[Package guide](packages/index.md){ .md-button }

</div>

<div class="feature-card" markdown>

### 23 IDE Integrations

Claude Code, Cursor, Windsurf, GitHub Copilot, Codex CLI, Cline, Kiro, Roo Code, Anteroom, and 14 more.

[See all IDEs](ide-integrations/index.md){ .md-button }

</div>

</div>

---

## Quick Start

```bash
# Install DevSync
$ pip install devsync

# Check which AI tools are detected
$ devsync tools

# Download instructions from a Git repo
$ devsync download --from github.com/company/standards --as company

# Install to your IDE (interactive TUI)
$ devsync install
```

See the full [quickstart guide](getting-started/quickstart.md) for a 5-minute walkthrough.

---

## Why DevSync?

**For teams:**

- **Consistency** -- everyone uses the same AI instructions and tool configs
- **Onboarding** -- new developers get configured in minutes, not hours
- **Compliance** -- enforce security policies and review checklists automatically
- **No secrets in Git** -- credentials stay local, configurations are shared

**For individuals:**

- **Portable** -- same setup across all your machines
- **Composable** -- layer company, team, and personal configs
- **Discoverable** -- install from any Git repository
- **Safe** -- automatic backups, conflict resolution, checksums

---

## Supported IDEs

### Multi-file IDEs

| Tool | Instruction Path | Extension |
|------|-----------------|-----------|
| [Claude Code](ide-integrations/claude-code.md) | `.claude/rules/` | `.md` |
| [Cursor](ide-integrations/cursor.md) | `.cursor/rules/` | `.mdc` |
| [Windsurf](ide-integrations/windsurf.md) | `.windsurf/rules/` | `.md` |
| [GitHub Copilot](ide-integrations/copilot.md) | `.github/instructions/` | `.instructions.md` |
| [Roo Code](ide-integrations/other-ides.md#roo-code) | `.roo/rules/` | `.md` |
| [Cline](ide-integrations/other-ides.md#cline) | `.clinerules/` | `.md` |
| [Kiro](ide-integrations/other-ides.md#kiro) | `.kiro/steering/` | `.md` |
| + 8 more | [Full list](ide-integrations/index.md) | |

### Single-file IDEs

| Tool | Instruction File |
|------|-----------------|
| [Codex CLI](ide-integrations/codex.md) | `AGENTS.md` |
| [Aider](ide-integrations/other-ides.md#aider) | `CONVENTIONS.md` |
| [Gemini CLI](ide-integrations/other-ides.md#gemini-cli) | `GEMINI.md` |
| + 4 more | [Full list](ide-integrations/index.md) |

---

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Git Repository  │────>│  Local       │────>│  Project IDE    │
│  (team configs)  │     │  Library     │     │  Config Files   │
│                  │     │  ~/.devsync/ │     │  .cursor/rules/ │
└─────────────────┘     └──────────────┘     │  .claude/rules/ │
    devsync download        devsync install   │  .windsurf/...  │
                                              └─────────────────┘
```

1. **Download** instruction repos to your local library (`~/.devsync/library/`)
2. **Browse** instructions with the interactive TUI or CLI
3. **Install** to any AI tool at project level
4. **Update** with a single command when upstream changes

---

## Documentation

| Section | What you'll find |
|---------|-----------------|
| [Getting Started](getting-started/installation.md) | Installation, quickstart, core concepts |
| [CLI Reference](cli/index.md) | All commands with examples |
| [IDE Integrations](ide-integrations/index.md) | Setup guides for each AI tool |
| [Packages](packages/index.md) | Creating and installing config packages |
| [MCP Server](mcp-server/index.md) | devsync-mcp for AI-powered config merging |
| [Tutorials](tutorials/team-config-repo.md) | Step-by-step walkthroughs |
| [Advanced](advanced/config-types.md) | Config types, conflict resolution, contributing |
| [Reference](reference/cli-reference.md) | Full CLI reference, YAML schemas |

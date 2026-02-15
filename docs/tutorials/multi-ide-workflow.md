# Using DevSync Across Multiple IDEs

**Time to complete**: 10 minutes
**Difficulty**: Beginner
**Prerequisites**:

- DevSync installed (`pip install devsync`)
- Two or more AI coding assistants installed (e.g., Claude Code, Cursor, GitHub Copilot)

## The Scenario

You use multiple AI coding assistants throughout the day -- perhaps Claude Code for complex refactoring, Cursor for quick edits, and GitHub Copilot for inline suggestions. Each tool has its own configuration directory and file format. You want the same coding standards applied across all of them without manually duplicating files.

## What You Will Learn

- How to detect which AI tools are available on your machine
- How to install the same instructions to multiple IDEs at once
- How each IDE stores its configuration files and what format differences exist
- How to keep instructions in sync when updating
- When to use packages versus individual instructions

---

## Step 1: Detect Available Tools

DevSync auto-detects installed AI coding assistants. Run:

```bash
devsync tools
```

Expected output (varies by machine):

```
Detected AI Tools:

Tool              Status     Install Path
Claude Code       detected   .claude/rules/
Cursor            detected   .cursor/rules/
GitHub Copilot    detected   .github/instructions/
Windsurf          detected   .windsurf/rules/
Cline             not found
Roo Code          not found
Codex CLI         not found
Kiro              not found

4 tool(s) detected.
```

!!! info "Detection logic"
    DevSync checks for the presence of each tool's CLI or application on your system. A tool showing as "detected" means DevSync can install configurations for it. You do not need to have the tool actively running.

---

## Step 2: Download Instructions to Your Library

Download a template repository to your local library. This tutorial uses the starter templates as an example:

```bash
devsync download https://github.com/troylar/devsync-starter-templates
```

Expected output:

```
Cloning repository...
Repository downloaded to library: ~/.devsync/library/troylar/devsync-starter-templates

Instructions found:
  python-standards     Python coding conventions
  security-policy      Security guidelines
  code-review          Structured review checklist
```

Browse what is available:

```bash
devsync list available
```

This displays all instructions in your local library, ready to install.

---

## Step 3: Install to Multiple IDEs

Install an instruction to a specific IDE using the `--tool` flag:

```bash
cd ~/projects/my-project

# Install to Claude Code
devsync install python-standards --tool claude

# Install to Cursor
devsync install python-standards --tool cursor

# Install to GitHub Copilot
devsync install python-standards --tool copilot
```

Each command places the instruction file in the correct directory with the correct format for that IDE.

To install to all detected IDEs at once, use the interactive TUI:

```bash
devsync install
```

The TUI lets you select instructions from your library and choose which IDEs to target. Selected instructions are installed to all chosen tools simultaneously.

!!! tip "Batch installation"
    If you have many instructions to install, the TUI is faster than running individual commands. It shows a unified view of your library and lets you select multiple instructions at once.

---

## Step 4: Understand File Format Differences

Each IDE expects its configuration files in a specific format and location. DevSync handles these translations automatically.

| IDE | Directory | Extension | Notes |
|-----|-----------|-----------|-------|
| Claude Code | `.claude/rules/` | `.md` | Standard Markdown |
| Cursor | `.cursor/rules/` | `.mdc` | Cursor-specific Markdown variant |
| Cline | `.clinerules/` | `.md` | Standard Markdown |
| Kiro | `.kiro/steering/` | `.md` | Standard Markdown |
| Roo Code | `.roo/rules/` | `.md` | Standard Markdown |
| Windsurf | `.windsurf/rules/` | `.md` | Standard Markdown |
| GitHub Copilot | `.github/instructions/` | `.md` | Standard Markdown |
| Codex CLI | `AGENTS.md` | `.md` | Sections within a single file |

After installing `python-standards` to three IDEs, your project structure looks like this:

```
my-project/
├── .claude/
│   └── rules/
│       └── python-standards.md
├── .cursor/
│   └── rules/
│       └── python-standards.mdc
├── .github/
│   └── instructions/
│       └── python-standards.md
├── .devsync/
│   └── installations.json
└── ... (project files)
```

!!! warning "Cursor's .mdc format"
    Cursor uses `.mdc` files, which are similar to Markdown but may include Cursor-specific frontmatter. DevSync converts standard Markdown instructions to the `.mdc` format automatically. Do not rename `.mdc` files to `.md` -- Cursor will not pick them up.

---

## Step 5: Keep Instructions in Sync

When the source repository is updated, you can pull the latest changes and reinstall:

```bash
# Update your local library
devsync update troylar/devsync-starter-templates

# Reinstall to all IDEs
devsync install python-standards --tool claude
devsync install python-standards --tool cursor
devsync install python-standards --tool copilot
```

DevSync detects that the files already exist and prompts you with conflict resolution options:

```
File already exists: .claude/rules/python-standards.md

Choose action:
  [s] Skip -- keep the existing file
  [o] Overwrite -- replace with the updated version
  [r] Rename -- install as python-standards-1.md

Your choice:
```

To skip the prompt and always overwrite, use the `--conflict overwrite` flag:

```bash
devsync install python-standards --tool claude --conflict overwrite
```

---

## Step 6: When to Use Packages vs. Individual Instructions

DevSync supports two installation modes:

**Individual instructions** are single files installed one at a time. Use them when:

- You only need coding standards or guidelines
- Different projects need different subsets of instructions
- You want fine-grained control over what is installed

**Packages** are bundles containing multiple component types (instructions, MCP servers, hooks, commands, resources). Use them when:

- You need to install a coordinated set of components
- MCP server configurations or hooks are involved
- You want one-command installation of a complete setup

Install a package with:

```bash
devsync package install https://github.com/troylar/devsync-python-package --ide claude
```

!!! info "Package IDE support"
    Not all IDEs support all component types. For example, Claude Code supports instructions, MCP servers, hooks, commands, and resources. Cursor only supports instructions and resources. DevSync automatically skips unsupported components and reports what was installed versus what was skipped.

To see what a package contains before installing:

```bash
devsync package install https://github.com/troylar/devsync-python-package --ide claude --dry-run
```

---

## Troubleshooting

### "No AI tools detected"

Install at least one supported AI coding assistant and ensure it is on your system PATH. Run `devsync tools` after installation to confirm detection.

### Instruction installed but IDE does not use it

Some IDEs require a restart or project reload to pick up new configuration files. Close and reopen the IDE, or reload the project window.

### Cursor ignores the installed file

Verify the file has the `.mdc` extension and is located in `.cursor/rules/`. Cursor does not read `.md` files from this directory.

### Conflict on every install

If you frequently update instructions, use `--conflict overwrite` to avoid repeated prompts:

```bash
devsync install python-standards --tool claude --conflict overwrite
```

### Instructions appear in one IDE but not another

Run `devsync list installed` to see which tools each instruction was installed to. You may need to install explicitly for each tool:

```bash
devsync install python-standards --tool cursor
```

---

## Next Steps

- [Enforcing DevSync Standards in CI/CD](ci-cd-integration.md) -- Validate instruction compliance in your CI pipeline
- [Migrating Existing AI Configs to DevSync](migrate-existing-configs.md) -- Bring existing config files under DevSync management
- [Build and Distribute a Custom Package](custom-packages.md) -- Create multi-component packages for your team

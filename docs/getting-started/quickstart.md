# Quickstart

Get DevSync working in 5 minutes.

## 1. Install DevSync

```bash
$ pip install devsync
```

## 2. Check Your IDEs

```bash
$ devsync tools
```

DevSync auto-detects which AI coding tools are installed. You'll see something like:

```
Detected AI Tools:
  Claude Code    .claude/rules/          (.md)
  Cursor         .cursor/rules/          (.mdc)
  Windsurf       .windsurf/rules/        (.md)
```

## 3. Download Instructions

Download a repository of instructions to your local library:

```bash
$ devsync download --from github.com/company/coding-standards --as company
```

This clones the repo to `~/.devsync/library/company/`. The `--as` flag sets a friendly alias.

!!! info
    You can also download from local directories:

    ```bash
    $ devsync download --from ./my-instructions --as local
    ```

## 4. Browse and Install

Launch the interactive TUI to browse and select instructions:

```bash
$ devsync install
```

The TUI shows all instructions in your library. Select which ones to install and which IDEs to target.

Or install by name directly:

```bash
$ devsync install python-best-practices --tool cursor --tool claude
```

## 5. Verify

Check what's installed:

```bash
$ devsync list installed
```

Your AI tools now have the instructions. Open your IDE and the coding assistant will follow them automatically.

---

## Alternative: Templates

Templates provide a richer system with slash commands, hooks, and more:

```bash
# Create a template repo
$ devsync template init my-standards

# Install from Git
$ devsync template install https://github.com/company/templates --as company

# List installed
$ devsync template list
```

See the [CLI reference](../cli/index.md) for full template commands.

---

## Alternative: Packages

Packages bundle instructions, MCP servers, hooks, and commands together:

```bash
# Install a complete package
$ devsync package install ./example-package --ide claude

# List installed packages
$ devsync package list
```

See the [Packages guide](../packages/index.md) for details.

---

## What's Next?

- [Core Concepts](concepts.md) -- understand the library, namespaces, and scopes
- [CLI Reference](../cli/index.md) -- all commands with examples
- [IDE Integrations](../ide-integrations/index.md) -- setup guide for each AI tool
- [Tutorials](../tutorials/team-config-repo.md) -- step-by-step walkthroughs

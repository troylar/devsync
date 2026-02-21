<div align="center">

# DevSync

**Distribute and sync AI coding assistant configurations across your team**

[![CI](https://github.com/troylar/devsync/actions/workflows/ci.yml/badge.svg)](https://github.com/troylar/devsync/actions/workflows/ci.yml)
[![Docs](https://readthedocs.org/projects/devsync/badge/?version=latest)](https://devsync.readthedocs.io)
[![PyPI version](https://img.shields.io/pypi/v/devsync.svg)](https://pypi.org/project/devsync/)
[![Coverage](https://codecov.io/gh/troylar/devsync/branch/main/graph/badge.svg)](https://codecov.io/gh/troylar/devsync)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Works with:** Aider | Amazon Q | Amp | Antigravity | Augment | Claude Code | Claude Desktop | Cline | Codex CLI | Continue.dev | Cursor | Gemini CLI | GitHub Copilot | JetBrains AI | Junie | Kiro | OpenCode | OpenHands | Roo Code | Tabnine | Trae | Windsurf | Zed

</div>

---

DevSync is a CLI tool for managing AI coding assistant instructions, MCP servers, and configuration packages across 22+ IDEs. Download shared configs from Git repos, install them to any tool, and keep your team aligned.

## Quick Start

```bash
pip install devsync

# Check detected AI tools
devsync tools

# Download instructions from a Git repo
devsync download --from github.com/company/standards --as company

# Install interactively
devsync install
```

## Features

- **Instructions** -- share coding standards, style guides, and AI prompts from Git repos
- **MCP Servers** -- distribute Model Context Protocol configs with secure credential management
- **Packages** -- bundle instructions, MCP servers, hooks, commands, and resources together
- **23 IDE integrations** -- Claude Code, Cursor, Windsurf, GitHub Copilot, and 19 more
- **Templates** -- IDE-targeted content with slash commands, hooks, and backups
- **Conflict resolution** -- skip, overwrite, or rename when files already exist

## Documentation

Full documentation at **[devsync.readthedocs.io](https://devsync.readthedocs.io)**:

- [Getting Started](https://devsync.readthedocs.io/getting-started/installation/) -- installation, quickstart, core concepts
- [CLI Reference](https://devsync.readthedocs.io/cli/) -- all commands with examples
- [IDE Integrations](https://devsync.readthedocs.io/ide-integrations/) -- setup guides for each AI tool
- [Packages](https://devsync.readthedocs.io/packages/) -- creating and installing config packages
- [MCP Server](https://devsync.readthedocs.io/mcp-server/) -- MCP configuration management
- [Tutorials](https://devsync.readthedocs.io/tutorials/team-config-repo/) -- step-by-step walkthroughs

## Contributing

```bash
git clone https://github.com/troylar/devsync.git
cd devsync
pip install -e .[dev]
invoke test
```

See the [contributing guide](https://devsync.readthedocs.io/advanced/contributing/) for details.

## License

MIT -- see [LICENSE](LICENSE).

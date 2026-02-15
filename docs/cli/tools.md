# devsync tools

Show which AI coding tools are detected on your system.

## Usage

```
$ devsync tools
```

No options. The command scans for supported tools and reports their installation status.

## Example Output

```
AI Coding Tools
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Tool                ┃ Status        ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ Cursor              │ ✓ Installed   │
│ GitHub Copilot      │ ✓ Installed   │
│ Windsurf            │ ✗ Not found   │
│ Claude Code         │ ✓ Installed   │
│ Kiro                │ ✗ Not found   │
│ Cline               │ ✗ Not found   │
│ Roo Code            │ ✗ Not found   │
│ ...                 │               │
└─────────────────────┴───────────────┘

Found 3 installed tool(s): Cursor, GitHub Copilot, Claude Code
```

## Supported Tools

DevSync supports 21 AI coding tools:

| Tool | Config Directory | File Extension |
|------|-----------------|----------------|
| Cursor | `.cursor/rules/` | `.mdc` |
| GitHub Copilot | `.github/instructions/` | `.md` |
| Windsurf | `.windsurf/rules/` | `.md` |
| Claude Code | `.claude/rules/` | `.md` |
| Kiro | `.kiro/steering/` | `.md` |
| Cline | `.clinerules/` | `.md` |
| Roo Code | `.roo/rules/` | `.md` |
| Codex CLI | `AGENTS.md` (sections) | `.md` |
| Gemini | `.gemini/` | `.md` |
| Antigravity | `.antigravity/` | `.md` |
| Amazon Q | `.amazonq/rules/` | `.md` |
| JetBrains AI | `.junie/` | `.md` |
| Junie | `.junie/` | `.md` |
| Zed | `.zed/` | `.md` |
| Continue | `.continue/` | `.md` |
| Aider | `.aider/` | `.md` |
| Trae | `.trae/rules/` | `.md` |
| Augment | `.augment/` | `.md` |
| Tabnine | `.tabnine/` | `.md` |
| OpenHands | `.openhands/` | `.md` |
| Amp | `.amp/` | `.md` |
| OpenCode | `.opencode/` | `.md` |

!!! tip
    Run `devsync tools` to verify which tools are detected before running `devsync install`. Auto-detection determines where instructions get installed when you don't specify `--tool`.

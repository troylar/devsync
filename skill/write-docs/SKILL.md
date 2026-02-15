# /write-docs

Write or update DevSync documentation pages following the project's style conventions.

## Usage

```
/write-docs <page-path> [description of changes]
```

Examples:
- `/write-docs docs/cli/download.md` -- rewrite from scratch based on current source
- `/write-docs docs/ide-integrations/cursor.md add MCP tool limit info` -- update specific section
- `/write-docs docs/tutorials/new-tutorial.md create a tutorial about X` -- create new page

## Instructions

When writing or updating documentation:

### Style

- **Voice:** Direct, second-person ("you"), active voice
- **Tone:** Professional but approachable. No filler, no fluff
- **No preambles:** Don't start with "In this section you will learn..."
- **One-sentence opener:** Every page starts with a single sentence explaining what the page covers
- **No emojis** in documentation unless explicitly requested

### Structure

- Use `#` for page title, `##` for major sections, `###` for subsections
- Use MkDocs Material admonitions: `!!! tip`, `!!! warning`, `!!! info`, `!!! example`
- Use tabbed code blocks (`=== "Tab Name"`) for multi-IDE examples
- Use tables for comparisons and option references
- Link between pages liberally -- every mention of another feature should link to its page

### Code Examples

- Every concept gets a working example
- CLI examples use `$ ` prefix: `$ devsync install`
- Show expected output where helpful
- Use language-specific fenced blocks: ````bash`, ````yaml`, ````json`, ````python`

### CLI Command Pages

Each CLI command page should follow this structure:

```markdown
# devsync <command>

One-sentence description of what the command does.

## Usage

\```
$ devsync <command> [args] [options]
\```

## Options

| Option | Short | Description | Required |
|--------|-------|-------------|----------|
| `--flag` | `-f` | What it does | Yes/No |

## How It Works

Brief explanation of the command's behavior.

## Examples

### Example Title

\```
$ devsync <command> --flag value
\```
```

### IDE Integration Pages

Each IDE page should include:
- How DevSync installs instructions to this IDE
- File format and location
- MCP support (if applicable)
- Package component support matrix
- Example installation command
- Tabbed config examples where relevant

### Reference Pages

- Include all flags and options
- Document environment variables
- Show YAML/JSON schemas with annotated examples

## Source of Truth

Always read the actual source code before writing docs:

- **CLI commands:** `devsync/cli/main.py` and individual command files in `devsync/cli/`
- **AI tools:** `devsync/ai_tools/` for IDE-specific paths and behavior
- **Models:** `devsync/core/models.py` for data structures
- **Package system:** `devsync/cli/package.py` and `devsync/cli/package_install.py`

## File Organization

```
docs/
├── index.md                    # Landing page
├── getting-started/            # Installation, quickstart, concepts
├── cli/                        # One page per command group
├── ide-integrations/           # One page per major IDE + other-ides.md
├── packages/                   # Package system docs
├── mcp-server/                 # MCP configuration + devsync-mcp
├── tutorials/                  # Step-by-step walkthroughs
├── advanced/                   # Deep dives
└── reference/                  # Full reference docs
```

## MkDocs Configuration

The site uses MkDocs Material. Config is in `mkdocs.yml` at the repo root. Navigation is defined in the `nav` section -- update it when adding new pages.

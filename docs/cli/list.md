# devsync list

List instructions from remote sources, your local library, or installed in your AI tools.

## Usage

```
$ devsync list <subcommand> [options]
```

---

## list available

List instructions from a remote source without downloading.

### Usage

```
$ devsync list available --from <source> [options]
```

### Options

| Option | Short | Description | Required |
|--------|-------|-------------|----------|
| `--from` | `-f` | Source URL or local directory path | Yes |
| `--tag` | `-t` | Filter by tag | No |
| `--bundles-only` | | Show only bundles | No |
| `--instructions-only` | | Show only individual instructions | No |

### Examples

List all instructions from a repository:

```
$ devsync list available --from https://github.com/company/ai-instructions
```

List from a local directory:

```
$ devsync list available --from ./my-instructions
```

Filter by tag:

```
$ devsync list available --from https://github.com/company/ai-instructions --tag python
```

Show only bundles:

```
$ devsync list available --from https://github.com/company/ai-instructions --bundles-only
```

Show only individual instructions (no bundles):

```
$ devsync list available --from https://github.com/company/ai-instructions --instructions-only
```

!!! tip
    Use `list available` to preview what a repository offers before downloading it with `devsync download`.

---

## list installed

List instructions currently installed in your AI tools at the project level.

### Usage

```
$ devsync list installed [options]
```

### Options

| Option | Short | Description | Required |
|--------|-------|-------------|----------|
| `--tool` | `-t` | Filter by AI tool (`cursor`, `copilot`, `windsurf`, `claude`, etc.) | No |
| `--source` | `-s` | Filter by source alias or name | No |

### Examples

List all installed instructions:

```
$ devsync list installed
```

Filter by AI tool:

```
$ devsync list installed --tool cursor
```

Filter by source:

```
$ devsync list installed --source company
```

Combine filters:

```
$ devsync list installed --tool claude --source company
```

---

## list library

List sources and instructions stored in your local library (`~/.devsync/library/`).

### Usage

```
$ devsync list library [options]
```

### Options

| Option | Short | Description | Required |
|--------|-------|-------------|----------|
| `--source` | `-s` | Filter by source alias or namespace | No |
| `--instructions` | `-i` | Show individual instructions instead of repositories | No |

### Examples

List all downloaded sources:

```
$ devsync list library
```

Show individual instructions across all sources:

```
$ devsync list library --instructions
```

Filter by source:

```
$ devsync list library --source company
```

!!! tip
    The default view shows repository-level summaries. Use `--instructions` to see every individual instruction with its name, description, tags, and version.

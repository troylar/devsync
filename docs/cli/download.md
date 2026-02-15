# devsync download

Download instructions from a source into your local library at `~/.devsync/library/`.

## Usage

```
$ devsync download --from <source> [options]
```

## Options

| Option | Short | Description | Required |
|--------|-------|-------------|----------|
| `--from` | `-f` | Source URL or local directory path | Yes |
| `--ref` | `-r` | Git reference (tag, branch, or commit) | No |
| `--as` | `-a` | Custom alias for this source | No |
| `--force` | | Re-download even if already in library | No |

## How It Works

The `download` command clones or copies instruction repositories into `~/.devsync/library/`, organized by namespace. Instructions are cached locally but not installed to any AI tool. Use `devsync install` after downloading to install instructions into your project.

Each downloaded source gets a namespace (auto-generated from the URL) and an optional alias for easier reference.

!!! tip
    Download first, then install. This two-step workflow lets you browse and selectively install instructions without re-cloning every time.

## Examples

### Download from a Git URL

```
$ devsync download --from https://github.com/company/ai-instructions
```

### Download from a local folder

```
$ devsync download --from ./my-instructions
```

!!! warning
    The `--ref` option is not supported for local directories. Local sources are copied as-is.

### Download a specific tag

```
$ devsync download --from https://github.com/company/ai-instructions --ref v1.0.0
```

Tags and commits are treated as immutable. They will not be updated by `devsync update`.

### Download from a specific branch

```
$ devsync download --from https://github.com/company/ai-instructions --ref develop
```

Branch-based downloads can be updated later with `devsync update`.

### Download with a custom alias

```
$ devsync download --from https://github.com/company/ai-instructions --as company
```

The alias makes it easier to reference the source when listing or installing instructions.

### Force re-download

```
$ devsync download --from https://github.com/company/ai-instructions --force
```

Use `--force` to overwrite a source that already exists in your library.

## What Happens Next

After downloading, you can:

- Browse your library: `devsync list library`
- View individual instructions: `devsync list library --instructions`
- Install interactively: `devsync install`
- Install by name: `devsync install python-best-practices`

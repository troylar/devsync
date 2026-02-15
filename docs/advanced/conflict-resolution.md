# Conflict Resolution

When installing instructions or templates, DevSync checks whether the target file already exists. If it does, a conflict must be resolved before installation can proceed.

## When Conflicts Occur

A conflict is detected when:

- An instruction file already exists at the target path (e.g., `.cursor/rules/python-style.mdc` already exists)
- A template has been modified locally since it was last installed
- A section with the same name already exists in a single-file IDE (e.g., an `AGENTS.md` section with the same marker)
- A package component would overwrite an existing file

## Resolution Strategies

DevSync provides four conflict resolution strategies.

### Prompt (Default)

The default strategy for interactive use. When a conflict is detected, DevSync displays a Rich terminal prompt asking the user to choose how to proceed.

```
Conflict: Instruction 'python-style' already exists.
How would you like to resolve this?
  [K]eep local version (ignore remote update)
  [O]verwrite with remote version (discard local changes)
  [R]ename local and install remote

Your choice [k/o/r]:
```

For template conflicts, the prompt also displays context about the conflict type (local-only changes vs. both sides changed).

### Skip

Keeps the existing file unchanged. The new instruction is not installed.

```bash
devsync install python-style --conflict skip
```

Use this when you want to preserve any existing configurations without interruption.

### Overwrite

Replaces the existing file with the new content.

!!! warning "Automatic Backup"
    When using the overwrite strategy during template operations, DevSync automatically creates a timestamped backup of the existing file before overwriting it. Backups are stored in `.devsync/backups/<timestamp>/`.

    ```
    Backup created: 20260215_143052/python-style.md
    ```

```bash
devsync install python-style --conflict overwrite
```

### Rename

Installs the new instruction with an auto-incremented suffix to avoid overwriting the existing file. The existing file is left untouched.

```bash
devsync install python-style --conflict rename
```

This generates filenames like:

- `python-style-1.md`
- `python-style-2.md`

For template conflicts with the rename strategy, the existing local file is renamed (preserving local changes) and the new remote version is installed at the original path.

## Setting Strategy via CLI

### Instructions

Use the `--conflict` (or `-c`) flag with `devsync install`:

```bash
# Interactive prompt (default)
devsync install python-style

# Skip conflicts silently
devsync install python-style --conflict skip

# Overwrite existing files
devsync install python-style --conflict overwrite

# Rename to avoid conflicts
devsync install python-style --conflict rename
```

### Templates

Use the `--conflict` flag with `devsync template install`:

```bash
devsync template install my-repo/security-rules --conflict overwrite
```

### Packages

Use the `--conflict` (or `-c`) flag with `devsync package install`:

```bash
devsync package install ./my-package --ide claude --conflict overwrite
```

## Upgrade Detection

When reinstalling an instruction from a newer version of a source repository, DevSync detects version changes and prompts for confirmation.

The upgrade detection workflow:

1. DevSync checks the installation tracker for existing records of the instruction
2. If the instruction exists and comes from the same source, it compares the `source_ref` (Git tag, branch, or commit)
3. If versions differ, it displays a side-by-side comparison:

```
Upgrade available: python-style
  Current: v1.0.0
  New:     v2.0.0

Proceed with upgrade? [y/N]:
```

This works across all AI tools and respects the configured conflict resolution strategy.

## Name Collision Handling

When an instruction with the same name exists from a **different** repository, DevSync treats this as a name collision rather than an upgrade.

The collision handling workflow:

1. DevSync queries the installation tracker with `find_instructions_by_name()` to find existing installations
2. If the instruction exists from a different source, it displays detailed information:

```
Name collision: 'python-style' already installed
  Existing source: github.com/team-a/instructions
  New source:      github.com/team-b/instructions

Options:
  1. Provide custom filename
  2. Skip installation
```

3. The user can provide an alternative filename to install both instructions without conflict, or skip the installation entirely.

## Checksum-Based Conflict Detection

For template operations, DevSync uses a three-way checksum comparison to determine the exact nature of a conflict:

| Current File | Original (at install) | New Template | Result |
|---|---|---|---|
| Unchanged | -- | Unchanged | No conflict |
| Unchanged | -- | Changed | No conflict (safe to update) |
| Changed | -- | Unchanged | `LOCAL_MODIFIED` |
| Changed | -- | Changed | `BOTH_MODIFIED` |

- **No conflict**: The file can be updated automatically
- **LOCAL_MODIFIED**: The user modified the file but the remote template has not changed. The prompt asks whether to keep local or overwrite.
- **BOTH_MODIFIED**: Both the local file and the remote template have changed. The prompt asks the user to choose which version to keep or to rename the local copy.

All checksums use SHA-256 for integrity verification.

## Batch Conflict Resolution

When installing multiple instructions at once (e.g., a bundle or package), DevSync can apply the same strategy to all conflicts:

```bash
# Skip all conflicts in a batch install
devsync install python-style testing-guide api-design --conflict skip

# Overwrite all existing files
devsync install --bundle python-backend --conflict overwrite
```

The `batch_resolve_conflicts()` function applies the chosen strategy uniformly to all detected conflicts in a single operation.

## Backup Integration

Backups are created automatically before any destructive operation during template conflict resolution. The backup system:

- Stores backups in `.devsync/backups/<YYYYMMDD_HHMMSS>/`
- Preserves the original filename
- Handles name collisions within the same timestamp directory by appending a counter suffix
- Supports listing, restoring, and cleaning up old backups

```bash
# List available backups
devsync template backup list

# Restore a specific backup
devsync template backup restore

# Clean up backups older than 30 days
devsync template backup cleanup --days 30
```

See the [Template Backup commands](../reference/cli-reference.md) for the full CLI reference.

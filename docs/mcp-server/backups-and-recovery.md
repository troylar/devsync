# Backups & Recovery

DevSync automatically backs up configuration files before modifying them. This applies to MCP config syncs, template installations, and package operations. If something goes wrong, you can list, inspect, and restore from any previous backup.

---

## How Backups Work

When DevSync writes to an AI tool's config file (e.g., `.cursor/mcp.json` or `claude_desktop_config.json`), it first copies the existing file to the backup directory. Each backup is timestamped and grouped by operation.

**Backup storage location:**

```
.devsync/backups/
  2026-02-15T103045/
    cursor_mcp.json
    claude_settings.local.json
  2026-02-14T091530/
    cursor_mcp.json
```

The timestamp format is `YYYY-MM-DDTHHMMSS` in local time.

---

## Automatic Backups

Backups are created automatically during these operations:

| Operation | What Gets Backed Up |
|-----------|-------------------|
| `devsync mcp sync` | AI tool MCP config files before overwrite |
| `devsync template install` | Existing instruction files that would be overwritten |
| `devsync package install` | All files that would be modified or replaced |
| AI merge flow | Full config state before merge is applied |

To skip backup creation for a specific operation:

```bash
devsync mcp sync --tool all --no-backup
```

!!! warning
    Skipping backups means you cannot roll back if the sync produces an undesirable result. Use `--no-backup` only when you are confident in the operation or have your own backup strategy.

---

## Listing Backups

```bash
devsync template backup list
```

Output:

```
Backups for current project:

Timestamp             Files    Size     Operation
2026-02-15 10:30:45   3        12 KB    mcp sync
2026-02-14 09:15:30   1        4 KB     mcp sync
2026-02-12 14:22:10   5        28 KB    package install
2026-02-10 08:45:00   2        8 KB     template install

Total: 4 backups, 52 KB
```

### Filtering

```bash
# List only MCP-related backups
devsync template backup list --type mcp

# List backups from a specific date range
devsync template backup list --since 2026-02-14

# JSON output
devsync template backup list --json
```

---

## Restoring from Backup

Restore all files from a specific backup:

```bash
devsync template backup restore 2026-02-15T103045
```

Output:

```
Restoring backup from 2026-02-15 10:30:45

Restored:
  .cursor/mcp.json
  .claude/settings.local.json

2 file(s) restored.
Current configs backed up to: .devsync/backups/2026-02-15T110000/
```

!!! info
    Restoring a backup creates a new backup of the current state first. This means you can always undo a restore operation.

### Selective Restore

Restore a specific file from a backup:

```bash
devsync template backup restore 2026-02-15T103045 --file cursor_mcp.json
```

### Dry Run

Preview what would be restored without making changes:

```bash
devsync template backup restore 2026-02-15T103045 --dry-run
```

---

## Cleanup

Old backups accumulate over time. The cleanup command removes backups older than a specified retention period.

```bash
# Remove backups older than 30 days (default)
devsync template backup cleanup

# Remove backups older than 7 days
devsync template backup cleanup --days 7

# Preview what would be removed
devsync template backup cleanup --dry-run
```

Output:

```
Cleaning up backups older than 30 days

Removed:
  2026-01-10T083000/ (3 files, 15 KB)
  2026-01-05T142200/ (1 file, 4 KB)

Freed 19 KB across 2 backup(s).
Remaining: 4 backup(s), 52 KB
```

---

## Backup Directory Structure

```
.devsync/
  backups/
    2026-02-15T103045/           # One directory per operation
      cursor_mcp.json            # Backed-up config files
      claude_settings.local.json
      manifest.json              # Metadata about the backup
    2026-02-14T091530/
      cursor_mcp.json
      manifest.json
```

The `manifest.json` in each backup directory records metadata:

```json title="manifest.json"
{
  "timestamp": "2026-02-15T10:30:45",
  "operation": "mcp_sync",
  "tool": "all",
  "files": [
    {
      "name": "cursor_mcp.json",
      "original_path": ".cursor/mcp.json",
      "size": 4096,
      "checksum": "sha256:abc123..."
    },
    {
      "name": "claude_settings.local.json",
      "original_path": ".claude/settings.local.json",
      "size": 8192,
      "checksum": "sha256:def456..."
    }
  ]
}
```

---

## Gitignore

The `.devsync/backups/` directory is automatically added to `.gitignore`. Backups are local to each developer's machine and should not be committed.

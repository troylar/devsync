# AI Merge Flow

AI merge flow uses an AI assistant -- connected via MCP -- to intelligently merge configuration changes instead of relying on simple overwrite or skip strategies. The assistant reads your current config, compares it with incoming changes, understands the intent behind both, and proposes a merge that preserves your customizations while incorporating updates.

!!! note "Forward-looking feature"
    AI merge flow depends on the `devsync-mcp` package. The workflow described here represents the planned design. Implementation details will be refined as `devsync-mcp` matures.

---

## Why AI-Assisted Merging?

Standard conflict resolution strategies have limitations:

| Strategy | Problem |
|----------|---------|
| **Skip** | You miss important updates from the upstream template |
| **Overwrite** | You lose local customizations |
| **Rename** | You accumulate duplicate files and must manually reconcile |

AI merge flow adds a fourth option: **understand both sides and produce an intelligent merge**.

Consider a team coding standard that you have customized for your project. When the team publishes an update, a simple overwrite destroys your customizations. A skip means you miss the update. An AI assistant can read both versions, identify what changed upstream, identify your local modifications, and produce a merged result that incorporates both.

---

## Workflow

### 1. Detect Changes

The AI assistant uses `devsync_compare_configs` to identify differences between your installed configuration and an incoming update.

```text
You: Update my backend MCP servers to the latest version.

AI: I'll check what changed. [calls devsync_compare_configs]

Found 3 differences in namespace 'backend':
- github server: args updated (mcp-server-github v1.2 -> v1.4)
- postgres server: new env var DATABASE_READONLY added
- redis server: newly added (not in your current config)
```

### 2. Analyze Conflicts

The assistant identifies which changes conflict with your local modifications and which can be applied cleanly.

```text
AI: Analyzing against your current configuration...

No conflicts:
- redis server: new addition, no local equivalent
- postgres DATABASE_READONLY: new variable, does not affect existing ones

Conflict detected:
- github server: you added custom args ["--org", "acme-corp"]
  Upstream changed args from [mcp-server-github] to [mcp-server-github, "--include-forks"]
```

### 3. Propose Merge Strategy

The assistant suggests how to handle each change based on context.

```text
AI: Here is my proposed merge:

1. github server: Merge args to include both your custom flags and the upstream update
   Result: [mcp-server-github, "--include-forks", "--org", "acme-corp"]

2. postgres server: Add DATABASE_READONLY with null (requires your credential)
   No existing config affected.

3. redis server: Add as new server.
   You will need to configure REDIS_URL.

Apply this merge? [yes/no/edit]
```

### 4. Apply Changes

After confirmation, the assistant uses `devsync_merge_config` to apply the changes and creates a backup of the previous state.

```text
You: Yes, apply it.

AI: [calls devsync_merge_config]

Merge complete:
- Backup created at .devsync/backups/2026-02-15T103045/
- 3 servers updated
- 1 new credential required: REDIS_URL

Run 'devsync mcp configure backend' to set REDIS_URL,
then 'devsync mcp sync --tool all' to push changes to your AI tools.
```

---

## Merge Strategies

The AI assistant can apply different strategies depending on the type of change:

### Additive Merge

New items (servers, environment variables, instructions) are added without affecting existing configuration. This is the default for non-conflicting changes.

### Selective Override

The upstream change replaces a specific field while preserving the rest. For example, updating a server's command version without changing custom arguments.

### Manual Resolution

For changes that cannot be automatically merged, the assistant presents both versions and asks the developer to choose or write a custom resolution.

---

## Safeguards

AI merge flow includes protections against destructive changes:

- **Automatic backups** are created before any merge operation. See [Backups & Recovery](backups-and-recovery.md).
- **Dry run mode** lets you preview the merge result without applying it.
- **Credential preservation** -- merge operations never modify `.devsync/.env` files. New credentials are flagged for manual configuration.
- **Rollback** -- if a merge produces an undesirable result, restore from the backup.

---

## Prerequisites

To use AI merge flow:

1. Install the `devsync-mcp` server package: `pip install devsync-mcp`
2. Register `devsync-mcp` as an MCP server in your AI tool (see [Tools Reference](tools-reference.md))
3. Have an AI assistant that supports MCP tool use (Claude Code, Cursor, etc.)

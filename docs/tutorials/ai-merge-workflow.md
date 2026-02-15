# AI-Assisted Configuration Merging

**Time to complete**: 20 minutes
**Difficulty**: Advanced
**Prerequisites**:

- DevSync installed (`pip install devsync`)
- Claude Code installed and configured
- Familiarity with DevSync templates and packages

!!! warning "Evolving feature"
    The AI-assisted merge workflow described in this tutorial is under active development. Commands, interfaces, and capabilities may change between releases. This tutorial reflects the intended workflow direction and will be updated as features stabilize.

## The Concept

As teams grow, configuration drift becomes a real problem. Different developers customize their AI assistant rules, new templates override old ones, and project-specific changes conflict with global standards. Manual merging of these configurations is tedious and error-prone.

**AI-assisted merging** uses the DevSync MCP server (`devsync-mcp`) to give your AI assistant direct access to your DevSync configuration. Instead of manually comparing files and resolving conflicts, you describe what you want in natural language and the AI handles the merge.

### When to Use AI Merge

| Situation | Traditional Approach | AI Merge Approach |
|-----------|---------------------|-------------------|
| Template update changes files you customized | Diff files manually, copy sections | Ask AI to merge keeping your customizations |
| Two template namespaces have overlapping rules | Read both, decide which takes precedence | Ask AI to reconcile and deduplicate |
| Migrating from one template repo to another | Uninstall old, install new, re-add custom changes | Ask AI to compare both and produce a merged version |
| Auditing installed configs against current standards | Open each file, compare to source | Ask AI to list all deviations from the source template |

---

## Step 1: Install devsync-mcp

The `devsync-mcp` package provides an MCP server that exposes DevSync operations as tools your AI assistant can call.

```bash
pip install devsync-mcp
```

Verify the installation:

```bash
devsync-mcp --version
```

---

## Step 2: Configure MCP in Claude Code

Add the DevSync MCP server to your Claude Code configuration. You can do this manually or use DevSync itself.

### Manual Configuration

Add the following to your Claude Code MCP settings (typically in `~/.claude/settings.json` or your project's `.claude/settings.local.json`):

```json
{
  "mcpServers": {
    "devsync": {
      "command": "devsync-mcp",
      "args": ["serve"],
      "env": {}
    }
  }
}
```

### Using DevSync

If your team distributes MCP configurations via DevSync, the `devsync-mcp` server may already be included in your team's MCP template:

```bash
devsync mcp sync --tool claude
```

After configuring, restart Claude Code to pick up the new MCP server.

### Verify MCP Connection

In Claude Code, ask:

```
What DevSync tools do you have access to?
```

The AI should respond with a list of available DevSync operations, such as listing templates, reading configuration files, and comparing versions.

---

## Step 3: Compare Configuration Changes

Suppose your team has pushed a new version of the standards template, but you have local customizations you want to keep. Use the AI to compare.

### Start the Conversation

In Claude Code, within your project directory:

```
I updated the team template namespace with `devsync template update team`.
Some of my local customizations in .claude/rules/ may have been overwritten.
Can you compare the current installed files against my Git history
to identify what changed?
```

The AI uses the DevSync MCP tools to:

1. Read the currently installed template files
2. Check Git history for your previous versions
3. Identify differences between the template source and your local modifications

### Example AI Response

```
I found 3 template files in the 'team' namespace. Here's the comparison:

1. team.python-standards.md
   - Template version: v1.2.0 (updated)
   - Your customization: Added a "Docstring Format" section (lines 45-62)
   - Status: Your customization was overwritten by the update

2. team.security-policy.md
   - Template version: v1.2.0 (unchanged from v1.1.0)
   - No local modifications detected
   - Status: No action needed

3. team.review-code.md
   - Template version: v1.2.0 (updated)
   - Your customization: Added "Performance" checklist section
   - Status: Your customization was overwritten by the update

Would you like me to merge your customizations back into the updated files?
```

---

## Step 4: Merge with AI Assistance

Ask the AI to perform the merge:

```
Yes, please merge my customizations back into the updated template files.
Keep the new template content as the base, and add my custom sections
where they don't conflict.
```

The AI will:

1. Read the updated template content
2. Retrieve your customizations from Git history
3. Merge the two versions, keeping template updates as the base
4. Add your custom sections in appropriate locations
5. Write the merged files back

### Example Merge Output

```
I've merged your customizations into the updated templates:

1. team.python-standards.md
   - Kept all v1.2.0 template updates
   - Re-added your "Docstring Format" section after the "Type Hints" section
   - No conflicts detected

3. team.review-code.md
   - Kept all v1.2.0 template updates (added "Accessibility" checklist)
   - Re-added your "Performance" checklist section
   - Note: The template now has a similar "Performance" section.
     I merged both, keeping the more detailed version (yours)
     and adding two items from the template version you didn't have.

Files written:
  .claude/rules/team.python-standards.md
  .claude/commands/team.review-code.md
```

---

## Step 5: Review and Approve

Always review AI-generated merges before committing. The AI does its best, but configuration files affect how your AI assistant behaves across all future interactions.

### Review the Changes

```bash
git diff .claude/
```

Or ask the AI to summarize:

```
Show me a summary of all changes you made, with before/after for each section.
```

### Approve and Commit

If the merge looks correct:

```bash
git add .claude/
git commit -m "chore: merge team template v1.2.0 with local customizations"
```

### Revert if Needed

If the merge introduced problems:

```bash
git checkout -- .claude/
```

Then try the merge again with more specific instructions:

```
Let's try the merge again for team.review-code.md. This time, keep my
Performance section exactly as-is and remove the template's version.
```

---

## Common AI Merge Workflows

### Deduplicate Overlapping Templates

When two namespaces contain similar rules:

```
I have templates installed from both the 'company' and 'backend' namespaces.
Some rules overlap (both have Python style guidelines).
Can you identify the overlapping content and suggest a consolidated version?
```

### Audit Against Source

Check if installed files have drifted from their source:

```
Compare all installed template files against their source repositories.
List any files where the installed version differs from the source.
```

### Migrate Between Template Repositories

When switching from one template source to another:

```
I'm migrating from the 'old-standards' namespace to 'new-standards'.
Both are installed. Can you:
1. Compare the two sets of templates
2. Identify what's new in 'new-standards' that 'old-standards' didn't have
3. Identify customizations I made to 'old-standards' that should carry over
4. Create a migration plan
```

---

## Limitations

- **AI merge is advisory**: The AI suggests and applies changes, but you should always review before committing. Configuration files directly affect AI behavior, so mistakes propagate.
- **No automatic conflict resolution**: When two sections genuinely conflict (contradictory rules), the AI will flag the conflict and ask for your decision rather than guessing.
- **Git history required**: The compare-and-merge workflow relies on Git history to identify your customizations. If you haven't been committing your configuration changes, the AI has less context to work with.
- **MCP server availability**: The `devsync-mcp` server must be running and connected. If Claude Code cannot reach it, the AI falls back to reading files directly (which works but loses some DevSync-specific context like namespace and version information).

---

## Next Steps

- [Create a Team Configuration Repository](team-config-repo.md) -- Set up the templates that feed into this merge workflow
- [Onboard a New Developer](onboard-new-developer.md) -- Complete onboarding walkthrough
- [Build and Distribute a Custom Package](custom-packages.md) -- Create multi-component packages

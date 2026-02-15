# Migrating Existing AI Configs to DevSync

**Time to complete**: 20 minutes
**Difficulty**: Intermediate
**Prerequisites**:

- DevSync installed (`pip install devsync`)
- Existing AI configuration files in one or more projects (e.g., `.cursor/rules/`, `.claude/rules/`, `AGENTS.md`)
- Git available for repository creation

## The Scenario

You have been using AI coding assistants for a while. Over time, you have accumulated configuration files -- cursor rules, claude instructions, copilot guidelines -- scattered across projects. Some were written by hand, some copied from colleagues, some downloaded from the internet. You want to bring these under DevSync management so they can be versioned, shared, and kept in sync.

## What You Will Learn

- How to audit your existing AI configuration files
- How to create a `templatekit.yaml` manifest from existing instructions
- How to create an `ai-config-kit-package.yaml` for complex setups with hooks and commands
- How to set up a Git repository for distribution
- How to handle the transition period on a team
- How to clean up old manual configurations

---

## Step 1: Audit Your Current Configuration Files

Start by finding all AI configuration files in your project. Check the standard directories:

```bash
# Claude Code
ls -la .claude/rules/ 2>/dev/null
ls -la .claude/commands/ 2>/dev/null
ls -la .claude/hooks/ 2>/dev/null

# Cursor
ls -la .cursor/rules/ 2>/dev/null

# Windsurf
ls -la .windsurf/rules/ 2>/dev/null

# GitHub Copilot
ls -la .github/instructions/ 2>/dev/null

# Cline
ls -la .clinerules/ 2>/dev/null

# Codex CLI
ls -la AGENTS.md 2>/dev/null
```

Make a list of what you find. For example:

```
Found:
  .claude/rules/coding-standards.md
  .claude/rules/api-conventions.md
  .claude/commands/review-pr.md
  .cursor/rules/coding-standards.mdc
  .cursor/rules/api-conventions.mdc
```

!!! info "Duplicate content across IDEs"
    It is common to find the same instructions duplicated across IDE directories with minor format differences. DevSync eliminates this duplication by maintaining a single source and translating to each IDE's format during installation.

---

## Step 2: Organize Files into a Template Repository

Create a new directory for your template repository and copy your existing instruction files into it:

```bash
mkdir -p my-templates/templates/rules
mkdir -p my-templates/templates/commands
```

Copy your instruction files. Use the Markdown (`.md`) versions as the canonical source, since DevSync converts to other formats automatically:

```bash
cp .claude/rules/coding-standards.md my-templates/templates/rules/
cp .claude/rules/api-conventions.md my-templates/templates/rules/
cp .claude/commands/review-pr.md my-templates/templates/commands/
```

!!! warning "Cursor .mdc files"
    If you only have `.mdc` files from Cursor and no `.md` equivalents, rename the copies to `.md`. The `.mdc` format is similar to Markdown, but you may need to remove any Cursor-specific frontmatter (lines between `---` markers at the top of the file) to create a clean portable version.

Your directory should now look like this:

```
my-templates/
└── templates/
    ├── rules/
    │   ├── coding-standards.md
    │   └── api-conventions.md
    └── commands/
        └── review-pr.md
```

---

## Step 3: Create the templatekit.yaml Manifest

Create `my-templates/templatekit.yaml` to describe your instructions:

```yaml
name: my-team-templates
version: 1.0.0
description: Team coding standards and workflows migrated from existing configs

templates:
  - name: coding-standards
    description: Language-agnostic coding conventions and formatting rules
    ide: claude
    files:
      - path: .claude/rules/coding-standards.md
        type: instruction
    tags: [standards, style]

  - name: api-conventions
    description: REST API design patterns and naming conventions
    ide: claude
    files:
      - path: .claude/rules/api-conventions.md
        type: instruction
    tags: [api, rest, design]

  - name: review-pr
    description: Structured pull request review checklist
    ide: claude
    files:
      - path: .claude/commands/review-pr.md
        type: command
    tags: [review, workflow]
```

!!! tip "Map your existing files"
    Each entry in `templates` corresponds to one of your existing instruction files. The `name` should be descriptive and kebab-cased. The `files.path` defines where DevSync will install the file in target projects.

---

## Step 4: Create a Package for Complex Setups (Optional)

If your existing configuration includes more than just instruction files -- for example, hooks, shell commands, or MCP server configurations -- create an `ai-config-kit-package.yaml` instead of (or in addition to) the template manifest.

```yaml
name: my-team-package
version: 1.0.0
description: Complete team configuration including standards, hooks, and commands
author: Your Team
license: MIT

components:
  instructions:
    - name: coding-standards
      file: instructions/coding-standards.md
      description: Language-agnostic coding conventions
      tags: [standards, style]

    - name: api-conventions
      file: instructions/api-conventions.md
      description: REST API design patterns
      tags: [api, design]

  hooks:
    - name: pre-commit-lint
      file: hooks/pre-commit-lint.sh
      description: Run linting before each commit
      hook_type: pre-commit

  commands:
    - name: review-pr
      file: commands/review-pr.md
      description: Structured PR review checklist
      command_type: slash

  resources:
    - name: editorconfig
      file: resources/.editorconfig
      description: Editor configuration for consistent formatting
```

The package directory structure:

```
my-team-package/
├── ai-config-kit-package.yaml
├── instructions/
│   ├── coding-standards.md
│   └── api-conventions.md
├── hooks/
│   └── pre-commit-lint.sh
├── commands/
│   └── review-pr.md
└── resources/
    └── .editorconfig
```

!!! info "Packages vs. templates"
    Use a `templatekit.yaml` for instruction-only setups. Use `ai-config-kit-package.yaml` when you need to bundle hooks, commands, MCP servers, or resource files alongside instructions. Both can be distributed via Git.

---

## Step 5: Set Up the Git Repository

Initialize the repository and push it to GitHub:

```bash
cd my-templates
git init
git add .
git commit -m "feat: initial migration of team AI configurations"
```

Create the remote repository:

```bash
gh repo create your-org/team-ai-configs --private --source=. --remote=origin --push
```

Tag the first version:

```bash
git tag -a v1.0.0 -m "v1.0.0: Initial migration from manual configs"
git push origin v1.0.0
```

!!! tip "Reference structure"
    See [troylar/devsync-starter-templates](https://github.com/troylar/devsync-starter-templates) for an example of a well-structured template repository. Use it as a reference for directory layout and manifest format.

---

## Step 6: Install from the New Repository

Test the installation in a project to verify everything works:

```bash
cd ~/projects/my-project

# For template repositories
devsync template install https://github.com/your-org/team-ai-configs --as team

# For package repositories
aiconfig package install https://github.com/your-org/team-ai-configs --ide claude
```

Expected output for a template install:

```
Installing templates from https://github.com/your-org/team-ai-configs...
Namespace: team

Installed:
  team.coding-standards  -> .claude/rules/team.coding-standards.md
  team.api-conventions   -> .claude/rules/team.api-conventions.md
  team.review-pr         -> .claude/commands/team.review-pr.md

3 templates installed successfully.
```

Verify by listing installed templates:

```bash
devsync template list
```

---

## Step 7: Distribute to Your Team

Share the repository URL with your team. Provide clear instructions in your project README or onboarding docs:

```markdown
## AI Assistant Setup

Install team coding standards for your AI assistant:

    devsync template install https://github.com/your-org/team-ai-configs --as team

This installs coding standards, API conventions, and review commands
to your AI assistant's configuration directory.
```

### Handling the Transition Period

Not every team member will adopt DevSync on the same day. During the transition:

1. **Keep manual configs committed.** Do not delete `.claude/rules/` or `.cursor/rules/` files from the repository immediately. Team members who have not installed DevSync still need them.

2. **Add a deprecation notice.** Add a comment to the top of manually maintained config files:

    ```markdown
    <!-- DEPRECATED: This file is now managed by DevSync.
         Install with: devsync template install https://github.com/your-org/team-ai-configs --as team
         This file will be removed in a future update. -->
    ```

3. **Set a migration deadline.** Announce a date by which all team members should have DevSync installed. After that date, remove the manually maintained config files.

4. **Use CI enforcement.** Once most of the team has migrated, add a [CI check](ci-cd-integration.md) that validates DevSync installations. Start with warnings, then switch to blocking.

!!! warning "Namespace conflicts"
    If team members have existing files with the same names as DevSync-managed ones, they will encounter conflicts during installation. Use `--conflict overwrite` to replace old files, or `--conflict rename` to keep both during the transition.

---

## Step 8: Clean Up Old Manual Configs

Once the entire team has migrated to DevSync, remove the old manually maintained configuration files:

```bash
# Remove old manual configs (DevSync now manages these)
git rm .claude/rules/coding-standards.md
git rm .claude/rules/api-conventions.md
git rm .claude/commands/review-pr.md
git rm .cursor/rules/coding-standards.mdc
git rm .cursor/rules/api-conventions.mdc

git commit -m "chore: remove manually maintained AI configs, now managed by DevSync"
```

After this commit, the only AI configuration files in the project will be the ones installed and tracked by DevSync.

Verify the clean state:

```bash
devsync template list
```

```
Installed Templates:

Namespace   Name                Type         Scope    Source
team        coding-standards    instruction  project  github.com/your-org/team-ai-configs
team        api-conventions     instruction  project  github.com/your-org/team-ai-configs
team        review-pr           command      project  github.com/your-org/team-ai-configs
```

---

## Troubleshooting

### "Namespace already exists" during install

A previous installation attempt may have partially completed. Use `--force` to overwrite:

```bash
devsync template install https://github.com/your-org/team-ai-configs --as team --force
```

### Cursor files not working after migration

Ensure you are installing to Cursor specifically:

```bash
aiconfig install coding-standards --tool cursor
```

DevSync automatically converts `.md` source files to `.mdc` format for Cursor. If conversion fails, check that the source Markdown does not contain syntax that is incompatible with the `.mdc` format.

### Existing files conflict with DevSync installations

During the transition, you may have both manually created and DevSync-managed files. Use `--conflict rename` to keep both:

```bash
aiconfig install coding-standards --tool claude --conflict rename
```

This installs the DevSync version alongside the existing file so you can compare them before removing the old one.

### Team members see different instruction versions

This usually means the local library is out of date. Have each team member update:

```bash
aiconfig update your-org/team-ai-configs
```

Then reinstall:

```bash
devsync template install https://github.com/your-org/team-ai-configs --as team --force
```

### Package install skips some components

Different IDEs support different component types. For example, Cursor only supports instructions and resources -- hooks and commands will be skipped. Check the [IDE capability matrix](multi-ide-workflow.md#step-4-understand-file-format-differences) to see what each IDE supports.

---

## Next Steps

- [Create a Team Configuration Repository](team-config-repo.md) -- Build a more comprehensive template repository from scratch
- [Enforcing DevSync Standards in CI/CD](ci-cd-integration.md) -- Automate compliance checks in your CI pipeline
- [Build and Distribute a Custom Package](custom-packages.md) -- Create packages with MCP servers, hooks, and more

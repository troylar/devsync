# Create a Team Configuration Repository

**Time to complete**: 25 minutes
**Difficulty**: Intermediate
**Prerequisites**:

- DevSync installed (`pip install devsync`)
- Git and GitHub CLI (`gh`) available
- A GitHub organization or personal account for hosting

## What You Will Build

A Git-hosted configuration repository containing coding standards, slash commands, and hooks that your entire team can install with a single command. By the end of this tutorial, any team member can run:

```bash
devsync template install https://github.com/troylar/devsync-starter-templates --as team
```

...and immediately have your team's conventions loaded into their AI assistant.

## What You Will Learn

- How to scaffold a template repository with `devsync template init`
- The structure of a `templatekit.yaml` manifest
- How to write instructions, commands, and hooks
- How to publish and distribute templates via Git
- How to update templates and sync changes across the team

---

## Step 1: Initialize the Template Repository

Use `devsync template init` to scaffold a new template repository. This creates a directory with the correct structure and a starter manifest.

```bash
cd ~/projects
devsync template init my-team-standards
```

This creates the following directory structure:

```
my-team-standards/
├── templatekit.yaml          # Manifest describing all templates
├── templates/
│   ├── rules/                # Instruction files (coding standards, guidelines)
│   │   └── example-rule.md
│   ├── commands/             # Slash commands (e.g., /review-code)
│   │   └── example-command.md
│   └── hooks/                # Hooks (pre-prompt, post-prompt automation)
│       └── example-hook.md
└── README.md
```

Enter the directory and inspect the generated manifest:

```bash
cd my-team-standards
```

The generated `templatekit.yaml` looks like this:

```yaml
name: my-team-standards
version: 1.0.0
description: Template repository created with DevSync

templates:
  - name: example-rule
    description: An example instruction rule
    ide: claude
    files:
      - path: .claude/rules/example-rule.md
        type: instruction
    tags: [example]
```

!!! info "About the manifest"
    The `templatekit.yaml` file is the source of truth for your template repository. It declares every template, its target IDE, the files it installs, and metadata like tags and descriptions. DevSync reads this file during `template install` to know what to copy and where.

---

## Step 2: Add a Coding Standards Instruction

Replace the example rule with a real coding standards instruction. Create a Python style guide that your AI assistant will follow.

Create the file `templates/rules/python-standards.md`:

```markdown
# Python Coding Standards

All Python code in this project must follow these conventions.

## Formatting and Style

- Use **black** for formatting with a line length of 120 characters.
- Use **ruff** for linting with rule sets E, F, I, N, W.
- Use **mypy** in strict mode for type checking.

## Type Hints

All functions must include type hints for parameters and return values:

```python
def calculate_total(items: list[dict[str, float]], tax_rate: float = 0.0) -> float:
    """Calculate the total price including tax."""
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    return subtotal * (1 + tax_rate)
```

## Naming Conventions

- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private attributes: `_leading_underscore`

## Error Handling

- Use specific exception types, never bare `except:` or `except Exception:`.
- Log errors with context before re-raising.
- Include relevant identifiers (user ID, request ID) in error messages.

```python
import logging

logger = logging.getLogger(__name__)

def fetch_user(user_id: int) -> User:
    try:
        return db.query(User).filter_by(id=user_id).one()
    except NoResultFound:
        logger.warning("User not found", extra={"user_id": user_id})
        raise UserNotFoundError(f"No user with id={user_id}")
```

## Imports

Order imports in three groups separated by blank lines:

1. Standard library
2. Third-party packages
3. Local application modules

```python
import os
from pathlib import Path

import requests
from pydantic import BaseModel

from myapp.models import User
from myapp.utils import format_date
```

## Testing

- Every public function must have at least one test.
- Use the Arrange-Act-Assert pattern.
- Minimum 80% test coverage for new code.
```

Now update `templatekit.yaml` to reference this file instead of the example:

```yaml
name: my-team-standards
version: 1.0.0
description: Team coding standards and workflow automation

templates:
  - name: python-standards
    description: Python coding conventions (formatting, types, naming, errors)
    ide: claude
    files:
      - path: .claude/rules/python-standards.md
        type: instruction
    tags: [python, style, standards]
```

Remove the old example file:

```bash
rm templates/rules/example-rule.md
```

---

## Step 3: Add a Slash Command

Slash commands are markdown files that define reusable prompts your AI assistant can execute. Add a `/review-code` command that performs a structured code review.

Create the file `templates/commands/review-code.md`:

```markdown
# /review-code

Review the current file or selection against team standards. Check each category and report findings.

## Checklist

### Correctness
- Does the code do what the function/class name suggests?
- Are edge cases handled (empty inputs, None values, boundary conditions)?
- Are there off-by-one errors or incorrect boolean logic?

### Error Handling
- Are specific exception types used (not bare `except:`)?
- Are errors logged with context before re-raising?
- Do error messages include relevant identifiers?

### Type Safety
- Do all functions have parameter and return type hints?
- Are Optional types used where values can be None?
- Would mypy pass in strict mode?

### Testing
- Is there a corresponding test for each public function?
- Do tests cover both success and failure paths?
- Is the Arrange-Act-Assert pattern followed?

### Style
- Does naming follow snake_case (functions/variables) and PascalCase (classes)?
- Are imports ordered: stdlib, third-party, local?
- Is the line length within 120 characters?

## Output Format

For each category, report:
- **Pass**: Requirements met
- **Issue**: Describe the problem and suggest a fix
- **N/A**: Category does not apply

Summarize with a count of issues found and their severity (critical, warning, suggestion).
```

Update `templatekit.yaml` to include the command:

```yaml
name: my-team-standards
version: 1.0.0
description: Team coding standards and workflow automation

templates:
  - name: python-standards
    description: Python coding conventions (formatting, types, naming, errors)
    ide: claude
    files:
      - path: .claude/rules/python-standards.md
        type: instruction
    tags: [python, style, standards]

  - name: review-code
    description: Structured code review against team standards
    ide: claude
    files:
      - path: .claude/commands/review-code.md
        type: command
    tags: [review, quality, workflow]
```

Remove the old example files:

```bash
rm templates/commands/example-command.md
rm templates/hooks/example-hook.md
```

---

## Step 4: Validate the Repository

Before publishing, validate that the manifest and file references are correct:

```bash
devsync template validate .
```

Expected output:

```
Validating template repository...

Templates found: 2
  python-standards (instruction) -- templates/rules/python-standards.md
  review-code (command) -- templates/commands/review-code.md

All files referenced in templatekit.yaml exist.
Validation passed.
```

!!! warning "Fix before publishing"
    If validation reports missing files or manifest errors, fix them before pushing. Team members who install a broken repository will get confusing errors.

---

## Step 5: Push to Git

Initialize the repository, commit, and push to GitHub:

```bash
git init
git add .
git commit -m "feat: initial team standards with Python conventions and review command"

gh repo create troylar/devsync-starter-templates --public --source=. --remote=origin --push
```

!!! tip "Private repositories"
    For proprietary team standards, use `--private` instead of `--public`. Team members will need read access to the repository.

Tag the first release:

```bash
git tag -a v1.0.0 -m "Release v1.0.0: Python standards and review command"
git push origin v1.0.0
```

---

## Step 6: Team Members Install

Share the installation command with your team. Each member runs this in their project directory:

```bash
cd ~/projects/my-project
devsync template install https://github.com/troylar/devsync-starter-templates --as team
```

Expected output:

```
Installing templates from https://github.com/troylar/devsync-starter-templates...
Namespace: team

Installed:
  team.python-standards -> .claude/rules/team.python-standards.md
  team.review-code      -> .claude/commands/team.review-code.md

2 templates installed successfully.
```

The namespace prefix (`team.`) prevents conflicts if team members also have personal templates installed.

### Installing with Global Scope

For standards that should apply across all projects (not just one), use the `--scope global` flag:

```bash
devsync template install https://github.com/troylar/devsync-starter-templates --as team --scope global
```

This installs to `~/.claude/rules/` instead of the project-level `.claude/rules/`.

### Verify the Installation

```bash
devsync template list
```

Expected output:

```
Installed Templates:

Namespace   Name                Type         Scope    Source
team        python-standards    instruction  project  github.com/troylar/devsync-starter-templates
team        review-code         command      project  github.com/troylar/devsync-starter-templates
```

---

## Step 7: Update and Sync Changes

When standards evolve, the team lead updates the repository and team members sync.

### Team Lead: Push an Update

Edit `templates/rules/python-standards.md` to add a new section, then bump the version:

```yaml
# In templatekit.yaml
version: 1.1.0
```

Commit and push:

```bash
git add .
git commit -m "feat: add docstring requirements to Python standards"
git tag -a v1.1.0 -m "Release v1.1.0: Added docstring requirements"
git push origin main --tags
```

### Team Members: Pull the Update

Each team member updates their installation:

```bash
cd ~/projects/my-project
devsync template update team
```

Expected output:

```
Updating namespace 'team' from https://github.com/troylar/devsync-starter-templates...

Updated:
  team.python-standards  (1.0.0 -> 1.1.0)

1 template updated.
```

To update all installed template namespaces at once:

```bash
devsync template update --all
```

---

## Final Repository Structure

After completing all steps, your repository looks like this:

```
my-team-standards/
├── templatekit.yaml
├── templates/
│   ├── rules/
│   │   └── python-standards.md
│   └── commands/
│       └── review-code.md
└── README.md
```

And in each team member's project:

```
my-project/
├── .claude/
│   ├── rules/
│   │   └── team.python-standards.md
│   └── commands/
│       └── team.review-code.md
├── .devsync/
│   └── installations.json
└── ... (project files)
```

---

## Troubleshooting

### "Template namespace 'team' already exists"

This means the namespace is already installed. Use `--force` to overwrite:

```bash
devsync template install https://github.com/troylar/devsync-starter-templates --as team --force
```

### Files not appearing after install

Check that the `templatekit.yaml` `files.path` values match where your IDE looks for configuration. For Claude Code, instructions go in `.claude/rules/` and commands in `.claude/commands/`.

```bash
ls -la .claude/rules/
ls -la .claude/commands/
```

### Team member cannot access private repository

Ensure the team member has read access to the GitHub repository and their Git credentials are configured:

```bash
gh auth status
```

---

## Next Steps

- [Onboard a New Developer](onboard-new-developer.md) -- Full onboarding walkthrough using templates and MCP
- [Build and Distribute a Custom Package](custom-packages.md) -- Create multi-component packages with MCP servers, hooks, and more
- [AI-Assisted Configuration Merging](ai-merge-workflow.md) -- Use AI to compare and merge configuration changes

# Build and Distribute a Custom Package

**Time to complete**: 30 minutes
**Difficulty**: Intermediate
**Prerequisites**:

- DevSync installed (`pip install devsync`)
- Familiarity with YAML syntax
- At least one AI coding assistant installed

## What You Will Build

A complete DevSync package containing:

- **Instructions** -- Coding guidelines your AI assistant follows
- **An MCP server config** -- External tool integration with credential management
- **A pre-commit hook** -- Automated checks before each commit
- **A slash command** -- A reusable task your AI assistant can execute
- **A resource file** -- A static configuration file installed to the project root

By the end, you will have a distributable package that any team member can install with one command.

## What You Will Learn

- The full `ai-config-kit-package.yaml` manifest format
- How to write each component type
- How to handle credentials securely
- How to test packages locally
- How to distribute packages via Git

---

## Step 1: Create the Directory Structure

Start by creating the package directory with subdirectories for each component type:

```bash
mkdir -p my-package/{instructions,mcp,hooks,commands,resources}
cd my-package
```

The resulting structure:

```
my-package/
├── instructions/     # AI assistant guidelines
├── mcp/              # MCP server configurations
├── hooks/            # Git and workflow hooks
├── commands/         # Slash commands and scripts
└── resources/        # Static files (configs, templates)
```

---

## Step 2: Write the Package Manifest

Create `ai-config-kit-package.yaml` at the root of your package. This file declares every component, its location, and its metadata.

```yaml
name: backend-dev-kit
version: 1.0.0
description: Backend development standards with tooling, hooks, and commands
author: Backend Team
license: MIT
namespace: troylar/devsync-python-package

components:
  instructions:
    - name: api-design
      file: instructions/api-design.md
      description: REST API design conventions and patterns
      tags: [api, rest, design]

    - name: database-patterns
      file: instructions/database-patterns.md
      description: Database query patterns and ORM conventions
      tags: [database, orm, sql]

  mcp_servers:
    - name: github-integration
      file: mcp/github.json
      description: GitHub API access for PR reviews and issue management
      credentials:
        - name: GITHUB_PERSONAL_ACCESS_TOKEN
          description: GitHub token with repo and read:org scopes
          required: true

  hooks:
    - name: pre-commit-checks
      file: hooks/pre-commit.sh
      description: Run linting, type checking, and tests before commits
      hook_type: pre-commit

  commands:
    - name: run-tests
      file: commands/run-tests.sh
      description: Execute the test suite with coverage reporting
      command_type: shell

  resources:
    - name: editorconfig
      file: resources/.editorconfig
      description: Editor configuration for consistent formatting
      checksum: sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
      size: 350
```

!!! info "Manifest field reference"
    - **name**: Package identifier. Use lowercase with hyphens.
    - **version**: Semantic version (major.minor.patch).
    - **namespace**: Unique identifier, typically `org/package-name`.
    - **components**: Contains one or more of: `instructions`, `mcp_servers`, `hooks`, `commands`, `resources`.
    - **credentials**: For MCP servers, declares required environment variables. `required: true` means the user must provide a value during configuration.

---

## Step 3: Add Instruction Files

Instructions are markdown files that tell your AI assistant how to behave. Create two instructions for this package.

### API Design Instruction

Create `instructions/api-design.md`:

```markdown
# REST API Design Conventions

Follow these conventions for all REST API endpoints in this project.

## URL Structure

- Use plural nouns for resources: `/users`, `/orders`, `/products`
- Use kebab-case for multi-word resources: `/order-items`, `/user-profiles`
- Nest related resources: `/users/{id}/orders`
- Limit nesting to two levels maximum

## HTTP Methods

| Method | Purpose | Example | Response Code |
|--------|---------|---------|---------------|
| GET | Retrieve resource(s) | `GET /users/123` | 200 |
| POST | Create a resource | `POST /users` | 201 |
| PUT | Full update | `PUT /users/123` | 200 |
| PATCH | Partial update | `PATCH /users/123` | 200 |
| DELETE | Remove a resource | `DELETE /users/123` | 204 |

## Response Format

All responses use a consistent envelope:

```json
{
  "data": {},
  "meta": {
    "request_id": "uuid",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

Error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      {"field": "email", "message": "Invalid email format"}
    ]
  },
  "meta": {
    "request_id": "uuid"
  }
}
```

## Pagination

Use cursor-based pagination for list endpoints:

```
GET /users?cursor=abc123&limit=25
```

Response includes pagination metadata:

```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "def456",
    "has_more": true,
    "limit": 25
  }
}
```

## When writing API code:

1. Always validate request body with Pydantic models
2. Return appropriate HTTP status codes
3. Include request_id in all responses for tracing
4. Use cursor-based pagination, not offset-based
5. Document endpoints with OpenAPI docstrings
```

### Database Patterns Instruction

Create `instructions/database-patterns.md`:

```markdown
# Database Query Patterns

Follow these patterns for all database operations.

## Query Construction

Use the ORM for standard queries. Drop to raw SQL only for complex aggregations
or performance-critical paths.

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

def get_active_users(session: Session, limit: int = 100) -> list[User]:
    """Retrieve active users ordered by last login."""
    stmt = (
        select(User)
        .where(User.is_active == True)
        .order_by(User.last_login.desc())
        .limit(limit)
    )
    return list(session.scalars(stmt))
```

## Transaction Boundaries

Keep transactions short. Open a session, do the work, commit or rollback:

```python
async def create_order(order_data: OrderCreate) -> Order:
    """Create an order within a single transaction."""
    async with async_session() as session:
        async with session.begin():
            order = Order(**order_data.model_dump())
            session.add(order)
        await session.refresh(order)
    return order
```

## N+1 Query Prevention

Always use eager loading for known relationships:

```python
stmt = (
    select(Order)
    .options(selectinload(Order.items))
    .where(Order.user_id == user_id)
)
```

## When writing database code:

1. Use the ORM unless raw SQL is justified with a comment
2. Eager-load relationships to avoid N+1 queries
3. Keep transactions as short as possible
4. Add database indexes for columns used in WHERE and ORDER BY
5. Use type hints for all query functions
```

---

## Step 4: Add an MCP Server Configuration

MCP server configurations allow your AI assistant to interact with external services. Create a GitHub integration that enables PR reviews and issue management.

Create `mcp/github.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

The `${GITHUB_PERSONAL_ACCESS_TOKEN}` placeholder is resolved at sync time from the credentials stored in `.devsync/.env`. The manifest's `credentials` section (Step 2) tells DevSync to prompt the user for this value during `devsync mcp configure`.

!!! warning "Credential security"
    Never hardcode tokens or passwords in MCP configuration files. Always use environment variable placeholders. DevSync stores credentials in `.devsync/.env` which is automatically gitignored.

!!! note "IDE compatibility"
    MCP server components are only installed for IDEs that support them. Currently, Claude Code supports MCP servers. For other IDEs (Cursor, Windsurf, Cline), MCP components are skipped during installation and counted separately in the output.

---

## Step 5: Add a Pre-Commit Hook

Hooks are scripts that run automatically at specific points in your workflow. Create a pre-commit hook that runs linting and type checking.

Create `hooks/pre-commit.sh`:

```bash
#!/usr/bin/env bash
set -e

echo "Running pre-commit checks..."

FAILED=0

# Linting
echo "  Checking lint (ruff)..."
if command -v ruff &> /dev/null; then
    if ! ruff check . --quiet; then
        echo "  FAIL: Linting errors found. Run 'ruff check --fix .' to auto-fix."
        FAILED=1
    else
        echo "  OK: Lint passed."
    fi
else
    echo "  SKIP: ruff not installed."
fi

# Type checking
echo "  Checking types (mypy)..."
if command -v mypy &> /dev/null; then
    if ! mypy . --quiet; then
        echo "  FAIL: Type errors found."
        FAILED=1
    else
        echo "  OK: Types passed."
    fi
else
    echo "  SKIP: mypy not installed."
fi

# Formatting
echo "  Checking format (black)..."
if command -v black &> /dev/null; then
    if ! black --check --quiet .; then
        echo "  FAIL: Formatting issues. Run 'black .' to fix."
        FAILED=1
    else
        echo "  OK: Format passed."
    fi
else
    echo "  SKIP: black not installed."
fi

if [ "$FAILED" -ne 0 ]; then
    echo ""
    echo "Pre-commit checks failed. Fix the issues above before committing."
    exit 1
fi

echo ""
echo "All pre-commit checks passed."
```

Make the script executable:

```bash
chmod +x hooks/pre-commit.sh
```

---

## Step 6: Add a Test Command

Commands are reusable scripts your AI assistant (or developers) can execute. Create a test runner command.

Create `commands/run-tests.sh`:

```bash
#!/usr/bin/env bash
set -e

COVERAGE_THRESHOLD="${1:-80}"

echo "Running test suite..."
echo "Coverage threshold: ${COVERAGE_THRESHOLD}%"
echo ""

if ! command -v pytest &> /dev/null; then
    echo "Error: pytest is not installed."
    echo "Install with: pip install pytest pytest-cov"
    exit 1
fi

pytest \
    --cov=. \
    --cov-report=term-missing \
    --cov-report=html:htmlcov \
    --cov-fail-under="$COVERAGE_THRESHOLD" \
    -v \
    "$@"

echo ""
echo "Test suite passed."
echo "Coverage report: htmlcov/index.html"
```

Make the script executable:

```bash
chmod +x commands/run-tests.sh
```

---

## Step 7: Add a Resource File

Resources are static configuration files installed directly into the project. Create an `.editorconfig` that enforces consistent editor settings.

Create `resources/.editorconfig`:

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true

[*.py]
indent_size = 4
max_line_length = 120

[*.{yaml,yml}]
indent_size = 2

[*.{json,js,ts,tsx}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

---

## Step 8: Review the Final Structure

Your package directory should now look like this:

```
my-package/
├── ai-config-kit-package.yaml
├── instructions/
│   ├── api-design.md
│   └── database-patterns.md
├── mcp/
│   └── github.json
├── hooks/
│   └── pre-commit.sh
├── commands/
│   └── run-tests.sh
└── resources/
    └── .editorconfig
```

---

## Step 9: Test Locally

Navigate to a test project and install the package. Use an absolute or relative path to the package directory.

```bash
cd ~/projects/test-project
devsync package install /path/to/my-package --ide claude
```

Expected output:

```
Installing package: backend-dev-kit v1.0.0

Installed components:
  api-design           (instruction)  -> .claude/rules/api-design.md
  database-patterns    (instruction)  -> .claude/rules/database-patterns.md
  github-integration   (mcp_server)   -> .claude/mcp/github.json
  pre-commit-checks    (hook)         -> .claude/hooks/pre-commit.sh
  run-tests            (command)      -> .claude/commands/run-tests.sh
  editorconfig         (resource)     -> .editorconfig

6/6 components installed.

Package 'backend-dev-kit' installed successfully.
```

Verify with:

```bash
devsync package list
```

Expected output:

```
Installed Packages:

Package           Version  Status      Components  Installed
backend-dev-kit   1.0.0    complete    6           2025-01-15 10:30:00
```

### Test on a Different IDE

Install to Cursor to see how component filtering works:

```bash
devsync package install /path/to/my-package --ide cursor
```

```
Installing package: backend-dev-kit v1.0.0

Installed components:
  api-design           (instruction)  -> .cursor/rules/api-design.mdc
  database-patterns    (instruction)  -> .cursor/rules/database-patterns.mdc
  editorconfig         (resource)     -> .editorconfig

3/6 components installed.
Skipped 3 components (not supported by Cursor):
  github-integration (mcp_server)
  pre-commit-checks  (hook)
  run-tests          (command)

Package 'backend-dev-kit' installed with status: partial.
```

!!! info "IDE capability differences"
    Different IDEs support different component types. Instructions and resources are broadly supported. MCP servers, hooks, and commands are currently supported by Claude Code and (partially) Roo Code. Unsupported components are skipped, not treated as errors.

### Test Conflict Resolution

If you install the same package again, DevSync detects the existing installation:

```bash
# Skip existing files (default)
devsync package install /path/to/my-package --ide claude --conflict skip

# Overwrite existing files
devsync package install /path/to/my-package --ide claude --conflict overwrite

# Rename new files to avoid conflicts
devsync package install /path/to/my-package --ide claude --conflict rename

# Force reinstall (uninstalls first, then installs fresh)
devsync package install /path/to/my-package --ide claude --force
```

### Test Uninstallation

```bash
devsync package uninstall backend-dev-kit
```

```
Uninstalling package: backend-dev-kit

Removed:
  .claude/rules/api-design.md
  .claude/rules/database-patterns.md
  .claude/mcp/github.json
  .claude/hooks/pre-commit.sh
  .claude/commands/run-tests.sh
  .editorconfig

Package 'backend-dev-kit' uninstalled. 6 files removed.
```

---

## Step 10: Distribute the Package

### Option A: Git Repository (Recommended)

Push the package to a Git repository for version-controlled distribution:

```bash
cd my-package
git init
git add .
git commit -m "feat: initial backend-dev-kit package v1.0.0"
git tag -a v1.0.0 -m "Release v1.0.0"

gh repo create troylar/devsync-python-package --private --source=. --remote=origin --push
git push origin v1.0.0
```

Team members install directly from the repository URL:

```bash
devsync package install https://github.com/troylar/devsync-python-package --ide claude
```

### Option B: Shared Directory

Copy the package to a network share or shared filesystem:

```bash
cp -r my-package /mnt/shared/ai-packages/backend-dev-kit
```

Team members install from the shared path:

```bash
devsync package install /mnt/shared/ai-packages/backend-dev-kit --ide claude
```

### Option C: Embed in Project Repository

Include the package directly in your project repository:

```bash
cp -r my-package ~/projects/backend-api/.ai-packages/backend-dev-kit
cd ~/projects/backend-api
git add .ai-packages/
git commit -m "chore: add backend-dev-kit AI configuration package"
```

New developers install after cloning:

```bash
git clone https://github.com/your-org/backend-api
cd backend-api
devsync package install .ai-packages/backend-dev-kit --ide claude
```

---

## How Team Members Install

Share this with your team:

```bash
# Install the package (replace URL with your repository)
devsync package install https://github.com/troylar/devsync-python-package --ide claude

# If the package includes MCP servers, configure credentials
devsync mcp configure your-org

# Sync MCP to AI tools
devsync mcp sync --tool all

# Verify
devsync package list
```

When the package is updated, team members can reinstall:

```bash
devsync package install https://github.com/troylar/devsync-python-package --ide claude --force
```

---

## Troubleshooting

### "Manifest validation failed"

Check that `ai-config-kit-package.yaml` has all required fields (`name`, `version`, `description`, `author`, `namespace`) and that all `file` paths reference files that exist in the package directory.

### "Component file not found"

The `file` path in the manifest is relative to the package root. Verify the file exists:

```bash
ls -la instructions/api-design.md
```

### "Package already installed"

Use `--force` to overwrite or `--conflict overwrite` to replace individual files:

```bash
devsync package install ./my-package --ide claude --force
```

### MCP credentials not prompting

Ensure the `credentials` section in the manifest lists the required environment variables:

```yaml
credentials:
  - name: GITHUB_PERSONAL_ACCESS_TOKEN
    description: GitHub token with repo scope
    required: true
```

### Hook not executing

Verify the hook file is executable:

```bash
chmod +x hooks/pre-commit.sh
```

After installation, check the installed copy:

```bash
ls -la .claude/hooks/pre-commit.sh
```

---

## Next Steps

- [Create a Team Configuration Repository](team-config-repo.md) -- Distribute templates (a lighter-weight alternative to packages)
- [Onboard a New Developer](onboard-new-developer.md) -- Use packages as part of developer onboarding
- [AI-Assisted Configuration Merging](ai-merge-workflow.md) -- Use AI to manage package update conflicts
- [YAML Schemas Reference](../reference/yaml-schemas.md) -- Complete YAML schema reference
- [Package Examples](../packages/examples.md) -- Real-world package examples

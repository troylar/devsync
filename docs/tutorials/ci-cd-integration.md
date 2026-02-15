# Enforcing DevSync Standards in CI/CD

**Time to complete**: 15 minutes
**Difficulty**: Intermediate
**Prerequisites**:

- DevSync installed (`pip install devsync`)
- A GitHub repository with GitHub Actions enabled
- At least one AI coding assistant configured in the project

## The Scenario

Your team uses DevSync to manage AI coding assistant instructions. Every project should have specific instructions installed -- coding standards, security policies, review commands -- but there is no enforcement. Developers forget to install them, or instructions drift out of date. You want your CI/CD pipeline to catch this automatically.

## What You Will Learn

- How to define required instructions for a project
- How to validate installed instructions in a CI pipeline
- How to create a GitHub Actions workflow that blocks PRs with missing instructions
- How to add status badges and notifications for compliance

---

## Step 1: Understand the Goal

DevSync tracks installed instructions in `.devsync/installations.json` at the project root. Your CI pipeline can read this file and compare it against a list of required instructions to determine whether the project is in compliance.

The workflow is:

1. Define which instructions are required in a config file
2. In CI, run `devsync list installed --json` to get current state
3. Compare against the requirements
4. Fail the build if any are missing or outdated

!!! info "Why enforce in CI?"
    Local enforcement relies on developers remembering to run checks. CI enforcement is automatic and cannot be bypassed. It also provides a clear audit trail of compliance over time.

---

## Step 2: Define Required Instructions

Create a file at `.devsync/required.json` in your project root. This file declares which instructions must be installed and optionally which AI tools they must target.

```json
{
  "version": "1.0",
  "required_instructions": [
    {
      "name": "python-standards",
      "namespace": "team",
      "description": "Python coding conventions"
    },
    {
      "name": "security-policy",
      "namespace": "team",
      "description": "Security guidelines for all code"
    },
    {
      "name": "review-code",
      "namespace": "team",
      "description": "Structured code review command"
    }
  ],
  "required_paths": [
    ".claude/rules/",
    ".cursor/rules/"
  ]
}
```

Commit this file to your repository:

```bash
git add .devsync/required.json
git commit -m "chore: add required DevSync instructions config"
```

!!! tip "Start small"
    Begin with a few critical instructions and expand over time. Adding too many requirements at once creates friction for developers who have not adopted DevSync yet.

---

## Step 3: Create the Validation Script

Create a script that compares installed instructions against the requirements. Save this as `scripts/check-devsync.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

REQUIRED_FILE=".devsync/required.json"
INSTALL_FILE=".devsync/installations.json"

if [ ! -f "$REQUIRED_FILE" ]; then
  echo "No required instructions config found at $REQUIRED_FILE"
  echo "Skipping DevSync validation."
  exit 0
fi

if [ ! -f "$INSTALL_FILE" ]; then
  echo "FAIL: No installations.json found."
  echo "DevSync instructions have not been installed in this project."
  echo ""
  echo "Run: devsync install"
  exit 1
fi

echo "Checking DevSync instruction compliance..."
echo ""

MISSING=0

# Read required instruction names
REQUIRED_NAMES=$(python3 -c "
import json, sys
with open('$REQUIRED_FILE') as f:
    data = json.load(f)
for inst in data.get('required_instructions', []):
    print(inst['name'])
")

# Read installed instruction names
INSTALLED_NAMES=$(python3 -c "
import json, sys
with open('$INSTALL_FILE') as f:
    data = json.load(f)
for inst in data.get('installations', []):
    print(inst.get('instruction_name', inst.get('name', '')))
")

for name in $REQUIRED_NAMES; do
  if echo "$INSTALLED_NAMES" | grep -q "^${name}$"; then
    echo "  PASS: $name"
  else
    echo "  FAIL: $name -- not installed"
    MISSING=$((MISSING + 1))
  fi
done

# Check required paths exist
REQUIRED_PATHS=$(python3 -c "
import json
with open('$REQUIRED_FILE') as f:
    data = json.load(f)
for p in data.get('required_paths', []):
    print(p)
")

for path in $REQUIRED_PATHS; do
  if [ -d "$path" ]; then
    FILE_COUNT=$(find "$path" -name "*.md" -o -name "*.mdc" 2>/dev/null | wc -l | tr -d ' ')
    echo "  PASS: $path ($FILE_COUNT files)"
  else
    echo "  FAIL: $path -- directory does not exist"
    MISSING=$((MISSING + 1))
  fi
done

echo ""

if [ "$MISSING" -gt 0 ]; then
  echo "RESULT: $MISSING requirement(s) not met."
  echo ""
  echo "To fix, install the missing instructions:"
  echo "  devsync install"
  exit 1
else
  echo "RESULT: All requirements met."
  exit 0
fi
```

Make it executable:

```bash
chmod +x scripts/check-devsync.sh
```

Test it locally:

```bash
./scripts/check-devsync.sh
```

Expected output when all instructions are installed:

```
Checking DevSync instruction compliance...

  PASS: python-standards
  PASS: security-policy
  PASS: review-code
  PASS: .claude/rules/ (3 files)
  PASS: .cursor/rules/ (3 files)

RESULT: All requirements met.
```

---

## Step 4: Create the GitHub Actions Workflow

Create the workflow file at `.github/workflows/devsync-check.yml`:

```yaml
name: DevSync Compliance

on:
  pull_request:
    branches: [main]
    paths:
      - '.devsync/**'
      - '.claude/**'
      - '.cursor/**'
      - '.windsurf/**'
      - '.github/instructions/**'

jobs:
  check-instructions:
    name: Verify Required Instructions
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install DevSync
        run: pip install devsync

      - name: Validate required instructions
        run: |
          chmod +x scripts/check-devsync.sh
          ./scripts/check-devsync.sh

      - name: List installed instructions
        if: always()
        run: devsync list installed --json || echo "No installations found"
```

!!! warning "Path filters"
    The `paths` filter ensures this workflow only runs when DevSync-related files change. If you want it to run on every PR regardless, remove the `paths` section.

---

## Step 5: Require the Check for PR Merges

To prevent merging PRs that fail the DevSync compliance check:

1. Go to your repository Settings on GitHub
2. Navigate to **Branches** and select your branch protection rule for `main`
3. Under **Require status checks to pass before merging**, add `Verify Required Instructions`
4. Save changes

Now any PR that modifies DevSync-related files must pass the compliance check before it can be merged.

---

## Step 6: Add a Status Badge

Add a badge to your README to show the compliance status at a glance. Add this line to the top of your `README.md`:

```markdown
[![DevSync Compliance](https://github.com/your-org/your-repo/actions/workflows/devsync-check.yml/badge.svg)](https://github.com/your-org/your-repo/actions/workflows/devsync-check.yml)
```

!!! tip "Reference repository"
    See [troylar/devsync-starter-templates](https://github.com/troylar/devsync-starter-templates) for an example repository structure that follows these standards.

---

## Step 7: Extend with Notifications (Optional)

Add a Slack or email notification when the check fails. Append this step to the workflow:

```yaml
      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1.27.0
        with:
          payload: |
            {
              "text": "DevSync compliance check failed on PR #${{ github.event.pull_request.number }} by ${{ github.actor }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## Troubleshooting

### Workflow does not trigger

Verify that the `paths` filter in the workflow matches the files being changed. If no DevSync-related files are in the PR diff, the workflow will not run. Remove the `paths` section to run on every PR.

### "No installations.json found" in CI

The `.devsync/installations.json` file must be committed to the repository. After installing instructions locally, commit the tracking file:

```bash
git add .devsync/installations.json
git commit -m "chore: track DevSync installations"
```

### Script fails with "python3 not found"

Ensure the `actions/setup-python@v5` step runs before the validation script. The Python version must be 3.10 or higher.

### False failures on new repositories

If the repository does not yet have DevSync set up, the script exits with code 0 when `.devsync/required.json` does not exist. Once you add the requirements file, enforcement begins.

---

## Next Steps

- [Using DevSync Across Multiple IDEs](multi-ide-workflow.md) -- Install and sync instructions across all your AI tools
- [Migrating Existing AI Configs to DevSync](migrate-existing-configs.md) -- Bring your existing configuration files under DevSync management
- [Create a Team Configuration Repository](team-config-repo.md) -- Build a shared template repository for your organization

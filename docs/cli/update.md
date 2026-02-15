# devsync update

Update downloaded instructions in your library to their latest versions from source.

## Usage

```
$ devsync update [options]
```

## Options

| Option | Short | Description | Required |
|--------|-------|-------------|----------|
| `--namespace` | `-n` | Repository namespace to update | No* |
| `--all` | `-a` | Update all repositories in the library | No* |

*One of `--namespace` or `--all` is required.

## How It Works

The `update` command pulls the latest changes from source repositories and refreshes both the library and any installed instruction files.

**Branch-based downloads** are updated automatically. If you downloaded from a branch (e.g., `main` or `develop`), `update` pulls the latest commits.

**Tag and commit-based downloads** are immutable and will be skipped. This is by design -- pinned versions should not change unexpectedly.

!!! warning
    Local sources (directories copied with `devsync download --from ./path`) cannot be updated because they have no remote Git history. These are skipped during updates.

## Examples

### Update a specific source

```
$ devsync update --namespace github.com_company_instructions
```

!!! tip
    Not sure what namespace to use? Run `devsync list library` to see all namespaces in your library.

### Update all sources

```
$ devsync update --all
```

### Typical workflow

```
$ devsync list library                  # Find the namespace
$ devsync update --namespace my-source  # Update it
$ devsync list library --instructions   # Verify updated instructions
```

## Update Behavior Summary

| Download Type | Updated? | Reason |
|---------------|----------|--------|
| Branch (e.g., `main`) | Yes | Branches track latest changes |
| No ref specified | Yes | Uses default branch |
| Tag (e.g., `v1.0.0`) | Skipped | Tags are immutable |
| Commit (e.g., `abc123`) | Skipped | Commits are immutable |
| Local directory | Skipped | No Git remote to pull from |

When updates are pulled, any instructions from that source that are already installed in your AI tools are also refreshed with the new content.

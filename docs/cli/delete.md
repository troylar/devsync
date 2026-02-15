# devsync delete

Remove a downloaded source from your local library.

## Usage

```
$ devsync delete <namespace> [options]
```

## Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `namespace` | Repository namespace to delete | Yes |

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--force` | `-f` | Skip the confirmation prompt |

## How It Works

The `delete` command removes a source and its instructions from `~/.devsync/library/`. It does **not** uninstall instructions that have already been installed into your AI tools.

!!! warning
    Deleting a source from the library does not remove instruction files from your AI tools. Use `devsync uninstall` to remove installed instructions.

If any instructions from the source are currently installed, DevSync shows a warning listing them before prompting for confirmation.

## Examples

### Delete a source

```
$ devsync delete github.com_company_instructions
```

You will be prompted to confirm the deletion.

### Delete without confirmation

```
$ devsync delete github.com_company_instructions --force
```

### Find the namespace first

```
$ devsync list library
$ devsync delete github.com_company_instructions
```

## After Deletion

- The source and its instructions are removed from `~/.devsync/library/`
- Previously installed instructions remain in your AI tool directories
- You can re-download the source at any time with `devsync download`
- To remove installed instructions, use `devsync uninstall <name>`

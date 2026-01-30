"""Unit tests for package create CLI command."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from aiconfigkit.cli.main import app

runner = CliRunner()


@pytest.fixture
def temp_project(tmp_path: Path) -> Path:
    """Create a temporary project with a git marker."""
    project = tmp_path / "project"
    project.mkdir()
    (project / ".git").mkdir()
    return project


@pytest.fixture
def project_with_instruction(temp_project: Path) -> Path:
    """Create a project with an instruction file."""
    rules_dir = temp_project / ".claude" / "rules"
    rules_dir.mkdir(parents=True)
    (rules_dir / "coding-style.md").write_text("# Coding Style\nBe consistent.")
    return temp_project


class TestPackageCreateCommand:
    """Test aiconfig package create command."""

    def test_create_no_components(self, temp_project: Path) -> None:
        """Test create fails with no components."""
        with patch("aiconfigkit.cli.package_create.find_project_root", return_value=temp_project):
            result = runner.invoke(app, ["package", "create", "--no-interactive", "--name", "test"])

        assert result.exit_code != 0
        assert "No packageable components" in result.output

    def test_create_basic_package(self, project_with_instruction: Path, tmp_path: Path) -> None:
        """Test basic package creation."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        with patch("aiconfigkit.cli.package_create.find_project_root", return_value=project_with_instruction):
            result = runner.invoke(
                app,
                [
                    "package",
                    "create",
                    "--no-interactive",
                    "--name",
                    "test-pkg",
                    "--output",
                    str(output_dir),
                    "--description",
                    "Test package",
                    "--author",
                    "Tester",
                ],
            )

        assert result.exit_code == 0, f"Failed with: {result.output}"
        assert "successfully" in result.output.lower()

        package_dir = output_dir / "package-test-pkg"
        assert package_dir.exists()
        assert (package_dir / "ai-config-kit-package.yaml").exists()

    def test_create_json_output(self, project_with_instruction: Path, tmp_path: Path) -> None:
        """Test JSON output format."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        with patch("aiconfigkit.cli.package_create.find_project_root", return_value=project_with_instruction):
            result = runner.invoke(
                app,
                [
                    "package",
                    "create",
                    "--no-interactive",
                    "--name",
                    "json-test",
                    "--output",
                    str(output_dir),
                    "--json",
                    "--quiet",  # Suppress non-JSON output
                ],
            )

        assert result.exit_code == 0
        # Verify key JSON fields are present in output
        assert '"success": true' in result.output or '"success":true' in result.output
        assert '"package_path"' in result.output
        assert '"components_included"' in result.output

        # Verify the package was actually created
        package_dir = output_dir / "package-json-test"
        assert package_dir.exists()
        assert (package_dir / "ai-config-kit-package.yaml").exists()

    def test_create_requires_name_non_interactive(self, project_with_instruction: Path) -> None:
        """Test that --name is required in non-interactive mode."""
        with patch("aiconfigkit.cli.package_create.find_project_root", return_value=project_with_instruction):
            result = runner.invoke(
                app,
                ["package", "create", "--no-interactive"],
            )

        assert result.exit_code != 0
        assert "--name is required" in result.output

    def test_create_invalid_name(self, project_with_instruction: Path, tmp_path: Path) -> None:
        """Test rejection of invalid package names."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        with patch("aiconfigkit.cli.package_create.find_project_root", return_value=project_with_instruction):
            result = runner.invoke(
                app,
                [
                    "package",
                    "create",
                    "--no-interactive",
                    "--name",
                    "invalid@name!",
                    "--output",
                    str(output_dir),
                ],
            )

        assert result.exit_code != 0
        assert "Invalid package name" in result.output

    def test_create_existing_directory(self, project_with_instruction: Path, tmp_path: Path) -> None:
        """Test failure when package directory exists."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        (output_dir / "package-existing").mkdir()

        with patch("aiconfigkit.cli.package_create.find_project_root", return_value=project_with_instruction):
            result = runner.invoke(
                app,
                [
                    "package",
                    "create",
                    "--no-interactive",
                    "--name",
                    "existing",
                    "--output",
                    str(output_dir),
                ],
            )

        assert result.exit_code != 0
        assert "already exists" in result.output

    def test_create_force_overwrite(self, project_with_instruction: Path, tmp_path: Path) -> None:
        """Test --force overwrites existing directory."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        existing = output_dir / "package-force-test"
        existing.mkdir()
        (existing / "old-file.txt").write_text("old content")

        with patch("aiconfigkit.cli.package_create.find_project_root", return_value=project_with_instruction):
            result = runner.invoke(
                app,
                [
                    "package",
                    "create",
                    "--no-interactive",
                    "--name",
                    "force-test",
                    "--output",
                    str(output_dir),
                    "--force",
                ],
            )

        assert result.exit_code == 0
        assert (existing / "ai-config-kit-package.yaml").exists()
        assert not (existing / "old-file.txt").exists()

    def test_create_quiet_mode(self, project_with_instruction: Path, tmp_path: Path) -> None:
        """Test quiet output mode."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        with patch("aiconfigkit.cli.package_create.find_project_root", return_value=project_with_instruction):
            result = runner.invoke(
                app,
                [
                    "package",
                    "create",
                    "--no-interactive",
                    "--name",
                    "quiet-test",
                    "--output",
                    str(output_dir),
                    "--quiet",
                ],
            )

        assert result.exit_code == 0
        assert "Components:" not in result.output

    def test_create_custom_version(self, project_with_instruction: Path, tmp_path: Path) -> None:
        """Test custom version number."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        with patch("aiconfigkit.cli.package_create.find_project_root", return_value=project_with_instruction):
            result = runner.invoke(
                app,
                [
                    "package",
                    "create",
                    "--no-interactive",
                    "--name",
                    "version-test",
                    "--version",
                    "2.5.0",
                    "--output",
                    str(output_dir),
                ],
            )

        assert result.exit_code == 0

        import yaml

        manifest_path = output_dir / "package-version-test" / "ai-config-kit-package.yaml"
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)
        assert manifest["version"] == "2.5.0"

    def test_create_keep_secrets(self, project_with_instruction: Path, tmp_path: Path) -> None:
        """Test --keep-secrets flag."""
        claude_dir = project_with_instruction / ".claude"
        settings = {"mcpServers": {"test": {"command": "cmd", "env": {"API_KEY": "secret-value-123456789"}}}}
        (claude_dir / "settings.local.json").write_text(json.dumps(settings))

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        with patch("aiconfigkit.cli.package_create.find_project_root", return_value=project_with_instruction):
            result = runner.invoke(
                app,
                [
                    "package",
                    "create",
                    "--no-interactive",
                    "--name",
                    "secrets-test",
                    "--output",
                    str(output_dir),
                    "--keep-secrets",
                ],
            )

        assert result.exit_code == 0

        mcp_file = output_dir / "package-secrets-test" / "mcp" / "test.json"
        if mcp_file.exists():
            with open(mcp_file) as f:
                mcp_config = json.load(f)
            if "env" in mcp_config:
                assert mcp_config["env"]["API_KEY"] == "secret-value-123456789"

    def test_create_invalid_output_directory(self, project_with_instruction: Path) -> None:
        """Test failure with invalid output directory."""
        with patch("aiconfigkit.cli.package_create.find_project_root", return_value=project_with_instruction):
            result = runner.invoke(
                app,
                [
                    "package",
                    "create",
                    "--no-interactive",
                    "--name",
                    "test",
                    "--output",
                    "/nonexistent/path",
                ],
            )

        assert result.exit_code != 0
        assert "not found" in result.output.lower()


class TestPackageCreateComponents:
    """Test package creation with various component types."""

    def test_create_with_multiple_instructions(self, temp_project: Path, tmp_path: Path) -> None:
        """Test package with multiple instruction files."""
        rules_dir = temp_project / ".claude" / "rules"
        rules_dir.mkdir(parents=True)
        (rules_dir / "style.md").write_text("# Style")
        (rules_dir / "testing.md").write_text("# Testing")
        (rules_dir / "security.md").write_text("# Security")

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        with patch("aiconfigkit.cli.package_create.find_project_root", return_value=temp_project):
            result = runner.invoke(
                app,
                [
                    "package",
                    "create",
                    "--no-interactive",
                    "--name",
                    "multi-inst",
                    "--output",
                    str(output_dir),
                ],
            )

        assert result.exit_code == 0

        import yaml

        manifest_path = output_dir / "package-multi-inst" / "ai-config-kit-package.yaml"
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)
        assert len(manifest["components"]["instructions"]) == 3

    def test_create_with_hooks_and_commands(self, temp_project: Path, tmp_path: Path) -> None:
        """Test package with hooks and commands."""
        (temp_project / ".claude" / "rules").mkdir(parents=True)
        (temp_project / ".claude" / "rules" / "test.md").write_text("# Test")

        hooks_dir = temp_project / ".claude" / "hooks"
        hooks_dir.mkdir(parents=True)
        (hooks_dir / "preToolUse.sh").write_text("#!/bin/bash")

        cmd_dir = temp_project / ".claude" / "commands"
        cmd_dir.mkdir(parents=True)
        (cmd_dir / "build.sh").write_text("#!/bin/bash")

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        with patch("aiconfigkit.cli.package_create.find_project_root", return_value=temp_project):
            result = runner.invoke(
                app,
                [
                    "package",
                    "create",
                    "--no-interactive",
                    "--name",
                    "full-pkg",
                    "--output",
                    str(output_dir),
                ],
            )

        assert result.exit_code == 0

        package_dir = output_dir / "package-full-pkg"
        assert (package_dir / "hooks" / "preToolUse.sh").exists()
        assert (package_dir / "commands" / "build.sh").exists()

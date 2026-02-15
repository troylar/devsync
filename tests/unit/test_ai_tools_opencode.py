"""Tests for OpenCode AI tool integration."""

import pytest

from devsync.ai_tools.opencode import OpenCodeTool
from devsync.core.models import AIToolType, InstallationScope, Instruction


@pytest.fixture
def opencode_tool():
    """Create an OpenCode tool instance."""
    return OpenCodeTool()


@pytest.fixture
def sample_instruction():
    """Create a sample instruction for testing."""
    return Instruction(
        name="test-instruction",
        description="Test instruction",
        content="# Test Instruction\n\nThis is test content.",
        file_path="test.md",
        tags=["test"],
    )


@pytest.fixture
def second_instruction():
    """Create a second instruction for testing multi-section behavior."""
    return Instruction(
        name="second-instruction",
        description="Second instruction",
        content="# Second Instruction\n\nMore content here.",
        file_path="second.md",
        tags=["test"],
    )


class TestOpenCodeTool:
    """Test suite for OpenCodeTool."""

    def test_tool_type(self, opencode_tool: OpenCodeTool) -> None:
        assert opencode_tool.tool_type == AIToolType.OPENCODE

    def test_tool_name(self, opencode_tool: OpenCodeTool) -> None:
        assert opencode_tool.tool_name == "OpenCode"

    def test_is_installed_when_binary_present(
        self, opencode_tool: OpenCodeTool, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr("devsync.ai_tools.opencode.shutil.which", lambda cmd: "/usr/local/bin/opencode")
        assert opencode_tool.is_installed() is True

    def test_is_installed_when_config_exists(
        self, opencode_tool: OpenCodeTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.opencode.shutil.which", lambda cmd: None)
        opencode_dir = temp_dir / ".opencode"
        opencode_dir.mkdir(parents=True)
        monkeypatch.setattr("devsync.ai_tools.opencode.Path.home", lambda: temp_dir)
        assert opencode_tool.is_installed() is True

    def test_is_installed_when_absent(
        self, opencode_tool: OpenCodeTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.opencode.shutil.which", lambda cmd: None)
        monkeypatch.setattr("devsync.ai_tools.opencode.Path.home", lambda: temp_dir)
        assert opencode_tool.is_installed() is False

    def test_get_instructions_directory_raises_not_implemented(self, opencode_tool: OpenCodeTool) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            opencode_tool.get_instructions_directory()
        assert "global installation is not supported" in str(exc_info.value).lower()

    def test_get_instruction_file_extension(self, opencode_tool: OpenCodeTool) -> None:
        assert opencode_tool.get_instruction_file_extension() == ".md"

    def test_get_project_instructions_directory(self, opencode_tool: OpenCodeTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()
        assert opencode_tool.get_project_instructions_directory(project_root) == project_root

    def test_get_instruction_path(self, opencode_tool: OpenCodeTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()
        path = opencode_tool.get_instruction_path("test", scope=InstallationScope.PROJECT, project_root=project_root)
        assert path == project_root / "AGENTS.md"

    def test_get_instruction_path_global_raises(self, opencode_tool: OpenCodeTool) -> None:
        with pytest.raises(NotImplementedError):
            opencode_tool.get_instruction_path("test", scope=InstallationScope.GLOBAL)

    def test_get_instruction_path_no_project_root_raises(self, opencode_tool: OpenCodeTool) -> None:
        with pytest.raises(ValueError):
            opencode_tool.get_instruction_path("test", scope=InstallationScope.PROJECT, project_root=None)

    def test_install_creates_agents_md(
        self, opencode_tool: OpenCodeTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        path = opencode_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path == project_root / "AGENTS.md"
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" in content
        assert "<!-- devsync:end:test-instruction -->" in content
        assert "# Test Instruction" in content

    def test_install_appends_to_existing(
        self,
        opencode_tool: OpenCodeTool,
        temp_dir,  # type: ignore[no-untyped-def]
        sample_instruction: Instruction,
        second_instruction: Instruction,
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        opencode_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )
        opencode_tool.install_instruction(
            second_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        content = (project_root / "AGENTS.md").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" in content
        assert "<!-- devsync:start:second-instruction -->" in content
        assert "# Test Instruction" in content
        assert "# Second Instruction" in content

    def test_install_existing_raises_without_overwrite(
        self, opencode_tool: OpenCodeTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        opencode_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        with pytest.raises(FileExistsError):
            opencode_tool.install_instruction(
                sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
            )

    def test_install_overwrite_replaces_section(
        self, opencode_tool: OpenCodeTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        opencode_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        updated = Instruction(
            name="test-instruction",
            description="Updated",
            content="# Updated Content",
            file_path="test.md",
        )
        opencode_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        content = (project_root / "AGENTS.md").read_text(encoding="utf-8")
        assert "# Updated Content" in content
        assert "# Test Instruction" not in content
        assert content.count("<!-- devsync:start:test-instruction -->") == 1

    def test_instruction_exists_true(
        self, opencode_tool: OpenCodeTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        opencode_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert (
            opencode_tool.instruction_exists(
                "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
            )
            is True
        )

    def test_instruction_exists_false_no_file(self, opencode_tool: OpenCodeTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        assert (
            opencode_tool.instruction_exists("nonexistent", scope=InstallationScope.PROJECT, project_root=project_root)
            is False
        )

    def test_uninstall_removes_section(
        self, opencode_tool: OpenCodeTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        opencode_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        result = opencode_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert result is True
        content = (project_root / "AGENTS.md").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" not in content

    def test_uninstall_nonexistent_returns_false(self, opencode_tool: OpenCodeTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = opencode_tool.uninstall_instruction(
            "nonexistent", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert result is False

    def test_repr(self, opencode_tool: OpenCodeTool) -> None:
        repr_str = repr(opencode_tool)
        assert "OpenCodeTool" in repr_str
        assert AIToolType.OPENCODE.value in repr_str

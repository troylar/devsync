"""Tests for Continue.dev AI tool integration."""

import pytest

from devsync.ai_tools.continuedev import ContinueTool
from devsync.core.models import AIToolType, InstallationScope, Instruction


@pytest.fixture
def continue_tool():
    """Create a Continue.dev tool instance."""
    return ContinueTool()


class TestContinueTool:
    """Test suite for ContinueTool."""

    def test_tool_type(self, continue_tool: ContinueTool) -> None:
        assert continue_tool.tool_type == AIToolType.CONTINUE

    def test_tool_name(self, continue_tool: ContinueTool) -> None:
        assert continue_tool.tool_name == "Continue.dev"

    def test_is_installed_when_config_dir_exists(
        self, continue_tool: ContinueTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        continue_dir = temp_dir / ".continue"
        continue_dir.mkdir()
        monkeypatch.setattr("devsync.ai_tools.continuedev.Path.home", lambda: temp_dir)
        assert continue_tool.is_installed() is True

    def test_is_installed_when_absent(
        self, continue_tool: ContinueTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.continuedev.Path.home", lambda: temp_dir)
        assert continue_tool.is_installed() is False

    def test_get_instructions_directory_raises_not_implemented(self, continue_tool: ContinueTool) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            continue_tool.get_instructions_directory()
        assert "global installation is not supported" in str(exc_info.value).lower()

    def test_get_instruction_file_extension(self, continue_tool: ContinueTool) -> None:
        assert continue_tool.get_instruction_file_extension() == ".md"

    def test_get_project_instructions_directory(self, continue_tool: ContinueTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instructions_dir = continue_tool.get_project_instructions_directory(project_root)

        assert instructions_dir == project_root / ".continue" / "rules"
        assert instructions_dir.exists()

    def test_install_instruction(self, continue_tool: ContinueTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
            tags=[],
        )

        path = continue_tool.install_instruction(
            instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path.exists()
        assert path.read_text() == "Test content"
        assert path.suffix == ".md"
        assert path.parent == project_root / ".continue" / "rules"

    def test_install_instruction_overwrite(self, continue_tool: ContinueTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Original content",
            file_path="test.md",
        )
        continue_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        updated = Instruction(
            name="test-instruction",
            description="Test",
            content="Updated content",
            file_path="test.md",
        )
        path = continue_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path.read_text() == "Updated content"

    def test_install_existing_raises_without_overwrite(self, continue_tool: ContinueTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        continue_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        with pytest.raises(FileExistsError):
            continue_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

    def test_uninstall_instruction(self, continue_tool: ContinueTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        continue_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        result = continue_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert result is True
        path = continue_tool.get_instruction_path(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert not path.exists()

    def test_uninstall_nonexistent_returns_false(self, continue_tool: ContinueTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = continue_tool.uninstall_instruction(
            "nonexistent", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert result is False

    def test_instruction_exists(self, continue_tool: ContinueTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        assert (
            continue_tool.instruction_exists(
                "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
            )
            is False
        )

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        continue_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert (
            continue_tool.instruction_exists(
                "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
            )
            is True
        )

    def test_repr(self, continue_tool: ContinueTool) -> None:
        repr_str = repr(continue_tool)
        assert "ContinueTool" in repr_str
        assert AIToolType.CONTINUE.value in repr_str

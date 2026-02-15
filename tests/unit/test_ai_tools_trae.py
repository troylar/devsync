"""Tests for Trae AI tool integration."""

import pytest

from devsync.ai_tools.trae import TraeTool
from devsync.core.models import AIToolType, InstallationScope, Instruction


@pytest.fixture
def trae_tool():
    """Create a Trae tool instance."""
    return TraeTool()


class TestTraeTool:
    """Test suite for TraeTool."""

    def test_tool_type(self, trae_tool: TraeTool) -> None:
        assert trae_tool.tool_type == AIToolType.TRAE

    def test_tool_name(self, trae_tool: TraeTool) -> None:
        assert trae_tool.tool_name == "Trae"

    def test_is_installed_when_binary_present(self, trae_tool: TraeTool, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("devsync.ai_tools.trae.shutil.which", lambda cmd: "/usr/local/bin/trae")
        assert trae_tool.is_installed() is True

    def test_is_installed_when_absent(self, trae_tool: TraeTool, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("devsync.ai_tools.trae.shutil.which", lambda cmd: None)
        assert trae_tool.is_installed() is False

    def test_get_instructions_directory_raises_not_implemented(self, trae_tool: TraeTool) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            trae_tool.get_instructions_directory()
        assert "global installation is not supported" in str(exc_info.value).lower()

    def test_get_instruction_file_extension(self, trae_tool: TraeTool) -> None:
        assert trae_tool.get_instruction_file_extension() == ".md"

    def test_get_project_instructions_directory(self, trae_tool: TraeTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instructions_dir = trae_tool.get_project_instructions_directory(project_root)

        assert instructions_dir == project_root / ".trae" / "rules"
        assert instructions_dir.exists()

    def test_install_instruction(self, trae_tool: TraeTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
            tags=[],
        )

        path = trae_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert path.exists()
        assert path.read_text() == "Test content"
        assert path.suffix == ".md"
        assert path.parent == project_root / ".trae" / "rules"

    def test_install_instruction_overwrite(self, trae_tool: TraeTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Original content",
            file_path="test.md",
        )
        trae_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        updated = Instruction(
            name="test-instruction",
            description="Test",
            content="Updated content",
            file_path="test.md",
        )
        path = trae_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path.read_text() == "Updated content"

    def test_install_existing_raises_without_overwrite(self, trae_tool: TraeTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        trae_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        with pytest.raises(FileExistsError):
            trae_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

    def test_uninstall_instruction(self, trae_tool: TraeTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        trae_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        result = trae_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert result is True
        path = trae_tool.get_instruction_path(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert not path.exists()

    def test_uninstall_nonexistent_returns_false(self, trae_tool: TraeTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = trae_tool.uninstall_instruction(
            "nonexistent", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert result is False

    def test_instruction_exists(self, trae_tool: TraeTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        assert (
            trae_tool.instruction_exists("test-instruction", scope=InstallationScope.PROJECT, project_root=project_root)
            is False
        )

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        trae_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert (
            trae_tool.instruction_exists("test-instruction", scope=InstallationScope.PROJECT, project_root=project_root)
            is True
        )

    def test_repr(self, trae_tool: TraeTool) -> None:
        repr_str = repr(trae_tool)
        assert "TraeTool" in repr_str
        assert AIToolType.TRAE.value in repr_str

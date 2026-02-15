"""Tests for Tabnine AI tool integration."""

import pytest

from devsync.ai_tools.tabnine import TabnineTool
from devsync.core.models import AIToolType, InstallationScope, Instruction


@pytest.fixture
def tabnine_tool():
    """Create a Tabnine tool instance."""
    return TabnineTool()


class TestTabnineTool:
    """Test suite for TabnineTool."""

    def test_tool_type(self, tabnine_tool: TabnineTool) -> None:
        assert tabnine_tool.tool_type == AIToolType.TABNINE

    def test_tool_name(self, tabnine_tool: TabnineTool) -> None:
        assert tabnine_tool.tool_name == "Tabnine"

    def test_is_installed_when_config_dir_exists(
        self, tabnine_tool: TabnineTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        tabnine_dir = temp_dir / ".tabnine"
        tabnine_dir.mkdir()
        monkeypatch.setattr("devsync.ai_tools.tabnine.Path.home", lambda: temp_dir)
        assert tabnine_tool.is_installed() is True

    def test_is_installed_when_absent(
        self, tabnine_tool: TabnineTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.tabnine.Path.home", lambda: temp_dir)
        assert tabnine_tool.is_installed() is False

    def test_get_instructions_directory_raises_not_implemented(self, tabnine_tool: TabnineTool) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            tabnine_tool.get_instructions_directory()
        assert "global installation is not supported" in str(exc_info.value).lower()

    def test_get_instruction_file_extension(self, tabnine_tool: TabnineTool) -> None:
        assert tabnine_tool.get_instruction_file_extension() == ".md"

    def test_get_project_instructions_directory(self, tabnine_tool: TabnineTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instructions_dir = tabnine_tool.get_project_instructions_directory(project_root)

        assert instructions_dir == project_root / ".tabnine" / "guidelines"
        assert instructions_dir.exists()

    def test_install_instruction(self, tabnine_tool: TabnineTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
            tags=[],
        )

        path = tabnine_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert path.exists()
        assert path.read_text() == "Test content"
        assert path.suffix == ".md"
        assert path.parent == project_root / ".tabnine" / "guidelines"

    def test_install_instruction_overwrite(self, tabnine_tool: TabnineTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Original content",
            file_path="test.md",
        )
        tabnine_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        updated = Instruction(
            name="test-instruction",
            description="Test",
            content="Updated content",
            file_path="test.md",
        )
        path = tabnine_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path.read_text() == "Updated content"

    def test_install_existing_raises_without_overwrite(self, tabnine_tool: TabnineTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        tabnine_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        with pytest.raises(FileExistsError):
            tabnine_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

    def test_uninstall_instruction(self, tabnine_tool: TabnineTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        tabnine_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        result = tabnine_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert result is True
        path = tabnine_tool.get_instruction_path(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert not path.exists()

    def test_uninstall_nonexistent_returns_false(self, tabnine_tool: TabnineTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = tabnine_tool.uninstall_instruction(
            "nonexistent", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert result is False

    def test_instruction_exists(self, tabnine_tool: TabnineTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        assert (
            tabnine_tool.instruction_exists(
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
        tabnine_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert (
            tabnine_tool.instruction_exists(
                "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
            )
            is True
        )

    def test_repr(self, tabnine_tool: TabnineTool) -> None:
        repr_str = repr(tabnine_tool)
        assert "TabnineTool" in repr_str
        assert AIToolType.TABNINE.value in repr_str

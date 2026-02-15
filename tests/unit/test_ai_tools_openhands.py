"""Tests for OpenHands AI tool integration."""

import pytest

from devsync.ai_tools.openhands import OpenHandsTool
from devsync.core.models import AIToolType, InstallationScope, Instruction


@pytest.fixture
def openhands_tool():
    """Create an OpenHands tool instance."""
    return OpenHandsTool()


class TestOpenHandsTool:
    """Test suite for OpenHandsTool."""

    def test_tool_type(self, openhands_tool: OpenHandsTool) -> None:
        assert openhands_tool.tool_type == AIToolType.OPENHANDS

    def test_tool_name(self, openhands_tool: OpenHandsTool) -> None:
        assert openhands_tool.tool_name == "OpenHands"

    def test_is_installed_when_config_dir_exists(
        self, openhands_tool: OpenHandsTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        openhands_dir = temp_dir / ".openhands"
        openhands_dir.mkdir()
        monkeypatch.setattr("devsync.ai_tools.openhands.Path.home", lambda: temp_dir)
        assert openhands_tool.is_installed() is True

    def test_is_installed_when_absent(
        self, openhands_tool: OpenHandsTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.openhands.Path.home", lambda: temp_dir)
        assert openhands_tool.is_installed() is False

    def test_get_instructions_directory_raises_not_implemented(self, openhands_tool: OpenHandsTool) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            openhands_tool.get_instructions_directory()
        assert "global installation is not supported" in str(exc_info.value).lower()

    def test_get_instruction_file_extension(self, openhands_tool: OpenHandsTool) -> None:
        assert openhands_tool.get_instruction_file_extension() == ".md"

    def test_get_project_instructions_directory(self, openhands_tool: OpenHandsTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instructions_dir = openhands_tool.get_project_instructions_directory(project_root)

        assert instructions_dir == project_root / ".openhands" / "microagents"
        assert instructions_dir.exists()

    def test_install_instruction(self, openhands_tool: OpenHandsTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
            tags=[],
        )

        path = openhands_tool.install_instruction(
            instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path.exists()
        assert path.read_text() == "Test content"
        assert path.suffix == ".md"
        assert path.parent == project_root / ".openhands" / "microagents"

    def test_install_instruction_overwrite(self, openhands_tool: OpenHandsTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Original content",
            file_path="test.md",
        )
        openhands_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        updated = Instruction(
            name="test-instruction",
            description="Test",
            content="Updated content",
            file_path="test.md",
        )
        path = openhands_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path.read_text() == "Updated content"

    def test_install_existing_raises_without_overwrite(self, openhands_tool: OpenHandsTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        openhands_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        with pytest.raises(FileExistsError):
            openhands_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

    def test_uninstall_instruction(self, openhands_tool: OpenHandsTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        openhands_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        result = openhands_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert result is True
        path = openhands_tool.get_instruction_path(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert not path.exists()

    def test_uninstall_nonexistent_returns_false(self, openhands_tool: OpenHandsTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = openhands_tool.uninstall_instruction(
            "nonexistent", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert result is False

    def test_instruction_exists(self, openhands_tool: OpenHandsTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        assert (
            openhands_tool.instruction_exists(
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
        openhands_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert (
            openhands_tool.instruction_exists(
                "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
            )
            is True
        )

    def test_repr(self, openhands_tool: OpenHandsTool) -> None:
        repr_str = repr(openhands_tool)
        assert "OpenHandsTool" in repr_str
        assert AIToolType.OPENHANDS.value in repr_str

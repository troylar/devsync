"""Tests for JetBrains AI tool integration."""

import pytest

from devsync.ai_tools.jetbrains import JetBrainsTool
from devsync.core.models import AIToolType, InstallationScope, Instruction


@pytest.fixture
def jetbrains_tool():
    """Create a JetBrains AI tool instance."""
    return JetBrainsTool()


class TestJetBrainsTool:
    """Test suite for JetBrainsTool."""

    def test_tool_type(self, jetbrains_tool: JetBrainsTool) -> None:
        assert jetbrains_tool.tool_type == AIToolType.JETBRAINS

    def test_tool_name(self, jetbrains_tool: JetBrainsTool) -> None:
        assert jetbrains_tool.tool_name == "JetBrains AI"

    def test_is_installed_when_config_dir_exists(
        self, jetbrains_tool: JetBrainsTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        jetbrains_dir = temp_dir / "Library" / "Application Support" / "JetBrains"
        jetbrains_dir.mkdir(parents=True)
        monkeypatch.setattr("devsync.ai_tools.jetbrains.Path.home", lambda: temp_dir)
        assert jetbrains_tool.is_installed() is True

    def test_is_installed_when_absent(
        self, jetbrains_tool: JetBrainsTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.jetbrains.Path.home", lambda: temp_dir)
        assert jetbrains_tool.is_installed() is False

    def test_get_instructions_directory_raises_not_implemented(self, jetbrains_tool: JetBrainsTool) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            jetbrains_tool.get_instructions_directory()
        assert "global installation is not supported" in str(exc_info.value).lower()

    def test_get_instruction_file_extension(self, jetbrains_tool: JetBrainsTool) -> None:
        assert jetbrains_tool.get_instruction_file_extension() == ".md"

    def test_get_project_instructions_directory(self, jetbrains_tool: JetBrainsTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instructions_dir = jetbrains_tool.get_project_instructions_directory(project_root)

        assert instructions_dir == project_root / ".aiassistant" / "rules"
        assert instructions_dir.exists()

    def test_install_instruction(self, jetbrains_tool: JetBrainsTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
            tags=[],
        )

        path = jetbrains_tool.install_instruction(
            instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path.exists()
        assert path.read_text() == "Test content"
        assert path.suffix == ".md"
        assert path.parent == project_root / ".aiassistant" / "rules"

    def test_install_instruction_overwrite(self, jetbrains_tool: JetBrainsTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Original content",
            file_path="test.md",
        )
        jetbrains_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        updated = Instruction(
            name="test-instruction",
            description="Test",
            content="Updated content",
            file_path="test.md",
        )
        path = jetbrains_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path.read_text() == "Updated content"

    def test_install_existing_raises_without_overwrite(self, jetbrains_tool: JetBrainsTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        jetbrains_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        with pytest.raises(FileExistsError):
            jetbrains_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

    def test_uninstall_instruction(self, jetbrains_tool: JetBrainsTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        jetbrains_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        result = jetbrains_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert result is True
        path = jetbrains_tool.get_instruction_path(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert not path.exists()

    def test_uninstall_nonexistent_returns_false(self, jetbrains_tool: JetBrainsTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = jetbrains_tool.uninstall_instruction(
            "nonexistent", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert result is False

    def test_instruction_exists(self, jetbrains_tool: JetBrainsTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        assert (
            jetbrains_tool.instruction_exists(
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
        jetbrains_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert (
            jetbrains_tool.instruction_exists(
                "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
            )
            is True
        )

    def test_repr(self, jetbrains_tool: JetBrainsTool) -> None:
        repr_str = repr(jetbrains_tool)
        assert "JetBrainsTool" in repr_str
        assert AIToolType.JETBRAINS.value in repr_str

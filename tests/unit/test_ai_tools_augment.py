"""Tests for Augment AI tool integration."""

import pytest

from devsync.ai_tools.augment import AugmentTool
from devsync.core.models import AIToolType, InstallationScope, Instruction


@pytest.fixture
def augment_tool():
    """Create an Augment tool instance."""
    return AugmentTool()


class TestAugmentTool:
    """Test suite for AugmentTool."""

    def test_tool_type(self, augment_tool: AugmentTool) -> None:
        assert augment_tool.tool_type == AIToolType.AUGMENT

    def test_tool_name(self, augment_tool: AugmentTool) -> None:
        assert augment_tool.tool_name == "Augment"

    def test_is_installed_when_binary_present(self, augment_tool: AugmentTool, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("devsync.ai_tools.augment.shutil.which", lambda cmd: "/usr/local/bin/augment")
        assert augment_tool.is_installed() is True

    def test_is_installed_when_config_dir_exists(
        self, augment_tool: AugmentTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.augment.shutil.which", lambda cmd: None)
        augment_dir = temp_dir / ".augment"
        augment_dir.mkdir()
        monkeypatch.setattr("devsync.ai_tools.augment.Path.home", lambda: temp_dir)
        assert augment_tool.is_installed() is True

    def test_is_installed_when_absent(
        self, augment_tool: AugmentTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.augment.shutil.which", lambda cmd: None)
        monkeypatch.setattr("devsync.ai_tools.augment.Path.home", lambda: temp_dir)
        assert augment_tool.is_installed() is False

    def test_get_instructions_directory_raises_not_implemented(self, augment_tool: AugmentTool) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            augment_tool.get_instructions_directory()
        assert "global installation is not supported" in str(exc_info.value).lower()

    def test_get_instruction_file_extension(self, augment_tool: AugmentTool) -> None:
        assert augment_tool.get_instruction_file_extension() == ".md"

    def test_get_project_instructions_directory(self, augment_tool: AugmentTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instructions_dir = augment_tool.get_project_instructions_directory(project_root)

        assert instructions_dir == project_root / ".augment" / "rules"
        assert instructions_dir.exists()

    def test_install_instruction(self, augment_tool: AugmentTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
            tags=[],
        )

        path = augment_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert path.exists()
        assert path.read_text() == "Test content"
        assert path.suffix == ".md"
        assert path.parent == project_root / ".augment" / "rules"

    def test_install_instruction_overwrite(self, augment_tool: AugmentTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Original content",
            file_path="test.md",
        )
        augment_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        updated = Instruction(
            name="test-instruction",
            description="Test",
            content="Updated content",
            file_path="test.md",
        )
        path = augment_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path.read_text() == "Updated content"

    def test_install_existing_raises_without_overwrite(self, augment_tool: AugmentTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        augment_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        with pytest.raises(FileExistsError):
            augment_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

    def test_uninstall_instruction(self, augment_tool: AugmentTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        augment_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        result = augment_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert result is True
        path = augment_tool.get_instruction_path(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert not path.exists()

    def test_uninstall_nonexistent_returns_false(self, augment_tool: AugmentTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = augment_tool.uninstall_instruction(
            "nonexistent", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert result is False

    def test_instruction_exists(self, augment_tool: AugmentTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        assert (
            augment_tool.instruction_exists(
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
        augment_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert (
            augment_tool.instruction_exists(
                "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
            )
            is True
        )

    def test_repr(self, augment_tool: AugmentTool) -> None:
        repr_str = repr(augment_tool)
        assert "AugmentTool" in repr_str
        assert AIToolType.AUGMENT.value in repr_str

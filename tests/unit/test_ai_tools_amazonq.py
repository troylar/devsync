"""Tests for Amazon Q AI tool integration."""

import pytest

from devsync.ai_tools.amazonq import AmazonQTool
from devsync.core.models import AIToolType, InstallationScope, Instruction


@pytest.fixture
def amazonq_tool():
    """Create an Amazon Q tool instance."""
    return AmazonQTool()


class TestAmazonQTool:
    """Test suite for AmazonQTool."""

    def test_tool_type(self, amazonq_tool: AmazonQTool) -> None:
        assert amazonq_tool.tool_type == AIToolType.AMAZONQ

    def test_tool_name(self, amazonq_tool: AmazonQTool) -> None:
        assert amazonq_tool.tool_name == "Amazon Q"

    def test_is_installed_when_binary_present(self, amazonq_tool: AmazonQTool, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("devsync.ai_tools.amazonq.shutil.which", lambda cmd: "/usr/local/bin/q")
        assert amazonq_tool.is_installed() is True

    def test_is_installed_when_config_dir_exists(
        self, amazonq_tool: AmazonQTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.amazonq.shutil.which", lambda cmd: None)
        amazonq_dir = temp_dir / ".amazonq"
        amazonq_dir.mkdir()
        monkeypatch.setattr("devsync.ai_tools.amazonq.Path.home", lambda: temp_dir)
        assert amazonq_tool.is_installed() is True

    def test_is_installed_when_absent(
        self, amazonq_tool: AmazonQTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.amazonq.shutil.which", lambda cmd: None)
        monkeypatch.setattr("devsync.ai_tools.amazonq.Path.home", lambda: temp_dir)
        assert amazonq_tool.is_installed() is False

    def test_get_instructions_directory_raises_not_implemented(self, amazonq_tool: AmazonQTool) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            amazonq_tool.get_instructions_directory()
        assert "global installation is not supported" in str(exc_info.value).lower()

    def test_get_instruction_file_extension(self, amazonq_tool: AmazonQTool) -> None:
        assert amazonq_tool.get_instruction_file_extension() == ".md"

    def test_get_project_instructions_directory(self, amazonq_tool: AmazonQTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instructions_dir = amazonq_tool.get_project_instructions_directory(project_root)

        assert instructions_dir == project_root / ".amazonq" / "rules"
        assert instructions_dir.exists()

    def test_install_instruction(self, amazonq_tool: AmazonQTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
            tags=[],
        )

        path = amazonq_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert path.exists()
        assert path.read_text() == "Test content"
        assert path.suffix == ".md"
        assert path.parent == project_root / ".amazonq" / "rules"

    def test_install_instruction_overwrite(self, amazonq_tool: AmazonQTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Original content",
            file_path="test.md",
        )
        amazonq_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        updated = Instruction(
            name="test-instruction",
            description="Test",
            content="Updated content",
            file_path="test.md",
        )
        path = amazonq_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path.read_text() == "Updated content"

    def test_install_existing_raises_without_overwrite(self, amazonq_tool: AmazonQTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        amazonq_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        with pytest.raises(FileExistsError):
            amazonq_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

    def test_uninstall_instruction(self, amazonq_tool: AmazonQTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        instruction = Instruction(
            name="test-instruction",
            description="Test",
            content="Test content",
            file_path="test.md",
        )
        amazonq_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        result = amazonq_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert result is True
        path = amazonq_tool.get_instruction_path(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert not path.exists()

    def test_uninstall_nonexistent_returns_false(self, amazonq_tool: AmazonQTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = amazonq_tool.uninstall_instruction(
            "nonexistent", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert result is False

    def test_instruction_exists(self, amazonq_tool: AmazonQTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        assert (
            amazonq_tool.instruction_exists(
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
        amazonq_tool.install_instruction(instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert (
            amazonq_tool.instruction_exists(
                "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
            )
            is True
        )

    def test_repr(self, amazonq_tool: AmazonQTool) -> None:
        repr_str = repr(amazonq_tool)
        assert "AmazonQTool" in repr_str
        assert AIToolType.AMAZONQ.value in repr_str

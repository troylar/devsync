"""Tests for Aider AI tool integration."""

import pytest

from devsync.ai_tools.aider import AiderTool
from devsync.core.models import AIToolType, InstallationScope, Instruction


@pytest.fixture
def aider_tool():
    """Create an Aider tool instance."""
    return AiderTool()


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


class TestAiderTool:
    """Test suite for AiderTool."""

    def test_tool_type(self, aider_tool: AiderTool) -> None:
        assert aider_tool.tool_type == AIToolType.AIDER

    def test_tool_name(self, aider_tool: AiderTool) -> None:
        assert aider_tool.tool_name == "Aider"

    def test_is_installed_when_binary_present(self, aider_tool: AiderTool, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("devsync.ai_tools.aider.shutil.which", lambda cmd: "/usr/local/bin/aider")
        assert aider_tool.is_installed() is True

    def test_is_installed_when_config_exists(
        self, aider_tool: AiderTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.aider.shutil.which", lambda cmd: None)
        config_file = temp_dir / ".aider.conf.yml"
        config_file.touch()
        monkeypatch.setattr("devsync.ai_tools.aider.Path.home", lambda: temp_dir)
        assert aider_tool.is_installed() is True

    def test_is_installed_when_absent(
        self, aider_tool: AiderTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.aider.shutil.which", lambda cmd: None)
        monkeypatch.setattr("devsync.ai_tools.aider.Path.home", lambda: temp_dir)
        assert aider_tool.is_installed() is False

    def test_get_instructions_directory_raises_not_implemented(self, aider_tool: AiderTool) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            aider_tool.get_instructions_directory()
        assert "global installation is not supported" in str(exc_info.value).lower()

    def test_get_instruction_file_extension(self, aider_tool: AiderTool) -> None:
        assert aider_tool.get_instruction_file_extension() == ".md"

    def test_get_project_instructions_directory(self, aider_tool: AiderTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()
        assert aider_tool.get_project_instructions_directory(project_root) == project_root

    def test_get_instruction_path(self, aider_tool: AiderTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()
        path = aider_tool.get_instruction_path("test", scope=InstallationScope.PROJECT, project_root=project_root)
        assert path == project_root / "CONVENTIONS.md"

    def test_get_instruction_path_global_raises(self, aider_tool: AiderTool) -> None:
        with pytest.raises(NotImplementedError):
            aider_tool.get_instruction_path("test", scope=InstallationScope.GLOBAL)

    def test_get_instruction_path_no_project_root_raises(self, aider_tool: AiderTool) -> None:
        with pytest.raises(ValueError):
            aider_tool.get_instruction_path("test", scope=InstallationScope.PROJECT, project_root=None)

    def test_install_creates_conventions_md(
        self, aider_tool: AiderTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        path = aider_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path == project_root / "CONVENTIONS.md"
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" in content
        assert "<!-- devsync:end:test-instruction -->" in content
        assert "# Test Instruction" in content

    def test_install_appends_to_existing(
        self,
        aider_tool: AiderTool,
        temp_dir,  # type: ignore[no-untyped-def]
        sample_instruction: Instruction,
        second_instruction: Instruction,
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        aider_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)
        aider_tool.install_instruction(second_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        content = (project_root / "CONVENTIONS.md").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" in content
        assert "<!-- devsync:start:second-instruction -->" in content
        assert "# Test Instruction" in content
        assert "# Second Instruction" in content

    def test_install_existing_raises_without_overwrite(
        self, aider_tool: AiderTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        aider_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        with pytest.raises(FileExistsError):
            aider_tool.install_instruction(
                sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
            )

    def test_install_overwrite_replaces_section(
        self, aider_tool: AiderTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        aider_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        updated = Instruction(
            name="test-instruction",
            description="Updated",
            content="# Updated Content",
            file_path="test.md",
        )
        aider_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        content = (project_root / "CONVENTIONS.md").read_text(encoding="utf-8")
        assert "# Updated Content" in content
        assert "# Test Instruction" not in content
        assert content.count("<!-- devsync:start:test-instruction -->") == 1

    def test_instruction_exists_true(
        self, aider_tool: AiderTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        aider_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert (
            aider_tool.instruction_exists(
                "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
            )
            is True
        )

    def test_instruction_exists_false_no_file(self, aider_tool: AiderTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        assert (
            aider_tool.instruction_exists("nonexistent", scope=InstallationScope.PROJECT, project_root=project_root)
            is False
        )

    def test_uninstall_removes_section(
        self, aider_tool: AiderTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        aider_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        result = aider_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert result is True
        content = (project_root / "CONVENTIONS.md").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" not in content

    def test_uninstall_nonexistent_returns_false(self, aider_tool: AiderTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = aider_tool.uninstall_instruction(
            "nonexistent", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert result is False

    def test_repr(self, aider_tool: AiderTool) -> None:
        repr_str = repr(aider_tool)
        assert "AiderTool" in repr_str
        assert AIToolType.AIDER.value in repr_str

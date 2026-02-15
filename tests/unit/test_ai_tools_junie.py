"""Tests for Junie AI tool integration."""

import pytest

from devsync.ai_tools.junie import JunieTool
from devsync.core.models import AIToolType, InstallationScope, Instruction


@pytest.fixture
def junie_tool():
    """Create a Junie tool instance."""
    return JunieTool()


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


class TestJunieTool:
    """Test suite for JunieTool."""

    def test_tool_type(self, junie_tool: JunieTool) -> None:
        assert junie_tool.tool_type == AIToolType.JUNIE

    def test_tool_name(self, junie_tool: JunieTool) -> None:
        assert junie_tool.tool_name == "Junie"

    def test_is_installed_when_config_dir_exists(
        self, junie_tool: JunieTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        jetbrains_dir = temp_dir / "Library" / "Application Support" / "JetBrains"
        jetbrains_dir.mkdir(parents=True)
        monkeypatch.setattr("devsync.ai_tools.junie.Path.home", lambda: temp_dir)
        assert junie_tool.is_installed() is True

    def test_is_installed_when_absent(
        self, junie_tool: JunieTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.junie.Path.home", lambda: temp_dir)
        assert junie_tool.is_installed() is False

    def test_get_instructions_directory_raises_not_implemented(self, junie_tool: JunieTool) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            junie_tool.get_instructions_directory()
        assert "global installation is not supported" in str(exc_info.value).lower()

    def test_get_instruction_file_extension(self, junie_tool: JunieTool) -> None:
        assert junie_tool.get_instruction_file_extension() == ".md"

    def test_get_project_instructions_directory(self, junie_tool: JunieTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()
        assert junie_tool.get_project_instructions_directory(project_root) == project_root / ".junie"

    def test_get_instruction_path(self, junie_tool: JunieTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()
        path = junie_tool.get_instruction_path("test", scope=InstallationScope.PROJECT, project_root=project_root)
        assert path == project_root / ".junie" / "guidelines.md"

    def test_get_instruction_path_global_raises(self, junie_tool: JunieTool) -> None:
        with pytest.raises(NotImplementedError):
            junie_tool.get_instruction_path("test", scope=InstallationScope.GLOBAL)

    def test_get_instruction_path_no_project_root_raises(self, junie_tool: JunieTool) -> None:
        with pytest.raises(ValueError):
            junie_tool.get_instruction_path("test", scope=InstallationScope.PROJECT, project_root=None)

    def test_install_creates_guidelines_md(
        self, junie_tool: JunieTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        path = junie_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path == project_root / ".junie" / "guidelines.md"
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" in content
        assert "<!-- devsync:end:test-instruction -->" in content
        assert "# Test Instruction" in content

    def test_install_appends_to_existing(
        self,
        junie_tool: JunieTool,
        temp_dir,  # type: ignore[no-untyped-def]
        sample_instruction: Instruction,
        second_instruction: Instruction,
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        junie_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)
        junie_tool.install_instruction(second_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        content = (project_root / ".junie" / "guidelines.md").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" in content
        assert "<!-- devsync:start:second-instruction -->" in content

    def test_install_existing_raises_without_overwrite(
        self, junie_tool: JunieTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        junie_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        with pytest.raises(FileExistsError):
            junie_tool.install_instruction(
                sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
            )

    def test_install_overwrite_replaces_section(
        self, junie_tool: JunieTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        junie_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        updated = Instruction(
            name="test-instruction",
            description="Updated",
            content="# Updated Content",
            file_path="test.md",
        )
        junie_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        content = (project_root / ".junie" / "guidelines.md").read_text(encoding="utf-8")
        assert "# Updated Content" in content
        assert "# Test Instruction" not in content

    def test_instruction_exists_true(
        self, junie_tool: JunieTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        junie_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert (
            junie_tool.instruction_exists(
                "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
            )
            is True
        )

    def test_instruction_exists_false_no_file(self, junie_tool: JunieTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        assert (
            junie_tool.instruction_exists("nonexistent", scope=InstallationScope.PROJECT, project_root=project_root)
            is False
        )

    def test_uninstall_removes_section(
        self, junie_tool: JunieTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        junie_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        result = junie_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert result is True
        content = (project_root / ".junie" / "guidelines.md").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" not in content

    def test_uninstall_nonexistent_returns_false(self, junie_tool: JunieTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = junie_tool.uninstall_instruction(
            "nonexistent", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert result is False

    def test_repr(self, junie_tool: JunieTool) -> None:
        repr_str = repr(junie_tool)
        assert "JunieTool" in repr_str
        assert AIToolType.JUNIE.value in repr_str

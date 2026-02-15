"""Tests for Gemini CLI / Code Assist AI tool integration."""

import pytest

from devsync.ai_tools.gemini import GeminiTool
from devsync.core.models import AIToolType, InstallationScope, Instruction


@pytest.fixture
def gemini_tool():
    """Create a Gemini tool instance."""
    return GeminiTool()


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


class TestGeminiTool:
    """Test suite for GeminiTool."""

    def test_tool_type(self, gemini_tool: GeminiTool) -> None:
        assert gemini_tool.tool_type == AIToolType.GEMINI

    def test_tool_name(self, gemini_tool: GeminiTool) -> None:
        assert gemini_tool.tool_name == "Gemini CLI"

    def test_is_installed_when_binary_present(self, gemini_tool: GeminiTool, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("devsync.ai_tools.gemini.shutil.which", lambda cmd: "/usr/local/bin/gemini")
        assert gemini_tool.is_installed() is True

    def test_is_installed_when_config_dir_exists(
        self, gemini_tool: GeminiTool, monkeypatch: pytest.MonkeyPatch, temp_dir
    ) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.gemini.shutil.which", lambda cmd: None)
        gemini_dir = temp_dir / ".gemini"
        gemini_dir.mkdir()
        monkeypatch.setattr("devsync.ai_tools.gemini.Path.home", lambda: temp_dir)
        assert gemini_tool.is_installed() is True

    def test_is_installed_when_absent(self, gemini_tool: GeminiTool, monkeypatch: pytest.MonkeyPatch, temp_dir) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr("devsync.ai_tools.gemini.shutil.which", lambda cmd: None)
        monkeypatch.setattr("devsync.ai_tools.gemini.Path.home", lambda: temp_dir)
        assert gemini_tool.is_installed() is False

    def test_get_instructions_directory_raises_not_implemented(self, gemini_tool: GeminiTool) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            gemini_tool.get_instructions_directory()
        assert "global installation is not supported" in str(exc_info.value).lower()

    def test_get_instruction_file_extension(self, gemini_tool: GeminiTool) -> None:
        assert gemini_tool.get_instruction_file_extension() == ".md"

    def test_get_project_instructions_directory(self, gemini_tool: GeminiTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()
        assert gemini_tool.get_project_instructions_directory(project_root) == project_root

    def test_get_instruction_path(self, gemini_tool: GeminiTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()
        path = gemini_tool.get_instruction_path("test", scope=InstallationScope.PROJECT, project_root=project_root)
        assert path == project_root / "GEMINI.md"

    def test_get_instruction_path_global_raises(self, gemini_tool: GeminiTool) -> None:
        with pytest.raises(NotImplementedError):
            gemini_tool.get_instruction_path("test", scope=InstallationScope.GLOBAL)

    def test_get_instruction_path_no_project_root_raises(self, gemini_tool: GeminiTool) -> None:
        with pytest.raises(ValueError):
            gemini_tool.get_instruction_path("test", scope=InstallationScope.PROJECT, project_root=None)

    def test_install_creates_gemini_md(
        self, gemini_tool: GeminiTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        path = gemini_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path == project_root / "GEMINI.md"
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" in content
        assert "<!-- devsync:end:test-instruction -->" in content
        assert "# Test Instruction" in content

    def test_install_appends_to_existing(
        self,
        gemini_tool: GeminiTool,
        temp_dir,  # type: ignore[no-untyped-def]
        sample_instruction: Instruction,
        second_instruction: Instruction,
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        gemini_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)
        gemini_tool.install_instruction(second_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        content = (project_root / "GEMINI.md").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" in content
        assert "<!-- devsync:start:second-instruction -->" in content
        assert "# Test Instruction" in content
        assert "# Second Instruction" in content

    def test_install_existing_raises_without_overwrite(
        self, gemini_tool: GeminiTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        gemini_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        with pytest.raises(FileExistsError):
            gemini_tool.install_instruction(
                sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
            )

    def test_install_overwrite_replaces_section(
        self, gemini_tool: GeminiTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        gemini_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        updated = Instruction(
            name="test-instruction",
            description="Updated",
            content="# Updated Content",
            file_path="test.md",
        )
        gemini_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        content = (project_root / "GEMINI.md").read_text(encoding="utf-8")
        assert "# Updated Content" in content
        assert "# Test Instruction" not in content
        assert content.count("<!-- devsync:start:test-instruction -->") == 1

    def test_install_overwrite_preserves_other_sections(
        self,
        gemini_tool: GeminiTool,
        temp_dir,  # type: ignore[no-untyped-def]
        sample_instruction: Instruction,
        second_instruction: Instruction,
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        gemini_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)
        gemini_tool.install_instruction(second_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        updated = Instruction(
            name="test-instruction",
            description="Updated",
            content="# Updated",
            file_path="test.md",
        )
        gemini_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        content = (project_root / "GEMINI.md").read_text(encoding="utf-8")
        assert "# Updated" in content
        assert "# Second Instruction" in content

    def test_instruction_exists_true(
        self, gemini_tool: GeminiTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        gemini_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert (
            gemini_tool.instruction_exists(
                "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
            )
            is True
        )

    def test_instruction_exists_false_no_file(self, gemini_tool: GeminiTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        assert (
            gemini_tool.instruction_exists("nonexistent", scope=InstallationScope.PROJECT, project_root=project_root)
            is False
        )

    def test_instruction_exists_false_different_name(
        self, gemini_tool: GeminiTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        gemini_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert (
            gemini_tool.instruction_exists("other-name", scope=InstallationScope.PROJECT, project_root=project_root)
            is False
        )

    def test_uninstall_removes_section(
        self, gemini_tool: GeminiTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        gemini_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        result = gemini_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert result is True
        content = (project_root / "GEMINI.md").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" not in content
        assert "# Test Instruction" not in content

    def test_uninstall_preserves_other_sections(
        self,
        gemini_tool: GeminiTool,
        temp_dir,  # type: ignore[no-untyped-def]
        sample_instruction: Instruction,
        second_instruction: Instruction,
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        gemini_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)
        gemini_tool.install_instruction(second_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        gemini_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        content = (project_root / "GEMINI.md").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" not in content
        assert "<!-- devsync:start:second-instruction -->" in content
        assert "# Second Instruction" in content

    def test_uninstall_nonexistent_returns_false(self, gemini_tool: GeminiTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = gemini_tool.uninstall_instruction(
            "nonexistent", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert result is False

    def test_uninstall_no_file_returns_false(self, gemini_tool: GeminiTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = gemini_tool.uninstall_instruction("test", scope=InstallationScope.PROJECT, project_root=project_root)
        assert result is False

    def test_repr(self, gemini_tool: GeminiTool) -> None:
        repr_str = repr(gemini_tool)
        assert "GeminiTool" in repr_str
        assert AIToolType.GEMINI.value in repr_str

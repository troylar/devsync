"""Tests for OpenAI Codex CLI AI tool integration."""

import pytest

from devsync.ai_tools.codex import CodexTool
from devsync.core.models import AIToolType, InstallationScope, Instruction


@pytest.fixture
def codex_tool():
    """Create a Codex tool instance."""
    return CodexTool()


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


class TestCodexTool:
    """Test suite for CodexTool."""

    def test_tool_type(self, codex_tool: CodexTool) -> None:
        assert codex_tool.tool_type == AIToolType.CODEX

    def test_tool_name(self, codex_tool: CodexTool) -> None:
        assert codex_tool.tool_name == "OpenAI Codex CLI"

    def test_is_installed_when_present(self, codex_tool: CodexTool, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("devsync.ai_tools.codex.shutil.which", lambda cmd: "/usr/local/bin/codex")
        assert codex_tool.is_installed() is True

    def test_is_installed_when_absent(self, codex_tool: CodexTool, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("devsync.ai_tools.codex.shutil.which", lambda cmd: None)
        assert codex_tool.is_installed() is False

    def test_get_instructions_directory_raises_not_implemented(self, codex_tool: CodexTool) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            codex_tool.get_instructions_directory()
        assert "global installation is not supported" in str(exc_info.value).lower()

    def test_get_instruction_file_extension(self, codex_tool: CodexTool) -> None:
        assert codex_tool.get_instruction_file_extension() == ".md"

    def test_get_project_instructions_directory(self, codex_tool: CodexTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()
        assert codex_tool.get_project_instructions_directory(project_root) == project_root

    def test_get_instruction_path(self, codex_tool: CodexTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()
        path = codex_tool.get_instruction_path("test", scope=InstallationScope.PROJECT, project_root=project_root)
        assert path == project_root / "AGENTS.md"

    def test_get_instruction_path_global_raises(self, codex_tool: CodexTool) -> None:
        with pytest.raises(NotImplementedError):
            codex_tool.get_instruction_path("test", scope=InstallationScope.GLOBAL)

    def test_get_instruction_path_no_project_root_raises(self, codex_tool: CodexTool) -> None:
        with pytest.raises(ValueError):
            codex_tool.get_instruction_path("test", scope=InstallationScope.PROJECT, project_root=None)

    def test_install_creates_agents_md(
        self, codex_tool: CodexTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        path = codex_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path == project_root / "AGENTS.md"
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" in content
        assert "<!-- devsync:end:test-instruction -->" in content
        assert "# Test Instruction" in content

    def test_install_appends_to_existing(
        self,
        codex_tool: CodexTool,
        temp_dir,  # type: ignore[no-untyped-def]
        sample_instruction: Instruction,
        second_instruction: Instruction,
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        codex_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)
        codex_tool.install_instruction(second_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        content = (project_root / "AGENTS.md").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" in content
        assert "<!-- devsync:start:second-instruction -->" in content
        assert "# Test Instruction" in content
        assert "# Second Instruction" in content

    def test_install_existing_raises_without_overwrite(
        self, codex_tool: CodexTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        codex_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        with pytest.raises(FileExistsError):
            codex_tool.install_instruction(
                sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
            )

    def test_install_overwrite_replaces_section(
        self, codex_tool: CodexTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        codex_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        updated = Instruction(
            name="test-instruction",
            description="Updated",
            content="# Updated Content",
            file_path="test.md",
        )
        codex_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        content = (project_root / "AGENTS.md").read_text(encoding="utf-8")
        assert "# Updated Content" in content
        assert "# Test Instruction" not in content
        assert content.count("<!-- devsync:start:test-instruction -->") == 1

    def test_install_overwrite_preserves_other_sections(
        self,
        codex_tool: CodexTool,
        temp_dir,  # type: ignore[no-untyped-def]
        sample_instruction: Instruction,
        second_instruction: Instruction,
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        codex_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)
        codex_tool.install_instruction(second_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        updated = Instruction(
            name="test-instruction",
            description="Updated",
            content="# Updated",
            file_path="test.md",
        )
        codex_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        content = (project_root / "AGENTS.md").read_text(encoding="utf-8")
        assert "# Updated" in content
        assert "# Second Instruction" in content

    def test_instruction_exists_true(
        self, codex_tool: CodexTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        codex_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert (
            codex_tool.instruction_exists(
                "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
            )
            is True
        )

    def test_instruction_exists_false_no_file(self, codex_tool: CodexTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        assert (
            codex_tool.instruction_exists("nonexistent", scope=InstallationScope.PROJECT, project_root=project_root)
            is False
        )

    def test_instruction_exists_false_different_name(
        self, codex_tool: CodexTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        codex_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert (
            codex_tool.instruction_exists("other-name", scope=InstallationScope.PROJECT, project_root=project_root)
            is False
        )

    def test_uninstall_removes_section(
        self, codex_tool: CodexTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        codex_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        result = codex_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert result is True
        content = (project_root / "AGENTS.md").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" not in content
        assert "# Test Instruction" not in content

    def test_uninstall_preserves_other_sections(
        self,
        codex_tool: CodexTool,
        temp_dir,  # type: ignore[no-untyped-def]
        sample_instruction: Instruction,
        second_instruction: Instruction,
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        codex_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)
        codex_tool.install_instruction(second_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        codex_tool.uninstall_instruction("test-instruction", scope=InstallationScope.PROJECT, project_root=project_root)

        content = (project_root / "AGENTS.md").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" not in content
        assert "<!-- devsync:start:second-instruction -->" in content
        assert "# Second Instruction" in content

    def test_uninstall_nonexistent_returns_false(self, codex_tool: CodexTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = codex_tool.uninstall_instruction(
            "nonexistent", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert result is False

    def test_uninstall_no_file_returns_false(self, codex_tool: CodexTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = codex_tool.uninstall_instruction("test", scope=InstallationScope.PROJECT, project_root=project_root)
        assert result is False

    def test_repr(self, codex_tool: CodexTool) -> None:
        repr_str = repr(codex_tool)
        assert "CodexTool" in repr_str
        assert AIToolType.CODEX.value in repr_str

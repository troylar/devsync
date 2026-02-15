"""Tests for Zed AI tool integration."""

import pytest

from devsync.ai_tools.zed import ZedTool
from devsync.core.models import AIToolType, InstallationScope, Instruction


@pytest.fixture
def zed_tool():
    """Create a Zed tool instance."""
    return ZedTool()


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


class TestZedTool:
    """Test suite for ZedTool."""

    def test_tool_type(self, zed_tool: ZedTool) -> None:
        assert zed_tool.tool_type == AIToolType.ZED

    def test_tool_name(self, zed_tool: ZedTool) -> None:
        assert zed_tool.tool_name == "Zed"

    def test_is_installed_when_binary_present(self, zed_tool: ZedTool, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("devsync.ai_tools.zed.shutil.which", lambda cmd: "/usr/local/bin/zed")
        assert zed_tool.is_installed() is True

    def test_is_installed_when_absent(self, zed_tool: ZedTool, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("devsync.ai_tools.zed.shutil.which", lambda cmd: None)
        assert zed_tool.is_installed() is False

    def test_get_instructions_directory_raises_not_implemented(self, zed_tool: ZedTool) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            zed_tool.get_instructions_directory()
        assert "global installation is not supported" in str(exc_info.value).lower()

    def test_get_instruction_file_extension(self, zed_tool: ZedTool) -> None:
        assert zed_tool.get_instruction_file_extension() == ".md"

    def test_get_project_instructions_directory(self, zed_tool: ZedTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()
        assert zed_tool.get_project_instructions_directory(project_root) == project_root

    def test_get_instruction_path(self, zed_tool: ZedTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()
        path = zed_tool.get_instruction_path("test", scope=InstallationScope.PROJECT, project_root=project_root)
        assert path == project_root / ".rules"

    def test_get_instruction_path_global_raises(self, zed_tool: ZedTool) -> None:
        with pytest.raises(NotImplementedError):
            zed_tool.get_instruction_path("test", scope=InstallationScope.GLOBAL)

    def test_get_instruction_path_no_project_root_raises(self, zed_tool: ZedTool) -> None:
        with pytest.raises(ValueError):
            zed_tool.get_instruction_path("test", scope=InstallationScope.PROJECT, project_root=None)

    def test_install_creates_rules_file(
        self, zed_tool: ZedTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        path = zed_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path == project_root / ".rules"
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" in content
        assert "<!-- devsync:end:test-instruction -->" in content
        assert "# Test Instruction" in content

    def test_install_appends_to_existing(
        self,
        zed_tool: ZedTool,
        temp_dir,  # type: ignore[no-untyped-def]
        sample_instruction: Instruction,
        second_instruction: Instruction,
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        zed_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)
        zed_tool.install_instruction(second_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        content = (project_root / ".rules").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" in content
        assert "<!-- devsync:start:second-instruction -->" in content
        assert "# Test Instruction" in content
        assert "# Second Instruction" in content

    def test_install_existing_raises_without_overwrite(
        self, zed_tool: ZedTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        zed_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        with pytest.raises(FileExistsError):
            zed_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

    def test_install_overwrite_replaces_section(
        self, zed_tool: ZedTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        zed_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        updated = Instruction(
            name="test-instruction",
            description="Updated",
            content="# Updated Content",
            file_path="test.md",
        )
        zed_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        content = (project_root / ".rules").read_text(encoding="utf-8")
        assert "# Updated Content" in content
        assert "# Test Instruction" not in content
        assert content.count("<!-- devsync:start:test-instruction -->") == 1

    def test_instruction_exists_true(
        self, zed_tool: ZedTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        zed_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        assert (
            zed_tool.instruction_exists("test-instruction", scope=InstallationScope.PROJECT, project_root=project_root)
            is True
        )

    def test_instruction_exists_false_no_file(self, zed_tool: ZedTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        assert (
            zed_tool.instruction_exists("nonexistent", scope=InstallationScope.PROJECT, project_root=project_root)
            is False
        )

    def test_uninstall_removes_section(
        self, zed_tool: ZedTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        zed_tool.install_instruction(sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root)

        result = zed_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert result is True
        content = (project_root / ".rules").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" not in content

    def test_uninstall_nonexistent_returns_false(self, zed_tool: ZedTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = zed_tool.uninstall_instruction(
            "nonexistent", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert result is False

    def test_repr(self, zed_tool: ZedTool) -> None:
        repr_str = repr(zed_tool)
        assert "ZedTool" in repr_str
        assert AIToolType.ZED.value in repr_str

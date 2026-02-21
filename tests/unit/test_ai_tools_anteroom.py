"""Tests for Anteroom AI tool integration."""

import pytest

from devsync.ai_tools.anteroom import AnteroomTool
from devsync.core.models import AIToolType, InstallationScope, Instruction


@pytest.fixture
def anteroom_tool():
    """Create an Anteroom tool instance."""
    return AnteroomTool()


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


class TestAnteroomTool:
    """Test suite for AnteroomTool."""

    def test_tool_type(self, anteroom_tool: AnteroomTool) -> None:
        assert anteroom_tool.tool_type == AIToolType.ANTEROOM

    def test_tool_name(self, anteroom_tool: AnteroomTool) -> None:
        assert anteroom_tool.tool_name == "Anteroom"

    def test_is_installed_when_binary_present(
        self, anteroom_tool: AnteroomTool, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr("devsync.ai_tools.anteroom.shutil.which", lambda cmd: "/usr/local/bin/aroom")
        assert anteroom_tool.is_installed() is True

    def test_is_installed_when_config_dir_exists(
        self,
        anteroom_tool: AnteroomTool,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path,  # type: ignore[no-untyped-def]
    ) -> None:
        monkeypatch.setattr("devsync.ai_tools.anteroom.shutil.which", lambda cmd: None)
        anteroom_dir = tmp_path / ".anteroom"
        anteroom_dir.mkdir()
        monkeypatch.setattr("devsync.ai_tools.anteroom.Path.home", lambda: tmp_path)
        assert anteroom_tool.is_installed() is True

    def test_is_installed_when_absent(
        self,
        anteroom_tool: AnteroomTool,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path,  # type: ignore[no-untyped-def]
    ) -> None:
        monkeypatch.setattr("devsync.ai_tools.anteroom.shutil.which", lambda cmd: None)
        monkeypatch.setattr("devsync.ai_tools.anteroom.Path.home", lambda: tmp_path)
        assert anteroom_tool.is_installed() is False

    def test_get_instructions_directory_raises_not_implemented(self, anteroom_tool: AnteroomTool) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            anteroom_tool.get_instructions_directory()
        assert "global installation is not supported" in str(exc_info.value).lower()

    def test_get_instruction_file_extension(self, anteroom_tool: AnteroomTool) -> None:
        assert anteroom_tool.get_instruction_file_extension() == ".md"

    def test_get_project_instructions_directory(
        self, anteroom_tool: AnteroomTool, temp_dir  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()
        assert anteroom_tool.get_project_instructions_directory(project_root) == project_root

    def test_get_instruction_path(self, anteroom_tool: AnteroomTool, temp_dir) -> None:  # type: ignore[no-untyped-def]
        project_root = temp_dir / "project"
        project_root.mkdir()
        path = anteroom_tool.get_instruction_path("test", scope=InstallationScope.PROJECT, project_root=project_root)
        assert path == project_root / "ANTEROOM.md"

    def test_get_instruction_path_global_raises(self, anteroom_tool: AnteroomTool) -> None:
        with pytest.raises(NotImplementedError):
            anteroom_tool.get_instruction_path("test", scope=InstallationScope.GLOBAL)

    def test_get_instruction_path_no_project_root_raises(self, anteroom_tool: AnteroomTool) -> None:
        with pytest.raises(ValueError):
            anteroom_tool.get_instruction_path("test", scope=InstallationScope.PROJECT, project_root=None)

    def test_install_creates_anteroom_md(
        self, anteroom_tool: AnteroomTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        path = anteroom_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert path == project_root / "ANTEROOM.md"
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" in content
        assert "<!-- devsync:end:test-instruction -->" in content
        assert "# Test Instruction" in content

    def test_install_appends_to_existing(
        self,
        anteroom_tool: AnteroomTool,
        temp_dir,  # type: ignore[no-untyped-def]
        sample_instruction: Instruction,
        second_instruction: Instruction,
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        anteroom_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )
        anteroom_tool.install_instruction(
            second_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        content = (project_root / "ANTEROOM.md").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" in content
        assert "<!-- devsync:start:second-instruction -->" in content
        assert "# Test Instruction" in content
        assert "# Second Instruction" in content

    def test_install_existing_raises_without_overwrite(
        self, anteroom_tool: AnteroomTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        anteroom_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        with pytest.raises(FileExistsError):
            anteroom_tool.install_instruction(
                sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
            )

    def test_install_overwrite_replaces_section(
        self, anteroom_tool: AnteroomTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        anteroom_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        updated = Instruction(
            name="test-instruction",
            description="Updated",
            content="# Updated Content",
            file_path="test.md",
        )
        anteroom_tool.install_instruction(
            updated, overwrite=True, scope=InstallationScope.PROJECT, project_root=project_root
        )

        content = (project_root / "ANTEROOM.md").read_text(encoding="utf-8")
        assert "# Updated Content" in content
        assert "# Test Instruction" not in content
        assert content.count("<!-- devsync:start:test-instruction -->") == 1

    def test_instruction_exists_true(
        self, anteroom_tool: AnteroomTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        anteroom_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert (
            anteroom_tool.instruction_exists(
                "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
            )
            is True
        )

    def test_instruction_exists_false_no_file(
        self, anteroom_tool: AnteroomTool, temp_dir  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        assert (
            anteroom_tool.instruction_exists("nonexistent", scope=InstallationScope.PROJECT, project_root=project_root)
            is False
        )

    def test_uninstall_removes_section(
        self, anteroom_tool: AnteroomTool, temp_dir, sample_instruction: Instruction  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        anteroom_tool.install_instruction(
            sample_instruction, scope=InstallationScope.PROJECT, project_root=project_root
        )

        result = anteroom_tool.uninstall_instruction(
            "test-instruction", scope=InstallationScope.PROJECT, project_root=project_root
        )

        assert result is True
        content = (project_root / "ANTEROOM.md").read_text(encoding="utf-8")
        assert "<!-- devsync:start:test-instruction -->" not in content

    def test_uninstall_nonexistent_returns_false(
        self, anteroom_tool: AnteroomTool, temp_dir  # type: ignore[no-untyped-def]
    ) -> None:
        project_root = temp_dir / "project"
        project_root.mkdir()

        result = anteroom_tool.uninstall_instruction(
            "nonexistent", scope=InstallationScope.PROJECT, project_root=project_root
        )
        assert result is False

    def test_repr(self, anteroom_tool: AnteroomTool) -> None:
        repr_str = repr(anteroom_tool)
        assert "AnteroomTool" in repr_str
        assert AIToolType.ANTEROOM.value in repr_str

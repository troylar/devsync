"""OpenAI Codex CLI AI tool integration."""

import re
import shutil
from pathlib import Path
from typing import Optional

from devsync.ai_tools.base import AITool
from devsync.core.models import AIToolType, InstallationScope, Instruction

START_MARKER = "<!-- devsync:start:{name} -->"
END_MARKER = "<!-- devsync:end:{name} -->"
SECTION_PATTERN = r"<!-- devsync:start:{name} -->\n.*?\n<!-- devsync:end:{name} -->"


class CodexTool(AITool):
    """Integration for OpenAI Codex CLI.

    Codex CLI reads a single AGENTS.md file at the project root.
    DevSync manages individual instruction sections using HTML comment markers:

        <!-- devsync:start:instruction-name -->
        ... instruction content ...
        <!-- devsync:end:instruction-name -->
    """

    @property
    def tool_type(self) -> AIToolType:
        """Return the AI tool type identifier."""
        return AIToolType.CODEX

    @property
    def tool_name(self) -> str:
        """Return human-readable tool name."""
        return "OpenAI Codex CLI"

    def is_installed(self) -> bool:
        """Check if OpenAI Codex CLI is installed on the system.

        Returns:
            True if codex binary is found on PATH
        """
        return shutil.which("codex") is not None

    def get_instructions_directory(self) -> Path:
        """Get the directory where instructions should be installed.

        Raises:
            NotImplementedError: Codex CLI only supports project-level installation
        """
        raise NotImplementedError(
            f"{self.tool_name} global installation is not supported. "
            "OpenAI Codex CLI uses project-level AGENTS.md only. "
            "Please use project-level installation instead (--scope project)."
        )

    def get_instruction_file_extension(self) -> str:
        """Get the file extension for Codex instructions.

        Returns:
            File extension including the dot
        """
        return ".md"

    def get_project_instructions_directory(self, project_root: Path) -> Path:
        """Get the directory for project-specific Codex instructions.

        AGENTS.md lives at the project root, so the directory is the root itself.

        Args:
            project_root: Path to the project root directory

        Returns:
            Path to project root (AGENTS.md lives at root)
        """
        return project_root

    def get_instruction_path(
        self,
        instruction_name: str,
        scope: InstallationScope = InstallationScope.GLOBAL,
        project_root: Optional[Path] = None,
    ) -> Path:
        """Get the path to AGENTS.md.

        Always returns project_root / AGENTS.md regardless of instruction name.

        Args:
            instruction_name: Name of the instruction (unused for path)
            scope: Installation scope (must be PROJECT)
            project_root: Project root path

        Returns:
            Path to AGENTS.md

        Raises:
            ValueError: If scope is PROJECT but project_root is None
            NotImplementedError: If scope is GLOBAL
        """
        if scope == InstallationScope.GLOBAL:
            raise NotImplementedError(
                f"{self.tool_name} global installation is not supported. "
                "Please use project-level installation instead (--scope project)."
            )
        if project_root is None:
            raise ValueError("project_root is required for PROJECT scope")
        return project_root / "AGENTS.md"

    def instruction_exists(
        self,
        instruction_name: str,
        scope: InstallationScope = InstallationScope.GLOBAL,
        project_root: Optional[Path] = None,
    ) -> bool:
        """Check if an instruction section exists in AGENTS.md.

        Args:
            instruction_name: Name of the instruction
            scope: Installation scope
            project_root: Project root path

        Returns:
            True if the instruction's section markers exist in AGENTS.md
        """
        try:
            path = self.get_instruction_path(instruction_name, scope, project_root)
            if not path.exists():
                return False
            content = path.read_text(encoding="utf-8")
            start = START_MARKER.format(name=instruction_name)
            return start in content
        except (FileNotFoundError, ValueError, NotImplementedError):
            return False

    def install_instruction(
        self,
        instruction: Instruction,
        overwrite: bool = False,
        scope: InstallationScope = InstallationScope.GLOBAL,
        project_root: Optional[Path] = None,
    ) -> Path:
        """Install an instruction as a section in AGENTS.md.

        Appends a new section with markers, or replaces an existing section
        if overwrite is True.

        Args:
            instruction: Instruction to install
            overwrite: Whether to overwrite existing section
            scope: Installation scope
            project_root: Project root path

        Returns:
            Path to AGENTS.md

        Raises:
            FileExistsError: If instruction section exists and overwrite=False
        """
        path = self.get_instruction_path(instruction.name, scope, project_root)

        start = START_MARKER.format(name=instruction.name)
        end = END_MARKER.format(name=instruction.name)
        section = f"{start}\n{instruction.content}\n{end}"

        if path.exists():
            content = path.read_text(encoding="utf-8")
            if start in content:
                if not overwrite:
                    raise FileExistsError(f"Instruction already exists in AGENTS.md: {instruction.name}")
                pattern = SECTION_PATTERN.format(name=re.escape(instruction.name))
                content = re.sub(pattern, section, content, flags=re.DOTALL)
                path.write_text(content, encoding="utf-8")
                return path
            if content and not content.endswith("\n"):
                content += "\n"
            content += "\n" + section + "\n"
            path.write_text(content, encoding="utf-8")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(section + "\n", encoding="utf-8")

        return path

    def uninstall_instruction(
        self,
        instruction_name: str,
        scope: InstallationScope = InstallationScope.GLOBAL,
        project_root: Optional[Path] = None,
    ) -> bool:
        """Remove an instruction section from AGENTS.md.

        Args:
            instruction_name: Name of instruction to remove
            scope: Installation scope
            project_root: Project root path

        Returns:
            True if section was removed, False if it didn't exist
        """
        try:
            path = self.get_instruction_path(instruction_name, scope, project_root)
            if not path.exists():
                return False

            content = path.read_text(encoding="utf-8")
            start = START_MARKER.format(name=instruction_name)
            if start not in content:
                return False

            pattern = SECTION_PATTERN.format(name=re.escape(instruction_name))
            new_content = re.sub(pattern, "", content, flags=re.DOTALL)
            # Clean up extra blank lines
            new_content = re.sub(r"\n{3,}", "\n\n", new_content).strip()
            if new_content:
                new_content += "\n"
            path.write_text(new_content, encoding="utf-8")
            return True
        except (FileNotFoundError, ValueError, NotImplementedError):
            return False

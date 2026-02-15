"""JetBrains Junie AI tool integration."""

import re
from pathlib import Path
from typing import Optional

from devsync.ai_tools.base import AITool
from devsync.core.models import AIToolType, InstallationScope, Instruction

START_MARKER = "<!-- devsync:start:{name} -->"
END_MARKER = "<!-- devsync:end:{name} -->"
SECTION_PATTERN = r"<!-- devsync:start:{name} -->\n.*?\n<!-- devsync:end:{name} -->"


class JunieTool(AITool):
    """Integration for JetBrains Junie.

    Junie reads a single .junie/guidelines.md file at the project level.
    DevSync manages individual instruction sections using HTML comment markers:

        <!-- devsync:start:instruction-name -->
        ... instruction content ...
        <!-- devsync:end:instruction-name -->
    """

    @property
    def tool_type(self) -> AIToolType:
        """Return the AI tool type identifier."""
        return AIToolType.JUNIE

    @property
    def tool_name(self) -> str:
        """Return human-readable tool name."""
        return "Junie"

    def is_installed(self) -> bool:
        """Check if Junie is available.

        Detects by looking for JetBrains IDE config directories.

        Returns:
            True if a JetBrains config directory is found
        """
        jetbrains_dir = Path.home() / ".config" / "JetBrains"
        if jetbrains_dir.exists():
            return True
        jetbrains_mac = Path.home() / "Library" / "Application Support" / "JetBrains"
        return jetbrains_mac.exists()

    def get_instructions_directory(self) -> Path:
        """Get the directory where instructions should be installed.

        Raises:
            NotImplementedError: Junie only supports project-level installation
        """
        raise NotImplementedError(
            f"{self.tool_name} global installation is not supported. "
            "Junie uses project-level .junie/guidelines.md only. "
            "Please use project-level installation instead (--scope project)."
        )

    def get_instruction_file_extension(self) -> str:
        """Get the file extension for Junie instructions.

        Returns:
            File extension including the dot
        """
        return ".md"

    def get_project_instructions_directory(self, project_root: Path) -> Path:
        """Get the directory for project-specific Junie instructions.

        Args:
            project_root: Path to the project root directory

        Returns:
            Path to project root's .junie/ directory
        """
        return project_root / ".junie"

    def get_instruction_path(
        self,
        instruction_name: str,
        scope: InstallationScope = InstallationScope.GLOBAL,
        project_root: Optional[Path] = None,
    ) -> Path:
        """Get the path to .junie/guidelines.md.

        Args:
            instruction_name: Name of the instruction (unused for path)
            scope: Installation scope (must be PROJECT)
            project_root: Project root path

        Returns:
            Path to .junie/guidelines.md

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
        return project_root / ".junie" / "guidelines.md"

    def instruction_exists(
        self,
        instruction_name: str,
        scope: InstallationScope = InstallationScope.GLOBAL,
        project_root: Optional[Path] = None,
    ) -> bool:
        """Check if an instruction section exists in guidelines.md.

        Args:
            instruction_name: Name of the instruction
            scope: Installation scope
            project_root: Project root path

        Returns:
            True if the instruction's section markers exist in guidelines.md
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
        """Install an instruction as a section in .junie/guidelines.md.

        Args:
            instruction: Instruction to install
            overwrite: Whether to overwrite existing section
            scope: Installation scope
            project_root: Project root path

        Returns:
            Path to guidelines.md

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
                    raise FileExistsError(f"Instruction already exists in guidelines.md: {instruction.name}")
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
        """Remove an instruction section from guidelines.md.

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
            new_content = re.sub(r"\n{3,}", "\n\n", new_content).strip()
            if new_content:
                new_content += "\n"
            path.write_text(new_content, encoding="utf-8")
            return True
        except (FileNotFoundError, ValueError, NotImplementedError):
            return False

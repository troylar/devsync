"""Antigravity IDE AI tool integration."""

import shutil
from pathlib import Path

from devsync.ai_tools.base import AITool
from devsync.core.models import AIToolType


class AntigravityTool(AITool):
    """Integration for Google's Antigravity IDE (VSCode fork).

    Antigravity uses .agent/rules/*.md for project-level instructions.
    """

    @property
    def tool_type(self) -> AIToolType:
        """Return the AI tool type identifier."""
        return AIToolType.ANTIGRAVITY

    @property
    def tool_name(self) -> str:
        """Return human-readable tool name."""
        return "Antigravity IDE"

    def is_installed(self) -> bool:
        """Check if Antigravity IDE is installed on the system.

        Returns:
            True if antigravity binary is found on PATH or config directory exists
        """
        if shutil.which("antigravity") is not None:
            return True
        antigravity_dir = Path.home() / ".gemini" / "antigravity"
        return antigravity_dir.exists()

    def get_instructions_directory(self) -> Path:
        """Get the directory where instructions should be installed.

        Raises:
            NotImplementedError: Antigravity only supports project-level installation
        """
        raise NotImplementedError(
            f"{self.tool_name} global installation is not supported. "
            "Please use project-level installation instead (--scope project)."
        )

    def get_instruction_file_extension(self) -> str:
        """Get the file extension for Antigravity instructions.

        Returns:
            File extension including the dot
        """
        return ".md"

    def get_project_instructions_directory(self, project_root: Path) -> Path:
        """Get the directory for project-specific Antigravity instructions.

        Antigravity stores project-specific rules in .agent/rules/ directory.

        Args:
            project_root: Path to the project root directory

        Returns:
            Path to project instructions directory (.agent/rules/)
        """
        instructions_dir = project_root / ".agent" / "rules"
        instructions_dir.mkdir(parents=True, exist_ok=True)
        return instructions_dir

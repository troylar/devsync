"""Trae AI tool integration."""

import shutil
from pathlib import Path

from devsync.ai_tools.base import AITool
from devsync.core.models import AIToolType


class TraeTool(AITool):
    """Integration for Trae IDE.

    Trae uses .trae/rules/*.md for project-level instructions.
    """

    @property
    def tool_type(self) -> AIToolType:
        """Return the AI tool type identifier."""
        return AIToolType.TRAE

    @property
    def tool_name(self) -> str:
        """Return human-readable tool name."""
        return "Trae"

    def is_installed(self) -> bool:
        """Check if Trae is installed on the system.

        Returns:
            True if trae binary is found on PATH
        """
        return shutil.which("trae") is not None

    def get_instructions_directory(self) -> Path:
        """Get the directory where instructions should be installed.

        Raises:
            NotImplementedError: Trae only supports project-level installation
        """
        raise NotImplementedError(
            f"{self.tool_name} global installation is not supported. "
            "Please use project-level installation instead (--scope project)."
        )

    def get_instruction_file_extension(self) -> str:
        """Get the file extension for Trae instructions.

        Returns:
            File extension including the dot
        """
        return ".md"

    def get_project_instructions_directory(self, project_root: Path) -> Path:
        """Get the directory for project-specific Trae instructions.

        Args:
            project_root: Path to the project root directory

        Returns:
            Path to project instructions directory (.trae/rules/)
        """
        instructions_dir = project_root / ".trae" / "rules"
        instructions_dir.mkdir(parents=True, exist_ok=True)
        return instructions_dir

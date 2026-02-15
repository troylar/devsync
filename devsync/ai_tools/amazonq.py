"""Amazon Q AI tool integration."""

import shutil
from pathlib import Path

from devsync.ai_tools.base import AITool
from devsync.core.models import AIToolType


class AmazonQTool(AITool):
    """Integration for Amazon Q Developer.

    Amazon Q uses .amazonq/rules/*.md for project-level instructions.
    """

    @property
    def tool_type(self) -> AIToolType:
        """Return the AI tool type identifier."""
        return AIToolType.AMAZONQ

    @property
    def tool_name(self) -> str:
        """Return human-readable tool name."""
        return "Amazon Q"

    def is_installed(self) -> bool:
        """Check if Amazon Q is installed on the system.

        Returns:
            True if q binary is found on PATH or .amazonq/ directory exists
        """
        if shutil.which("q") is not None:
            return True
        amazonq_dir = Path.home() / ".amazonq"
        return amazonq_dir.exists()

    def get_instructions_directory(self) -> Path:
        """Get the directory where instructions should be installed.

        Raises:
            NotImplementedError: Amazon Q only supports project-level installation
        """
        raise NotImplementedError(
            f"{self.tool_name} global installation is not supported. "
            "Please use project-level installation instead (--scope project)."
        )

    def get_instruction_file_extension(self) -> str:
        """Get the file extension for Amazon Q instructions.

        Returns:
            File extension including the dot
        """
        return ".md"

    def get_project_instructions_directory(self, project_root: Path) -> Path:
        """Get the directory for project-specific Amazon Q instructions.

        Args:
            project_root: Path to the project root directory

        Returns:
            Path to project instructions directory (.amazonq/rules/)
        """
        instructions_dir = project_root / ".amazonq" / "rules"
        instructions_dir.mkdir(parents=True, exist_ok=True)
        return instructions_dir

"""Continue.dev AI tool integration."""

from pathlib import Path

from devsync.ai_tools.base import AITool
from devsync.core.models import AIToolType


class ContinueTool(AITool):
    """Integration for Continue.dev.

    Continue.dev uses .continue/rules/*.md for project-level instructions.
    """

    @property
    def tool_type(self) -> AIToolType:
        """Return the AI tool type identifier."""
        return AIToolType.CONTINUE

    @property
    def tool_name(self) -> str:
        """Return human-readable tool name."""
        return "Continue.dev"

    def is_installed(self) -> bool:
        """Check if Continue.dev is installed on the system.

        Returns:
            True if .continue/ directory exists in home
        """
        continue_dir = Path.home() / ".continue"
        return continue_dir.exists()

    def get_instructions_directory(self) -> Path:
        """Get the directory where instructions should be installed.

        Raises:
            NotImplementedError: Continue.dev only supports project-level installation
        """
        raise NotImplementedError(
            f"{self.tool_name} global installation is not supported. "
            "Please use project-level installation instead (--scope project)."
        )

    def get_instruction_file_extension(self) -> str:
        """Get the file extension for Continue.dev instructions.

        Returns:
            File extension including the dot
        """
        return ".md"

    def get_project_instructions_directory(self, project_root: Path) -> Path:
        """Get the directory for project-specific Continue.dev instructions.

        Args:
            project_root: Path to the project root directory

        Returns:
            Path to project instructions directory (.continue/rules/)
        """
        instructions_dir = project_root / ".continue" / "rules"
        instructions_dir.mkdir(parents=True, exist_ok=True)
        return instructions_dir

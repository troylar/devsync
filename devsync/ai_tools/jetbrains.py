"""JetBrains AI Assistant tool integration."""

from pathlib import Path

from devsync.ai_tools.base import AITool
from devsync.core.models import AIToolType


class JetBrainsTool(AITool):
    """Integration for JetBrains AI Assistant.

    JetBrains AI Assistant uses .aiassistant/rules/*.md for project-level instructions.
    """

    @property
    def tool_type(self) -> AIToolType:
        """Return the AI tool type identifier."""
        return AIToolType.JETBRAINS

    @property
    def tool_name(self) -> str:
        """Return human-readable tool name."""
        return "JetBrains AI"

    def is_installed(self) -> bool:
        """Check if JetBrains IDE is installed on the system.

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
            NotImplementedError: JetBrains AI only supports project-level installation
        """
        raise NotImplementedError(
            f"{self.tool_name} global installation is not supported. "
            "Please use project-level installation instead (--scope project)."
        )

    def get_instruction_file_extension(self) -> str:
        """Get the file extension for JetBrains AI instructions.

        Returns:
            File extension including the dot
        """
        return ".md"

    def get_project_instructions_directory(self, project_root: Path) -> Path:
        """Get the directory for project-specific JetBrains AI instructions.

        Args:
            project_root: Path to the project root directory

        Returns:
            Path to project instructions directory (.aiassistant/rules/)
        """
        instructions_dir = project_root / ".aiassistant" / "rules"
        instructions_dir.mkdir(parents=True, exist_ok=True)
        return instructions_dir

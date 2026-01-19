from pathlib import Path

# Root directory the MCP server is allowed to read
CODEBASE_ROOT = Path(".").resolve()

# Directories to ignore
IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
}

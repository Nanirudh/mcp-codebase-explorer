# Codebase Explorer MCP Server

A minimal MCP server that exposes read-only tools for exploring a codebase.

## Requirements
- Python 3.10+
- Recommended: virtual environment (`python -m venv .venv`)


## Tools
- `list_files`: list files/directories (supports recursive)
- `get_file`: read a file with line range limits
- `search_code`: search for a string in the codebase



## Run (single-terminal, auto-launch)
The SDK client will auto-start `server.py` as a subprocess:
```bash
python sdk_client.py
```

## Output:
🔄 Initializing...
✅ Connected & initialized!

Available tools:
  📁 list_files: List files and directories in the codebase
  📁 get_file: Read a file with line range limits
  📁 search_code: Search for a string in the codebase and return matching locations

=== 📂 Current directory ===
{
  "path": ".",
  "directories": [],
  "files": [
    {
      "path": ".python-version",
      "size_bytes": 8
    },
    {
      "path": "README.md",
      "size_bytes": 997
    },
    {
      "path": "config.py",
      "size_bytes": 220
    },
    {
      "path": "sdk_client.py",
      "size_bytes": 5770
    },
    {
      "path": "server.py",
      "size_bytes": 2989
    },
    {
      "path": "simple_client.py",
      "size_bytes": 1301
    },
    {
      "path": "tools.py",
      "size_bytes": 2952
    }
  ],
  "total_files": 7
}

=== 🔍 Recursive scan ===
  📊 Total files: 7
  📁 Directories: 0
  📄 Files: 7

=== 📖 Reading server.py ===
  Lines 1-99/99
  Preview:
      1: from mcp.server import Server
      2: from mcp.server.stdio import stdio_server
      3: from mcp.server.models import InitializationOptions
      4: from mcp.types import Tool
      5: import asyncio
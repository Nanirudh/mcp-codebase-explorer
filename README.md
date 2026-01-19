# Codebase Explorer MCP Server

A minimal MCP server that exposes read-only tools for exploring a codebase.

## Requirements
- Python 3.10+
- Recommended: virtual environment (`python -m venv .venv`)


## Tools
- `list_files`: list files/directories (supports recursive) <br>
- `get_file`: read a file with line range limits <br>
- `search_code`: search for a string in the codebase <br>



## Run (single-terminal, auto-launch)
The SDK client will auto-start `server.py` as a subprocess:
```bash
python sdk_client.py
```

## Output:
🔄 Initializing... <br>
✅ Connected & initialized! <br>

Available tools: <br>
  📁 list_files: List files and directories in the codebase <br>
  📁 get_file: Read a file with line range limits <br>
  📁 search_code: Search for a string in the codebase and return matching locations <br>

=== 📂 Current directory === <br>
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

=== 🔍 Recursive scan === <br>
  📊 Total files: 7 <br>
  📁 Directories: 0 <br>
  📄 Files: 7 <br>

=== 📖 Reading server.py === <br>
  Lines 1-99/99 <br>
  Preview: <br>
      1: from mcp.server import Server <br>
      2: from mcp.server.stdio import stdio_server <br>
      3: from mcp.server.models import InitializationOptions <br>
      4: from mcp.types import Tool <br>
      5: import asyncio <br>

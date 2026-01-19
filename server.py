from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import Tool
import asyncio

from tools import list_files, get_file, search_code

server = Server(
    name="codebase-explorer",
    version="0.3.0",
    description="Read-only MCP server for exploring a codebase",
)

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="list_files",
            description="List files and directories in the codebase",
            input_schema={
                "type": "object",
                "properties": {
                    "root_path": {"type": "string", "default": "."},
                    "recursive": {"type": "boolean", "default": False},
                },
            },
        ),
        Tool(
            name="get_file",
            description="Read a file with line range limits",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "start_line": {"type": "integer", "default": 1},
                    "end_line": {"type": "integer", "default": 200},
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="search_code",
            description="Search for a string in the codebase and return matching locations",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "path": {"type": "string", "default": "."},
                },
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "list_files":
        return list_files(
            root_path=arguments.get("root_path", "."),
            recursive=arguments.get("recursive", False),
        )

    if name == "get_file":
        return get_file(
            path=arguments["path"],
            start_line=arguments.get("start_line", 1),
            end_line=arguments.get("end_line", 200),
        )

    if name == "search_code":
        return search_code(
            query=arguments["query"],
            path=arguments.get("path", "."),
        )

    raise ValueError(f"Unknown tool: {name}")

async def main():
    from mcp.server.lowlevel.server import NotificationOptions
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=server.name,
                server_version=server.version or "0.3.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            )
        )

if __name__ == "__main__":
    asyncio.run(main())


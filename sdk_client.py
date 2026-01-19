# sdk_client.py (FINAL WORKING VERSION)
import asyncio
import json
import os
import sys
import traceback
from mcp.client import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.types import Implementation

async def main():
    # Server parameters to auto-launch server.py
    # Use sys.executable to ensure we use the same Python interpreter (venv)
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"],
        env={**os.environ}  # Inherit environment
    )
    
    async with stdio_client(server_params) as (read_stream, write_stream):
        # Create client_info to pass to ClientSession
        client_info = Implementation(
            name="codebase-explorer-client",
            version="0.1.0"
        )
        
        async with ClientSession(read_stream, write_stream, client_info=client_info) as session:
            
            print("🔄 Initializing...")
            
            # CRITICAL: Proper MCP initialization sequence
            # Initialize (uses client_info from constructor and sends initialized notification internally)
            await session.initialize()
            
            print("✅ Connected & initialized!")
            
            # Now safe to use tools
            tools = await session.list_tools()
            print("\nAvailable tools:")
            for tool in tools.tools:
                print(f"  📁 {tool.name}: {tool.description}")
            print()
            
            # Test list_files
            print("=== 📂 Current directory ===")
            result = await session.call_tool(
                name="list_files",
                arguments={"root_path": ".", "recursive": False}
            )
            # result.content is a list of ContentBlock objects, extract text
            content_text = ""
            for block in result.content:
                if hasattr(block, 'text'):
                    content_text += block.text
            if content_text:
                # Try to parse as JSON for pretty printing
                try:
                    data = json.loads(content_text)
                    print(json.dumps(data, indent=2))
                except json.JSONDecodeError:
                    print(content_text)
            print()
            
            # Test recursive
            print("=== 🔍 Recursive scan ===")
            result = await session.call_tool(
                name="list_files",
                arguments={"root_path": ".", "recursive": True}
            )
            # Extract JSON from content blocks
            content_text = ""
            for block in result.content:
                if hasattr(block, 'text'):
                    content_text += block.text
            data = json.loads(content_text) if content_text else {}
            print(f"  📊 Total files: {data.get('total_files', 0)}")
            print(f"  📁 Directories: {len(data.get('directories', []))}")
            print(f"  📄 Files: {len(data.get('files', []))}")
            
            # Test get_file (server.py)
            print("\n=== 📖 Reading server.py ===")
            try:
                result = await session.call_tool(
                    name="get_file",
                    arguments={"path": "server.py"}
                )
                # Extract JSON from content blocks
                content_text = ""
                for block in result.content:
                    if hasattr(block, 'text'):
                        content_text += block.text
                data = json.loads(content_text) if content_text else {}
                print(f"  Lines {data.get('start_line', 0)}-{data.get('end_line', 0)}/{data.get('total_lines', 0)}")
                print("  Preview:")
                content_lines = data.get('content', [])
                start_line = data.get('start_line', 1)
                for i, line in enumerate(content_lines[:5], 1):
                    print(f"    {start_line+i-1:3d}: {line}")
                if data.get('truncated', False):
                    print("         ... (truncated)")
            except Exception as e:
                print(f"  ❌ Error: {e}")

def print_exception_group(eg, indent=0):
    """Recursively print ExceptionGroup and its nested exceptions"""
    prefix = "  " * indent
    print(f"{prefix}{type(eg).__name__}: {eg}")
    if hasattr(eg, 'exceptions'):
        for i, exc in enumerate(eg.exceptions, 1):
            print(f"{prefix}  Sub-exception {i}: {type(exc).__name__}: {exc}")
            if hasattr(exc, 'exceptions'):
                # Nested ExceptionGroup
                print_exception_group(exc, indent + 1)
            else:
                # Regular exception - print traceback
                import sys
                print(f"{prefix}    Traceback:")
                tb_lines = traceback.format_exception(type(exc), exc, exc.__traceback__, limit=10)
                for line in tb_lines:
                    for tb_line in line.rstrip().split('\n'):
                        if tb_line.strip():
                            print(f"{prefix}      {tb_line}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        # Handle ExceptionGroup (from TaskGroup or anyio)
        if hasattr(e, 'exceptions'):
            print(f"❌ Error: {type(e).__name__}")
            print_exception_group(e)
        else:
            print(f"❌ Error: {type(e).__name__}: {e}")
            print(f"\nFull traceback:")
            traceback.print_exception(type(e), e, e.__traceback__)
        print("\n💡 Make sure server.py is in the same directory and all dependencies are installed!")

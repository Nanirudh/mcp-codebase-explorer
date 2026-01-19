# connect_client.py (connects to RUNNING server)
import asyncio
import sys
import json
import os

async def connect_to_running_server():
    # Connect to ALREADY RUNNING server.py via stdin/stdout
    print("🔗 Connecting to running MCP server...")
    
    # Use direct stdio - no stdio_client needed
    loop = asyncio.get_event_loop()
    read = asyncio.StreamReader()
    read_protocol = asyncio.StreamReaderProtocol(read)
    write_obj = asyncio.StreamWriter(read_protocol, loop)
    
    # Send list_tools request
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "list_tools"
    }
    
    # For simplicity, use blocking I/O for demo
    print("📡 Sending list_tools request...")
    sys.stdout.write(json.dumps(request) + "\n")
    sys.stdout.flush()
    
    # Read response
    response = sys.stdin.readline().strip()
    if response:
        data = json.loads(response)
        print("✅ Success! Available tools:")
        for tool in data.get("result", {}).get("tools", []):
            print(f"  📁 {tool['name']}: {tool['description'][:50]}...")
    else:
        print("❌ No response received")

if __name__ == "__main__":
    try:
        asyncio.run(connect_to_running_server())
    except KeyboardInterrupt:
        print("\n👋 Disconnected")

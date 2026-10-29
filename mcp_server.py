import subprocess
import os
from mcp.server.mcpserver import MCPServer
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = MCPServer("talent-sourcing-mcp")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="exec_command",
            description="Execute a shell command and return output",
            inputSchema={
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"]
            }
        ),
        Tool(
            name="list_files",
            description="List files in a directory",
            inputSchema={
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "exec_command":
        command = arguments.get("command", "")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
            return [TextContent(type="text", text=f"CODE:{result.returncode}\nSTDOUT:{result.stdout}\nSTDERR:{result.stderr}")]
        except Exception as e:
            return [TextContent(type="text", text=f"ERROR:{e}")]
    elif name == "list_files":
        path = arguments.get("path", ".")
        try:
            files = os.listdir(path)
            return [TextContent(type="text", text="\n".join(files))]
        except Exception as e:
            return [TextContent(type="text", text=f"ERROR:{e}")]
    return [TextContent(type="text", text="TalentSourcing OS ONLINE")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

import subprocess
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("talent-sourcing-mcp")

@app.list_tools()
async def list_tools():
    return [
        Tool(name="exec_command", description="Execute shell command", inputSchema={"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}),
        Tool(name="list_files", description="List files in directory", inputSchema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]})
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "exec_command":
        try:
            r = subprocess.run(arguments["command"], shell=True, capture_output=True, text=True, timeout=60)
            return [TextContent(type="text", text=f"CODE:{r.returncode}\nSTDOUT:{r.stdout}\nSTDERR:{r.stderr}")]
        except Exception as e:
            return [TextContent(type="text", text=f"ERROR:{e}")]
    elif name == "list_files":
        try:
            return [TextContent(type="text", text="\n".join(os.listdir(arguments.get("path", "."))))]
        except Exception as e:
            return [TextContent(type="text", text=f"ERROR:{e}")]
    return [TextContent(type="text", text="TalentSourcing OS ONLINE")]

async def main():
    async with stdio_server() as (r, w):
        await app.run(r, w, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

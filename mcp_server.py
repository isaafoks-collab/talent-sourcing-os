import subprocess, os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server('talent-sourcing')

@app.list_tools()
async def list_tools():
    return [
        Tool(name='list_files', description='List files', inputSchema={'type': 'object', 'properties': {'path': {'type': 'string'}}, 'required': ['path']}),
        Tool(name='exec_command', description='Run command', inputSchema={'type': 'object', 'properties': {'command': {'type': 'string'}}, 'required': ['command']})
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == 'list_files':
        try: return [TextContent(type='text', text='\n'.join(os.listdir(arguments.get('path', '.'))))]
        except Exception as e: return [TextContent(type='text', text=f'ERROR:{e}')]
    elif name == 'exec_command':
        try:
            r = subprocess.run(arguments['command'], shell=True, capture_output=True, text=True, timeout=60)
            return [TextContent(type='text', text=f'CODE:{r.returncode}\nSTDOUT:{r.stdout}\nSTDERR:{r.stderr}')]
        except Exception as e: return [TextContent(type='text', text=f'ERROR:{e}')]
    return [TextContent(type='text', text='ONLINE')]

async def main():
    async with stdio_server() as (r, w): await app.run(r, w, app.create_initialization_options())

if __name__ == '__main__':
    import asyncio; asyncio.run(main())

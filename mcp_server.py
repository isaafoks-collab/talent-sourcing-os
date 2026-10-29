import subprocess,json,psutil
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool,TextContent
app=Server("talent-sourcing-mcp")
@app.list_tools()
async def lt(): return [Tool(name="exec",description="Выполнить команду в системе",inputSchema={"type":"object","properties":{"command":{"type":"string"}},"required":["command"]}),Tool(name="status",description="Статус системы",inputSchema={"type":"object","properties":{}})]
@app.call_tool()
async def ct(n:str,a:dict):
    if n=="exec":
        try: r=subprocess.run(a["command"],shell=True,capture_output=True,text=True,timeout=60); return [TextContent(type="text",text=f"CODE:{r.returncode}\n{r.stdout}\n{r.stderr}")]
        except Exception as e: return [TextContent(type="text",text=f"ERROR:{e}")]
    return [TextContent(type="text",text="TalentSourcing OS ONLINE")]
async def main():
    async with stdio_server() as (r,w): await app.run(r,w,app.create_initialization_options())
if __name__=="__main__": import asyncio; asyncio.run(main())

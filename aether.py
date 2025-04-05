from mcp.server.fastmcp import FastMCP
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai import Agent
from dotenv import load_dotenv
import asyncio
from pydantic import BaseModel
import logfire
class CommandType(BaseModel):
    command:str
    args:list[str]

logfire.configure(token="pylf_v1_eu_VR1vgxK6pKpj0ss6SwWjCWhv0B5lTmDPjkwLx5vq7nNt")  
logfire.instrument_anthropic()

load_dotenv()

mcp = FastMCP("weather")

def spin_up_agent(serverCommands: CommandType):
    mcp_server_list = []
    for c in serverCommands:
        server = MCPServerStdio(command=c.command, args=c.args)
        mcp_server_list.append(server)
    print(mcp_server_list)
    agent = Agent("anthropic:claude-3-7-sonnet-latest", mcp_servers=mcp_server_list)
    return agent

async def main():
    c = [CommandType(command="docker", args=["run", "-i", "--rm", "mcp/time"]),
         CommandType(command="docker", args=["run", "-i", "--rm", "--mount", "type=bind,src=/c/Users/Chris/Desktop/Bewerbungen/test,dst=/c/Users/Chris/Desktop/Bewerbungen/test","mcp/git"])]
    agent = spin_up_agent(c)
    async with agent.run_mcp_servers():
        response = await agent.run("init a git repo in /c/Users/Chris/Desktop/Bewerbungen/test")
        print(response.data)

if __name__ == "__main__":
    asyncio.run(main())

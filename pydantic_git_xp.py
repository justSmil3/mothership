from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai import Agent
from dotenv import load_dotenv
import asyncio

load_dotenv()

server = MCPServerStdio(
        command="docker",
        args=["run", "--rm", "-i", "mcp/time"]
        )

agent = Agent(
        model="anthropic:claude-3-7-sonnet-latest",
        mcp_servers=[]
        )

agent._mcp_servers = [server]

async def main():
    async with agent.run_mcp_servers():
        response=await agent.run("what is the current time")
        print(response.data)

if __name__ == "__main__":
    asyncio.run(main())

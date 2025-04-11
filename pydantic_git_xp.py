from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai import Agent
from dotenv import load_dotenv
import asyncio
import json

load_dotenv()

with open("./mcp_servers/time.json", 'r', encoding="utf-8") as f:
    server_data = json.loads(f.read())


server = MCPServerStdio(
        command=server_data['command'],
        args=server_data['args']
        )

agent = Agent(
        model="anthropic:claude-3-7-sonnet-latest",
        mcp_servers=[]
        )

agent._mcp_servers = [server]

async def main():
    async with agent.run_mcp_servers():
        response=await agent.run("what is the current time in bali, and what time is it in frankfurt")
        print(response.data)

if __name__ == "__main__":
    asyncio.run(main())

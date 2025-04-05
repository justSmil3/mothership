from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from dotenv import load_dotenv
import asyncio

load_dotenv()

server = MCPServerStdio("uv", ["run", "mcp_xp.py"])
agent = Agent("openai:gpt-4o", mcp_servers=[server])

async def main():
    print("c")
    async with agent.run_mcp_servers():
        print('a')
        result = await agent.run('what is the langchain documentation containing for information about the usage of mcp server with langchain agends ? ')
        print('b')
    print(result.data)

if __name__ == "__main__":
    asyncio.run(main())


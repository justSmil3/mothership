from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.mcp import MCPServerStdio
import asyncio
import os
from dotenv import dotenv_values, load_dotenv
import logfire

# configure logfire
logfire.configure(token='pylf_v1_eu_VR1vgxK6pKpj0ss6SwWjCWhv0B5lTmDPjkwLx5vq7nNt')
logfire.instrument_anthropic()

env_vars = dotenv_values(".env")
load_dotenv()

server = MCPServerStdio("uv", ["run", "mothership.py"])
model = AnthropicModel(
        "claude-3-7-sonnet-20250219", provider=AnthropicProvider(api_key=env_vars.get("ANTHROPIC_API_KEY"))
        )
agent = Agent(
        model=model,
        mcp_servers=[server],
        system_prompt="You are a helpful assistant"
        )

async def main():
    async with agent.run_mcp_servers():
        result = await agent.run('fetch the web for most relevant informations about mcp marketplaces, compile a list of all of those things and add the current time in frankfurt to it')
    print(result.data)

if __name__ == "__main__":
    asyncio.run(main())

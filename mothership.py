from mcp.server.fastmcp import FastMCP
from langgraph.types import Command

mcp = FastMCP("mothership")

def swarm_handoff():
    # cannot handoff to another node because I cannto adapt the graph
    ...

@mcp.tool()
def call_to_mothership(tasks: list[str]) -> list[str]:
    """
    Dynamically sets up another agend based on a list of tasks that an LLM cannot acomplish without a tool call. The new agend will be equipped with all the nessesary tools needed to acomplish the given tasks.

    Args:
        tasks: A list of tasks that need to be acomplished.

    Returns:
        results: A list of results.
    """

    for task in tasks:
        ...
        # retrieve a tools 
        # add tools to a list

    # bind tool to a new agent
    # prompt the new agent
    # return the results

    # i do need to create a agend in here compiled with tools etc

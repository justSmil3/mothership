from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mining laser")





@mcp.tool()
def forge_pickaxe(tasks: list[str]) -> list[str]:
    """
    Dynamically sets up another agend based on a list of tasks that an LLM cannot really acomplish on its own. the new agend will be equipped with all the nessesary tools needed to acomplish the given tasks.

    Args: 
        tasks: A list of tasks tht need to be acomplished.

    Returns: 
        results: A list of results
    """

    print(tasks)
    return []


if __name__ == "__main__":
    mcp.run(transport="stdio")

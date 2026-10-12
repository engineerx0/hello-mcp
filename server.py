from mcp.server import MCPServer

mcp = MCPServer("Hello MCP")


@mcp.tool()
def hello(name: str) -> str:
    """
    Return a greeting.
    """
    return f"Hello {name}!"


if __name__ == "__main__":
    mcp.run()
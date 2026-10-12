import asyncio

from mcp.client import ClientSession
from mcp.client.stdio import (
    StdioServerParameters,
    stdio_client,
)


async def main():

    # Configure MCP server startup
    server = StdioServerParameters(
        command="python",
        args=["server_ping_google.py"],
    )

    print("Starting server...\n")

    # Start MCP server
    async with stdio_client(server) as (read_stream, write_stream):

        print("Connected to server.")

        # Create MCP session
        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            print("Initializing session...")

            await session.initialize()

            print("Session initialized.\n")


            # List available tools
            print("Available tools:")

            tools_result = await session.list_tools()

            for tool in tools_result.tools:
                print(f" - {tool.name}")

            print()


            # Call tool
            print("Calling ping_google()...\n")

            result = await session.call_tool(
                "ping_google",
                {}
            )


            print("Tool Response:")

            if result.content:
                for item in result.content:
                    if hasattr(item, "text"):
                        print(item.text)

            else:
                print(result.structured_content)


if __name__ == "__main__":
    asyncio.run(main())
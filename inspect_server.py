import asyncio
from server import mcp

async def main():
    print("Server Name:", mcp.name)

    print("\nRegistered tools:")

    tools = await mcp.list_tools()

    for tool in tools:
        print("-", tool.name)


asyncio.run(main())

print()

from server_ping_google import mcp

async def main():
    print("Server Name:", mcp.name)

    print("\nRegistered tools:")

    tools = await mcp.list_tools()

    for tool in tools:
        print("-", tool.name)


asyncio.run(main())
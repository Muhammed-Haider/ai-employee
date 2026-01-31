import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    env = {
        **os.environ,
        # Secrets removed for security. Please set these in your environment variables.
    }
    
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "gmail-mcp-server"],
        env=env
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Available Tools:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

if __name__ == "__main__":
    asyncio.run(main())

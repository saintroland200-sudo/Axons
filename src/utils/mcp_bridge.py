import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import Any, Dict, List, Optional

class MCPBridge:
    def __init__(self, server_command: str, server_args: List[str] = []):
        self.server_params = StdioServerParameters(
            command=server_command,
            args=server_args,
            env=None
        )
        self.session: Optional[ClientSession] = None
        self._exit_stack = None

    async def connect(self):
        from contextlib import AsyncExitStack
        self._exit_stack = AsyncExitStack()

        # This setup is based on the MCP Python SDK client documentation
        transport = await self._exit_stack.enter_async_context(stdio_client(self.server_params))
        self.session = await self._exit_stack.enter_async_context(ClientSession(transport[0], transport[1]))
        await self.session.initialize()

    async def list_tools(self) -> List[Any]:
        if not self.session:
            raise RuntimeError("MCP Bridge not connected")
        tools_result = await self.session.list_tools()
        return tools_result.tools

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        if not self.session:
            raise RuntimeError("MCP Bridge not connected")
        return await self.session.call_tool(tool_name, arguments)

    async def disconnect(self):
        if self._exit_stack:
            await self._exit_stack.aclose()

# Example usage/test script
async def test_bridge():
    # Using a simple echo server if available, or just mocking for the bridge logic
    bridge = MCPBridge("python3", ["-c", "import sys; print('mock server')"])
    # Note: Connecting to a non-MCP server will fail initialization,
    # but we are testing the class structure here.
    print("MCP Bridge initialized.")

if __name__ == "__main__":
    asyncio.run(test_bridge())

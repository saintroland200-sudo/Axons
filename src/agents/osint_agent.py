import asyncio
import threading
import time
from src.acp.bus import ACPBus, ACPMessage
from src.utils.mcp_bridge import MCPBridge

class OSINTAgent:
    def __init__(self):
        self.bus = ACPBus()
        self.name = "OSINT"
        # In a real scenario, this would point to the installed osint-mcp-server
        # For this clone, we configure the command to run it.
        # Assuming badchars/osint-mcp-server is installed via npx or similar.
        self.bridge = MCPBridge("npx", ["-y", "@badchars/osint-mcp-server"])
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.thread.start()
        self.running = True

    def _run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def _async_handle_message(self, message: ACPMessage):
        topic = message.topic
        payload = message.payload

        try:
            if topic == "osint_list_tools":
                # Ensure connected
                if not self.bridge.session:
                    await self.bridge.connect()
                tools = await self.bridge.list_tools()
                self.bus.send(ACPMessage(self.name, message.sender, "osint_list_tools_res", {"tools": [t.name for t in tools]}))

            elif topic == "osint_call_tool":
                if not self.bridge.session:
                    await self.bridge.connect()
                tool_name = payload["tool"]
                args = payload.get("args", {})
                result = await self.bridge.call_tool(tool_name, args)
                self.bus.send(ACPMessage(self.name, message.sender, "osint_call_tool_res", {"result": result, "status": "success"}))

        except Exception as e:
            self.bus.send(ACPMessage(self.name, message.sender, f"{topic}_res", {"status": "error", "message": str(e)}))

    def handle_message(self, message: ACPMessage):
        asyncio.run_coroutine_threadsafe(self._async_handle_message(message), self.loop)

    def run_once(self):
        messages = self.bus.receive(self.name)
        for msg in messages:
            self.handle_message(msg)

if __name__ == "__main__":
    agent = OSINTAgent()
    print("OSINT Agent started...")
    while True:
        agent.run_once()
        time.sleep(1)

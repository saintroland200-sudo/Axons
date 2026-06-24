import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import os
import time
from src.acp.bus import ACPBus, ACPMessage
from src.agents.osint_agent import OSINTAgent

class TestOSINTAgent(unittest.TestCase):
    def setUp(self):
        self.queue = "test_osint_queue.json"
        if os.path.exists(self.queue):
            os.remove(self.queue)
        self.bus = ACPBus(self.queue)

        # We need to mock the bridge to avoid running actual npx
        with patch("src.agents.osint_agent.MCPBridge") as MockBridge:
            self.agent = OSINTAgent()
            self.agent.bridge = MockBridge.return_value
            self.agent.bus = self.bus

    def tearDown(self):
        if os.path.exists(self.queue):
            os.remove(self.queue)
        self.agent.loop.stop()

    def test_osint_list_tools(self):
        mock_tool = MagicMock()
        mock_tool.name = "shodan_search"
        self.agent.bridge.list_tools = AsyncMock(return_value=[mock_tool])
        self.agent.bridge.session = True # Mock connection

        msg = ACPMessage(sender="User", receiver="OSINT", topic="osint_list_tools", payload={})
        self.bus.send(msg)

        self.agent.run_once()

        # Give some time for the async task to complete in the loop thread
        time.sleep(0.5)

        responses = self.bus.receive("User")
        self.assertTrue(len(responses) > 0)
        self.assertIn("shodan_search", responses[0].payload["tools"])

if __name__ == "__main__":
    unittest.main()

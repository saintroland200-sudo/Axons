import unittest
import os
import time
import shutil
from src.acp.bus import ACPBus, ACPMessage
from src.agents.opencode import OpenCodeAgent
from src.security.grid import SecurityGrid

class TestLAISIntegration(unittest.TestCase):
    def setUp(self):
        self.queue = "integration_queue.json"
        self.workspace = "integration_workspace"
        if os.path.exists(self.queue): os.remove(self.queue)
        if os.path.exists(self.workspace): shutil.rmtree(self.workspace)

        self.bus = ACPBus(self.queue)
        self.security = SecurityGrid()
        self.opencode = OpenCodeAgent(self.workspace)
        self.opencode.bus = self.bus

    def tearDown(self):
        if os.path.exists(self.queue): os.remove(self.queue)
        if os.path.exists(self.workspace): shutil.rmtree(self.workspace)

    def test_full_flow(self):
        # 1. User sends a message via AIEngine (simulated)
        msg = ACPMessage(sender="User", receiver="OpenCode", topic="file_write", payload={"path": "test.txt", "content": "integration data"})

        # 2. Security Check
        if self.security.check_message(msg):
            self.bus.send(msg)

        # 3. Agent Processes
        self.opencode.run_once()

        # 4. Verify Response
        responses = self.bus.receive("User")
        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0].payload["status"], "success")

if __name__ == "__main__":
    unittest.main()

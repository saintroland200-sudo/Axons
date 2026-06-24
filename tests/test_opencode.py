import unittest
import os
import shutil
import time
from src.acp.bus import ACPBus, ACPMessage
from src.agents.opencode import OpenCodeAgent

class TestOpenCode(unittest.TestCase):
    def setUp(self):
        self.workspace = "test_workspace"
        self.queue = "test_queue.json"
        if os.path.exists(self.workspace):
            shutil.rmtree(self.workspace)
        if os.path.exists(self.queue):
            os.remove(self.queue)

        self.bus = ACPBus(self.queue)
        self.agent = OpenCodeAgent(self.workspace)
        self.agent.bus = self.bus # Inject test bus

    def tearDown(self):
        if os.path.exists(self.workspace):
            shutil.rmtree(self.workspace)
        if os.path.exists(self.queue):
            os.remove(self.queue)

    def test_file_write_read(self):
        # Send write request
        write_msg = ACPMessage(sender="User", receiver="OpenCode", topic="file_write", payload={"path": "hello.txt", "content": "world"})
        self.bus.send(write_msg)

        self.agent.run_once()

        # Check write response
        responses = self.bus.receive("User")
        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0].topic, "file_write_res")

        # Send read request
        read_msg = ACPMessage(sender="User", receiver="OpenCode", topic="file_read", payload={"path": "hello.txt"})
        self.bus.send(read_msg)

        self.agent.run_once()

        responses = self.bus.receive("User")
        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0].payload["content"], "world")

    def test_security_violation(self):
        bad_msg = ACPMessage(sender="User", receiver="OpenCode", topic="file_read", payload={"path": "../secret.txt"})
        self.bus.send(bad_msg)

        self.agent.run_once()

        responses = self.bus.receive("User")
        self.assertEqual(responses[0].payload["status"], "error")
        self.assertIn("Access denied", responses[0].payload["message"])

if __name__ == "__main__":
    unittest.main()

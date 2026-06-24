import unittest
import os
from src.acp.bus import ACPBus, ACPMessage
from src.agents.jarvis import JARVISAgent

class TestJARVIS(unittest.TestCase):
    def setUp(self):
        self.queue = "test_jarvis_queue.json"
        if os.path.exists(self.queue):
            os.remove(self.queue)
        self.bus = ACPBus(self.queue)
        self.agent = JARVISAgent(use_mock=True)
        self.agent.bus = self.bus

    def tearDown(self):
        if os.path.exists(self.queue):
            os.remove(self.queue)

    def test_voice_command_trigger(self):
        # Simulate a voice command sent via bus (mocked input)
        msg = ACPMessage(sender="User", receiver="JARVIS", topic="voice_command", payload={"text": "list files"})
        self.bus.send(msg)

        # Run agent logic
        messages = self.bus.receive("JARVIS")
        for m in messages:
            self.agent.process_voice_command(m.payload["text"])

        # JARVIS should have sent a message to OpenCode
        queued = self.bus.peek()
        found = any(m["receiver"] == "OpenCode" and m["topic"] == "file_list" for m in queued)
        self.assertTrue(found)

if __name__ == "__main__":
    unittest.main()

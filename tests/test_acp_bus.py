import unittest
import os
import shutil
from src.acp.bus import ACPBus, ACPMessage

class TestACPBus(unittest.TestCase):
    def setUp(self):
        self.test_queue = "test_queue.json"
        self.bus = ACPBus(self.test_queue)

    def tearDown(self):
        if os.path.exists(self.test_queue):
            os.remove(self.test_queue)

    def test_send_receive(self):
        msg = ACPMessage(sender="AgentA", receiver="AgentB", topic="test", payload={"data": 123})
        self.bus.send(msg)

        messages = self.bus.receive("AgentB")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].sender, "AgentA")
        self.assertEqual(messages[0].payload["data"], 123)

    def test_broadcast(self):
        msg = ACPMessage(sender="AgentA", receiver="broadcast", topic="test", payload={"data": "all"})
        self.bus.send(msg)

        messages = self.bus.receive("AgentC")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].payload["data"], "all")

    def test_receive_filtering(self):
        msg1 = ACPMessage(sender="AgentA", receiver="AgentB", topic="test", payload={"id": 1})
        msg2 = ACPMessage(sender="AgentA", receiver="AgentC", topic="test", payload={"id": 2})
        self.bus.send(msg1)
        self.bus.send(msg2)

        messages_b = self.bus.receive("AgentB")
        self.assertEqual(len(messages_b), 1)
        self.assertEqual(messages_b[0].payload["id"], 1)

        messages_c = self.bus.receive("AgentC")
        self.assertEqual(len(messages_c), 1)
        self.assertEqual(messages_c[0].payload["id"], 2)

if __name__ == "__main__":
    unittest.main()

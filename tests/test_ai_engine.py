import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Mock tkinter before importing AIEngineGUI
mock_tk = MagicMock()
sys.modules['tkinter'] = mock_tk
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['tkinter.scrolledtext'] = MagicMock()

from src.agents.ai_engine import AIEngineGUI
from src.acp.bus import ACPBus, ACPMessage

class TestAIEngineLogic(unittest.TestCase):
    def setUp(self):
        self.queue = "test_ai_queue.json"
        if os.path.exists(self.queue):
            os.remove(self.queue)
        self.bus = ACPBus(self.queue)

        self.root = MagicMock()
        # Mocking StringVars
        self.app = AIEngineGUI(self.root)
        self.app.bus = self.bus

        self.app.topic_var = MagicMock()
        self.app.payload_var = MagicMock()
        self.app.receiver_var = MagicMock()

    def tearDown(self):
        if os.path.exists(self.queue):
            os.remove(self.queue)

    def test_send_message_logic(self):
        self.app.topic_var.get.return_value = "test_topic"
        self.app.payload_var.get.return_value = '{"key": "value"}'
        self.app.receiver_var.get.return_value = "TestReceiver"

        self.app.send_message()

        queued = self.bus.peek()
        self.assertEqual(len(queued), 1)
        self.assertEqual(queued[0]["topic"], "test_topic")
        self.assertEqual(queued[0]["receiver"], "TestReceiver")

if __name__ == "__main__":
    unittest.main()

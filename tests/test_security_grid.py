import unittest
from src.security.grid import SecurityGrid
from src.acp.bus import ACPMessage

class TestSecurityGrid(unittest.TestCase):
    def setUp(self):
        self.grid = SecurityGrid()

    def test_permission_allowed(self):
        msg = ACPMessage("AIEngine", "OpenCode", "file_list", {"path": "."})
        self.assertTrue(self.grid.check_message(msg))

    def test_permission_denied(self):
        msg = ACPMessage("OSINT", "OpenCode", "file_write", {"path": "bad.sh", "content": "rm -rf"})
        self.assertFalse(self.grid.check_message(msg))

    def test_rate_limiting(self):
        msg = ACPMessage("User", "AIEngine", "ping", {})
        for _ in range(100):
            self.grid.check_message(msg)
        self.assertFalse(self.grid.check_message(msg))

if __name__ == "__main__":
    unittest.main()

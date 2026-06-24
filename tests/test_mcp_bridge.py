import unittest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from src.utils.mcp_bridge import MCPBridge

class TestMCPBridge(unittest.TestCase):
    def setUp(self):
        self.bridge = MCPBridge("mock_command")

    @patch("src.utils.mcp_bridge.stdio_client")
    @patch("src.utils.mcp_bridge.ClientSession")
    async def _test_connect(self, mock_session_cls, mock_stdio):
        # Mocking the async context managers
        mock_transport = (MagicMock(), MagicMock())
        mock_stdio.return_value.__aenter__.return_value = mock_transport

        mock_session = AsyncMock()
        mock_session_cls.return_value.__aenter__.return_value = mock_session

        await self.bridge.connect()
        self.assertTrue(mock_session.initialize.called)

    def test_connect_structure(self):
        # Basic structural test
        self.assertEqual(self.bridge.server_params.command, "mock_command")

if __name__ == "__main__":
    unittest.main()

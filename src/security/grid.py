import time
import logging
from typing import Dict, Any, List, Optional
from src.acp.bus import ACPMessage

class SecurityGrid:
    def __init__(self):
        self.logs = []
        self.rate_limits = {} # {sender: [timestamps]}
        # Permission map: sender -> { receiver -> [topics] }
        self.permissions = {
            "AIEngine": {"*": ["*"]},
            "User": {
                "OpenCode": ["file_read", "file_write", "file_list"],
                "OSINT": ["osint_list_tools", "osint_call_tool"],
                "JARVIS": ["speak", "voice_command", "process_voice_command"]
            },
            "JARVIS": {
                "OpenCode": ["file_list"],
                "AIEngine": ["log"]
            },
            "OpenCode": {
                "AIEngine": ["log"],
                "User": ["file_read_res", "file_write_res", "file_list_res"]
            },
            "OSINT": {
                "AIEngine": ["log"],
                "User": ["osint_list_tools_res", "osint_call_tool_res"]
            }
        }

    def _audit(self, message: str, level: str = "INFO"):
        entry = {"timestamp": time.time(), "level": level, "message": message}
        self.logs.append(entry)
        # Using print for visibility in logs during development
        # print(f"[SecurityGrid] {level}: {message}")

    def check_message(self, message: ACPMessage) -> bool:
        # 1. Authentication
        if not message.sender:
            self._audit(f"Authentication Failed: No sender", "CRITICAL")
            return False

        # 2. Permissions
        sender_perms = self.permissions.get(message.sender, {})
        allowed_topics = sender_perms.get(message.receiver, sender_perms.get("*", []))

        if "*" not in allowed_topics and message.topic not in allowed_topics:
            self._audit(f"Permission Denied: {message.sender} -> {message.receiver} [{message.topic}]", "WARNING")
            return False

        # 3. Rate Limiting
        now = time.time()
        user_hits = [h for h in self.rate_limits.get(message.sender, []) if now - h < 60]
        if len(user_hits) >= 100:
            self._audit(f"Rate Limit Exceeded: {message.sender}", "WARNING")
            return False
        user_hits.append(now)
        self.rate_limits[message.sender] = user_hits

        # 4. Input Validation
        if len(str(message.payload)) > 100000:
            self._audit(f"Input too large from {message.sender}", "WARNING")
            return False

        self._audit(f"Allowed: {message.sender} -> {message.receiver} [{message.topic}]")
        return True

if __name__ == "__main__":
    grid = SecurityGrid()
    msg = ACPMessage("User", "OpenCode", "file_read", {"path": "test.txt"})
    print(f"Allowed: {grid.check_message(msg)}")

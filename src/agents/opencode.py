import os
import json
from src.acp.bus import ACPBus, ACPMessage

class OpenCodeAgent:
    def __init__(self, workspace_dir: str = "workspace"):
        self.workspace_dir = os.path.abspath(workspace_dir)
        self.bus = ACPBus()
        self.name = "OpenCode"
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _safe_path(self, path: str) -> str:
        full_path = os.path.abspath(os.path.join(self.workspace_dir, path))
        if not full_path.startswith(self.workspace_dir):
            raise PermissionError("Access denied: path outside workspace.")
        return full_path

    def handle_message(self, message: ACPMessage):
        topic = message.topic
        payload = message.payload
        try:
            if topic == "file_read":
                path = self._safe_path(payload["path"])
                with open(path, "r") as f:
                    content = f.read()
                self.bus.send(ACPMessage(self.name, message.sender, "file_read_res", {"content": content, "status": "success"}))

            elif topic == "file_write":
                path = self._safe_path(payload["path"])
                with open(path, "w") as f:
                    f.write(payload["content"])
                self.bus.send(ACPMessage(self.name, message.sender, "file_write_res", {"status": "success"}))

            elif topic == "file_list":
                path = self._safe_path(payload.get("path", "."))
                files = os.listdir(path)
                self.bus.send(ACPMessage(self.name, message.sender, "file_list_res", {"files": files, "status": "success"}))

        except Exception as e:
            self.bus.send(ACPMessage(self.name, message.sender, f"{topic}_res", {"status": "error", "message": str(e)}))

    def run_once(self):
        messages = self.bus.receive(self.name)
        for msg in messages:
            self.handle_message(msg)

if __name__ == "__main__":
    agent = OpenCodeAgent()
    print("OpenCode Agent started...")
    while True:
        agent.run_once()
        import time
        time.sleep(1)

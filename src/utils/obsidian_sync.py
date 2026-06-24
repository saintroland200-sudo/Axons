import os
import shutil
import time
import json
from typing import Optional

class ObsidianSync:
    def __init__(self, memory_warm_path: str = "memory/warm/data.json", obsidian_vault_dir: str = "obsidian_vault"):
        self.memory_path = memory_warm_path
        self.vault_dir = obsidian_vault_dir
        if not os.path.exists(self.vault_dir):
            os.makedirs(self.vault_dir)

    def sync_to_obsidian(self):
        """Sync Warm Memory JSON to individual Markdown files in Obsidian Vault."""
        if not os.path.exists(self.memory_path):
            return

        with open(self.memory_path, "r") as f:
            data = json.load(f)

        for key, value in data.items():
            file_path = os.path.join(self.vault_dir, f"{key}.md")
            content = f"# {key}\n\nLast Synced: {time.ctime()}\n\n"
            if isinstance(value, dict):
                content += json.dumps(value, indent=4)
            else:
                content += str(value)

            with open(file_path, "w") as f:
                f.write(content)

    def sync_from_obsidian(self):
        """Minimal sync back: read .md files and update warm memory if possible."""
        # In a real system, we'd parse the markdown. For the clone, we'll just track files.
        for filename in os.listdir(self.vault_dir):
            if filename.endswith(".md"):
                key = filename[:-3]
                # If we were doing full bi-directional, we'd update warm memory here.
                pass

if __name__ == "__main__":
    sync = ObsidianSync()
    sync.sync_to_obsidian()
    print("Obsidian sync complete.")

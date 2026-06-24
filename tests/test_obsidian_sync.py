import unittest
import os
import json
import shutil
from src.utils.obsidian_sync import ObsidianSync

class TestObsidianSync(unittest.TestCase):
    def setUp(self):
        self.temp_dir = "test_obsidian_root"
        self.vault = os.path.join(self.temp_dir, "vault")
        self.memory_file = os.path.join(self.temp_dir, "warm.json")
        os.makedirs(self.vault, exist_ok=True)

        with open(self.memory_file, "w") as f:
            json.dump({"note1": "Hello", "note2": {"data": 123}}, f)

        self.sync = ObsidianSync(self.memory_file, self.vault)

    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_sync_to_obsidian(self):
        self.sync.sync_to_obsidian()
        self.assertTrue(os.path.exists(os.path.join(self.vault, "note1.md")))
        self.assertTrue(os.path.exists(os.path.join(self.vault, "note2.md")))

        with open(os.path.join(self.vault, "note1.md"), "r") as f:
            content = f.read()
            self.assertIn("Hello", content)

if __name__ == "__main__":
    unittest.main()

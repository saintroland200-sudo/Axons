import unittest
import os
import shutil
from src.memory.system import MemorySystem

class TestMemorySystem(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_memory_root"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        self.mem = MemorySystem(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_hot_memory(self):
        self.mem.set_hot("key", "value")
        self.assertEqual(self.mem.get_hot("key"), "value")

    def test_warm_memory_persistence(self):
        self.mem.set_warm("user", "jules")
        # New instance should load it
        mem2 = MemorySystem(self.test_dir)
        self.assertEqual(mem2.get_warm("user"), "jules")

    def test_crystallized_memory(self):
        self.mem.add_relation("Alice", "Bob", "knows")
        relations = self.mem.query_graph("Alice")
        self.assertEqual(len(relations), 1)
        self.assertEqual(relations[0]["target"], "Bob")
        self.assertEqual(relations[0]["relation"], "knows")

if __name__ == "__main__":
    unittest.main()

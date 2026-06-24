import unittest
from src.utils.token_opt import TokenOptimizer

class TestTokenOptimizer(unittest.TestCase):
    def setUp(self):
        self.opt = TokenOptimizer()
        self.text = "This is a long sentence about LAIS. LAIS is an integration system. It has many agents. Each agent does something unique. Integration is important."

    def test_extractive(self):
        compressed = self.opt.compress_extractive(self.text, ratio=0.4)
        self.assertTrue(len(compressed) < len(self.text))

    def test_keywords(self):
        keywords = self.opt.extract_keywords(self.text)
        self.assertIn("lais", [k.lower() for k in keywords])

    def test_semantic_dedup(self):
        dup_text = "Hello world. Hello world. Goodbye."
        compressed = self.opt.compress_semantic(dup_text)
        self.assertEqual(compressed, "Hello world. Goodbye.")

if __name__ == "__main__":
    unittest.main()

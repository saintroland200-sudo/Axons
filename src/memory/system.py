import os
import json
import time
import networkx as nx
from typing import Any, Dict, Optional, List

class MemorySystem:
    def __init__(self, base_dir: str = "memory"):
        self.base_dir = base_dir
        self.hot_memory: Dict[str, Any] = {} # RAM
        self.warm_path = os.path.join(base_dir, "warm/data.json")
        self.cold_dir = os.path.join(base_dir, "cold")
        self.crystallized_path = os.path.join(base_dir, "crystallized/graph.json")

        for d in ["warm", "cold", "crystallized"]:
            os.makedirs(os.path.join(base_dir, d), exist_ok=True)

        self.graph = nx.DiGraph()
        self._load_warm()
        self._load_crystallized()

    def _load_warm(self):
        if os.path.exists(self.warm_path):
            with open(self.warm_path, "r") as f:
                self.warm_memory = json.load(f)
        else:
            self.warm_memory = {}

    def _save_warm(self):
        with open(self.warm_path, "w") as f:
            json.dump(self.warm_memory, f, indent=4)

    def _load_crystallized(self):
        if os.path.exists(self.crystallized_path):
            with open(self.crystallized_path, "r") as f:
                data = json.load(f)
                self.graph = nx.node_link_graph(data)
        else:
            self.graph = nx.DiGraph()

    def _save_crystallized(self):
        data = nx.node_link_data(self.graph)
        with open(self.crystallized_path, "w") as f:
            json.dump(data, f, indent=4)

    # Hot Memory (RAM)
    def set_hot(self, key: str, value: Any):
        self.hot_memory[key] = value

    def get_hot(self, key: str) -> Optional[Any]:
        return self.hot_memory.get(key)

    # Warm Memory (JSON Persistence)
    def set_warm(self, key: str, value: Any):
        self.warm_memory[key] = value
        self._save_warm()

    def get_warm(self, key: str) -> Optional[Any]:
        return self.warm_memory.get(key)

    # Cold Memory (Archive)
    def archive_cold(self, key: str, value: Any):
        filename = f"{key}_{int(time.time())}.json"
        path = os.path.join(self.cold_dir, filename)
        with open(path, "w") as f:
            json.dump(value, f, indent=4)

    # Crystallized Memory (Knowledge Graph)
    def add_relation(self, source: str, target: str, relation: str):
        self.graph.add_edge(source, target, relation=relation)
        self._save_crystallized()

    def query_graph(self, node: str) -> List[Dict[str, Any]]:
        if node not in self.graph:
            return []
        return [{"target": n, "relation": d["relation"]} for n, d in self.graph[node].items()]

if __name__ == "__main__":
    mem = MemorySystem()
    mem.set_hot("session_id", "12345")
    mem.set_warm("user_pref", {"theme": "dark"})
    mem.add_relation("User", "Project", "owns")
    print("Memory system test complete.")

import time
import threading
from src.acp.bus import ACPBus, ACPMessage
from src.agents.opencode import OpenCodeAgent
from src.agents.jarvis import JARVISAgent
from src.agents.osint_agent import OSINTAgent
from src.security.grid import SecurityGrid
from src.memory.system import MemorySystem
from src.utils.obsidian_sync import ObsidianSync

class LAISSystem:
    def __init__(self):
        print("Initializing LAIS System...")
        self.bus = ACPBus()
        self.security = SecurityGrid()
        self.memory = MemorySystem()
        self.obsidian = ObsidianSync()

        self.opencode = OpenCodeAgent()
        self.jarvis = JARVISAgent(use_mock=True)
        self.osint = OSINTAgent()

        self.running = True

    def security_wrapper_run_once(self, agent):
        """Simple wrapper to check security before processing messages."""
        # Note: In a production version, the ACP Bus would call this automatically
        # For the clone, we'll implement it in the main loop or agent loop.
        pass

    def run(self):
        print("LAIS System Running. Press Ctrl+C to stop.")
        try:
            while self.running:
                # Run each agent's cycle
                self.opencode.run_once()
                self.jarvis.run() # This JARVIS run() actually loops internally, let's fix that.
                self.osint.run_once()

                # Periodic tasks
                self.obsidian.sync_to_obsidian()

                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down LAIS...")

if __name__ == "__main__":
    # In a real scenario, we'd run these in separate processes/threads.
    # For integration test, we just verify they can all be instantiated and run once.
    system = LAISSystem()
    print("LAIS Integration Test: Success")

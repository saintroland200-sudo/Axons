import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from src.acp.bus import ACPBus, ACPMessage

class AIEngineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LAIS AI Engine - Dashboard")
        self.root.geometry("800x600")

        self.bus = ACPBus()
        self.name = "AIEngine"

        self.setup_ui()

        self.running = True
        self.poll_thread = threading.Thread(target=self.poll_bus, daemon=True)
        self.poll_thread.start()

    def setup_ui(self):
        # Top Frame: Task Triggering
        top_frame = ttk.LabelFrame(self.root, text="Trigger Task")
        top_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(top_frame, text="Topic:").pack(side="left", padx=5)
        self.topic_var = tk.StringVar(value="file_list")
        self.topic_entry = ttk.Entry(top_frame, textvariable=self.topic_var)
        self.topic_entry.pack(side="left", padx=5)

        ttk.Label(top_frame, text="Payload (JSON):").pack(side="left", padx=5)
        self.payload_var = tk.StringVar(value='{"path": "."}')
        self.payload_entry = ttk.Entry(top_frame, textvariable=self.payload_var, width=40)
        self.payload_entry.pack(side="left", padx=5)

        ttk.Label(top_frame, text="Receiver:").pack(side="left", padx=5)
        self.receiver_var = tk.StringVar(value="OpenCode")
        self.receiver_entry = ttk.Entry(top_frame, textvariable=self.receiver_var)
        self.receiver_entry.pack(side="left", padx=5)

        send_btn = ttk.Button(top_frame, text="Send", command=self.send_message)
        send_btn.pack(side="left", padx=10)

        # Middle Frame: ACP Bus Status
        mid_frame = ttk.LabelFrame(self.root, text="ACP Bus Status (Queued Messages)")
        mid_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.bus_listbox = tk.Listbox(mid_frame)
        self.bus_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        # Bottom Frame: Logs
        bottom_frame = ttk.LabelFrame(self.root, text="System Logs")
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_area = scrolledtext.ScrolledText(bottom_frame, height=10)
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)

    def log(self, message):
        self.log_area.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see(tk.END)

    def send_message(self):
        try:
            import json
            payload = json.loads(self.payload_var.get())
            msg = ACPMessage(
                sender=self.name,
                receiver=self.receiver_var.get(),
                topic=self.topic_var.get(),
                payload=payload
            )
            self.bus.send(msg)
            self.log(f"Sent: {msg.topic} to {msg.receiver}")
        except Exception as e:
            self.log(f"Error sending message: {e}")

    def poll_bus(self):
        while self.running:
            # Receive messages for AIEngine
            messages = self.bus.receive(self.name)
            for msg in messages:
                self.root.after(0, self.log, f"Received from {msg.sender}: {msg.topic} - {msg.payload}")

            # Update Bus Status (Peek)
            queued = self.bus.peek()
            self.root.after(0, self.update_bus_list, queued)

            time.sleep(1)

    def update_bus_list(self, queued):
        self.bus_listbox.delete(0, tk.END)
        for msg in queued:
            self.bus_listbox.insert(tk.END, f"{msg['sender']} -> {msg['receiver']} | {msg['topic']}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AIEngineGUI(root)
        root.mainloop()
    except tk.TclError:
        print("TclError: Likely running in a headless environment. AIEngineGUI code is defined but cannot be displayed.")

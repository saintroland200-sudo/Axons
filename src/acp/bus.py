import json
import os
import time
import uuid
import portalocker
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional, List

@dataclass
class ACPMessage:
    sender: str
    receiver: str
    topic: str
    payload: Dict[str, Any]
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)

    def to_json(self):
        return json.dumps(asdict(self))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

class ACPBus:
    def __init__(self, queue_file: str = "acp_queue.json"):
        self.queue_file = queue_file
        if not os.path.exists(self.queue_file):
            with open(self.queue_file, "w") as f:
                json.dump([], f)

    def send(self, message: ACPMessage):
        with portalocker.Lock(self.queue_file, "r+", timeout=10) as f:
            data = json.load(f)
            data.append(asdict(message))
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def receive(self, agent_name: str) -> List[ACPMessage]:
        messages = []
        with portalocker.Lock(self.queue_file, "r+", timeout=10) as f:
            data = json.load(f)
            remaining = []
            for msg_dict in data:
                if msg_dict["receiver"] == agent_name or msg_dict["receiver"] == "broadcast":
                    messages.append(ACPMessage.from_dict(msg_dict))
                else:
                    remaining.append(msg_dict)

            f.seek(0)
            json.dump(remaining, f, indent=4)
            f.truncate()
        return messages

    def peek(self) -> List[Dict[str, Any]]:
        """Non-destructive peek for status display."""
        with portalocker.Lock(self.queue_file, "r", timeout=10) as f:
            return json.load(f)

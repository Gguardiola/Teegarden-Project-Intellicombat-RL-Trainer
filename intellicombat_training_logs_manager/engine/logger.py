import json
import os
import time 
import random

class CombatLogger:
    def __init__(self, log_dir="logs", filename=None):
        os.makedirs(log_dir, exist_ok=True)
        if filename is None:
            filename = f"combat_log_{int(time.time() * 1000)}_{random.randint(1000, 9999)}.jsonl"
        self.file_path = os.path.join(log_dir, filename)
        self.file = open(self.file_path, "a")

    def log(self, state, action, reward, next_state):
        entry = {
            "state": state,
            "action": action,
            "reward": reward,
            "next_state": next_state
        }
        self.file.write(json.dumps(entry) + "\n")

    def close(self):
        if not self.file.closed:
            self.file.close()

    def __del__(self):
        self.close()

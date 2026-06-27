import json
import os
import threading

DB_PATH = "data/dion.json"

class JSONDatabase:
    def __init__(self, path):
        self.path = path
        self.lock = threading.Lock()
        self.data = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            default_data = {
                "events": [],
                "event_rsvps": [],
                "temp_voice_config": {},
                "active_temp_channels": {},
                "warnings": [],
                "command_usage": {},
                "user_last_active": {}
            }
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=4)
            return default_data
        
        with open(self.path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def save(self):
        with self.lock:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)

# Global database instance
db = JSONDatabase(DB_PATH)

def get_db():
    return db

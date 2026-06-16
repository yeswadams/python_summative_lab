import os
import json
from typing import Dict
from src.models import User

class StorageManager:
    def __init__(self, filepath: str = "data/storage.json"):
        self.filepath = filepath
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

    def load_data(self) -> Dict[str, User]:
        """Loads data from JSON and reconstructs User, Project, and Task objects."""
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, "r") as f:
                raw_data = json.load(f)
                return {name: User.from_dict(u_data) for name, u_data in raw_data.items()}
        except (json.JSONDecodeError, IOError) as e:
            print(f"[Warning] Error loading database file ({e}). Starting fresh.")
            return {}

    def save_data(self, users: Dict[str, User]):
        """Serializes current memory state back down to JSON safely."""
        try:
            with open(self.filepath, "w") as f:
                serialized = {name: user.to_dict() for name, user in users.items()}
                json.dump(serialized, f, indent=4)
        except IOError as e:
            print(f"[Error] Failed to save data to disk: {e}")
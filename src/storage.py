import os
import json
import logging
from typing import Dict
from src.models import User

logger = logging.getLogger("PM-CLI.storage")

class Storage:
    def __init__(self, filepath: str = "data/storage.json"):
        self.filepath = filepath
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Ensures the directory for the storage file exists."""
        try:
            directory = os.path.dirname(self.filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
        except PermissionError as e:
            logger.error(f"Permission denied while creating directory: {e}")
            raise

    def load_data(self) -> Dict[str, User]:
        """Loads data from JSON and reconstructs User objects."""
        if not os.path.exists(self.filepath):
            logger.info("Storage file not found. Starting with empty database.")
            return {}

        try:
            with open(self.filepath, "r") as f:
                raw_data = json.load(f)
                return {name: User.from_dict(u_data) for name, u_data in raw_data.items()}
        except json.JSONDecodeError as e:
            logger.warning(f"Storage file corrupted ({e}). Falling back to empty state.")
            return {}
        except PermissionError as e:
            logger.error(f"Permission denied while reading storage file: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error while loading data: {e}")
            return {}
        finally:
            logger.debug("Load operation attempted.")

    def save_data(self, users: Dict[str, User]):
        """Serializes current state to JSON safely."""
        try:
            with open(self.filepath, "w") as f:
                serialized = {name: user.to_dict() for name, user in users.items()}
                json.dump(serialized, f, indent=4)
            logger.info("Data saved successfully.")
        except PermissionError as e:
            logger.error(f"Permission denied while saving data: {e}")
        except IOError as e:
            logger.error(f"IO Error while saving data: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while saving data: {e}")
        finally:
            logger.debug("Save operation attempted.")

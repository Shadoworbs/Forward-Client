import os
import json
from typing import List, Dict, Optional


class UserSettings:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.base_dir = os.path.join("user_data", str(user_id))
        self.settings_file = os.path.join(self.base_dir, "settings.json")
        self._ensure_dirs()
        self._load_settings()

    def _ensure_dirs(self):
        """Ensure the user directory exists"""
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)

    def _load_settings(self):
        """Load settings from JSON file"""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                self.settings = json.load(f)
        else:
            self.settings = {"forward_from": [], "forward_to": []}
            self._save_settings()

    def _save_settings(self):
        """Save settings to JSON file"""
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get_forward_from(self) -> List[int]:
        """Get list of chat IDs to forward from"""
        return self.settings.get("forward_from", [])

    def get_forward_to(self) -> List[int]:
        """Get list of chat IDs to forward to"""
        return self.settings.get("forward_to", [])

    def add_forward_from(self, chat_id: int) -> bool:
        """Add a chat ID to forward from"""
        if chat_id not in self.settings["forward_from"]:
            self.settings["forward_from"].append(chat_id)
            self._save_settings()
            return True
        return False

    def add_forward_to(self, chat_id: int) -> bool:
        """Add a chat ID to forward to"""
        if chat_id not in self.settings["forward_to"]:
            self.settings["forward_to"].append(chat_id)
            self._save_settings()
            return True
        return False

    def remove_forward_from(self, chat_id: int) -> bool:
        """Remove a chat ID from forward from"""
        if chat_id in self.settings["forward_from"]:
            self.settings["forward_from"].remove(chat_id)
            self._save_settings()
            return True
        return False

    def remove_forward_to(self, chat_id: int) -> bool:
        """Remove a chat ID from forward to"""
        if chat_id in self.settings["forward_to"]:
            self.settings["forward_to"].remove(chat_id)
            self._save_settings()
            return True
        return False

    def clear_forward_from(self):
        """Clear all forward from chat IDs"""
        self.settings["forward_from"] = []
        self._save_settings()

    def clear_forward_to(self):
        """Clear all forward to chat IDs"""
        self.settings["forward_to"] = []
        self._save_settings()

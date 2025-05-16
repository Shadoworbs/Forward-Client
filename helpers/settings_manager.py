# (c) @Shadoworbs

import os
import json
import time
from typing import List, Dict, Optional, Union, Tuple
from dataclasses import dataclass


@dataclass
class ValidationResult:
    is_valid: bool
    cleaned_id: Optional[int]
    error_message: Optional[str]


class UserSettings:
    MAX_CHATS = 5  # Maximum number of chats allowed for each direction
    SETTINGS_VERSION = 1  # For future migrations if needed

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.base_dir = os.path.join("user_data", str(user_id))
        self.settings_file = os.path.join(self.base_dir, "settings.json")
        self._ensure_dirs()
        self._load_settings()
        self.last_modified = time.time()

    def _ensure_dirs(self):
        """Ensure the user directory exists"""
        os.makedirs(self.base_dir, exist_ok=True)

    def _load_settings(self):
        """Load settings from JSON file with versioning support"""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                data = json.load(f)
                self.settings = {
                    "version": self.SETTINGS_VERSION,
                    "forward_from": data.get("forward_from", []),
                    "forward_to": data.get("forward_to", []),
                    "last_modified": time.time(),
                }
        else:
            self.settings = {
                "version": self.SETTINGS_VERSION,
                "forward_from": [],
                "forward_to": [],
                "last_modified": time.time(),
            }
            self._save_settings()

    def _save_settings(self):
        """Save settings to JSON file with atomic write"""
        temp_file = f"{self.settings_file}.tmp"
        with open(temp_file, "w") as f:
            json.dump(self.settings, f, indent=4)
        os.replace(temp_file, self.settings_file)
        self.last_modified = time.time()

    @staticmethod
    def validate_chat_id(chat_id: str) -> ValidationResult:
        """Validate chat ID format with detailed error messages"""
        if not chat_id:
            return ValidationResult(False, None, "Chat ID cannot be empty")

        if chat_id.strip().lower() == "cancel":
            return ValidationResult(False, None, "Operation cancelled")

        try:
            # Remove any whitespace and optional -100 prefix
            cleaned_id = chat_id.strip()
            # if cleaned_id.startswith("-100"):
            #     cleaned_id = cleaned_id[4:]

            # Convert to int and validate
            chat_id_int = int(cleaned_id)

            # Basic validation rules
            if chat_id_int == 0:
                return ValidationResult(False, None, "Invalid chat ID: cannot be 0")
            if len(str(abs(chat_id_int))) < 6:
                return ValidationResult(False, None, "Invalid chat ID: too short")
            if len(str(abs(chat_id_int))) > 15:
                return ValidationResult(False, None, "Invalid chat ID: too long")

            return ValidationResult(True, chat_id_int, None)
        except ValueError:
            return ValidationResult(False, None, "Invalid chat ID: must be a number")

    def _validate_chat_list(self, chat_list: List[int]) -> bool:
        """Validate the entire chat list"""
        return len(chat_list) <= self.MAX_CHATS

    def add_forward_from(self, chat_id: int) -> Tuple[bool, str]:
        """Add a chat ID to forward from with validation"""
        if not self._validate_chat_list(self.settings["forward_from"]):
            return False, f"Maximum of {self.MAX_CHATS} source chats allowed"

        if chat_id in self.settings["forward_from"]:
            return False, "This chat is already in the source list"

        self.settings["forward_from"].append(chat_id)
        self._save_settings()
        return True, "Successfully added to source chats"

    def add_forward_to(self, chat_id: int) -> Tuple[bool, str]:
        """Add a chat ID to forward to with validation"""
        if not self._validate_chat_list(self.settings["forward_to"]):
            return False, f"Maximum of {self.MAX_CHATS} destination chats allowed"

        if chat_id in self.settings["forward_to"]:
            return False, "This chat is already in the destination list"

        self.settings["forward_to"].append(chat_id)
        self._save_settings()
        return True, "Successfully added to destination chats"

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

    def has_required_settings(self) -> bool:
        """Check if the required settings are configured"""
        return len(self.get_forward_from()) > 0 and len(self.get_forward_to()) > 0

    def get_forward_from(self) -> List[int]:
        """Get list of chat IDs to forward from"""
        return self.settings.get("forward_from", [])

    def get_forward_to(self) -> List[int]:
        """Get list of chat IDs to forward to"""
        return self.settings.get("forward_to", [])

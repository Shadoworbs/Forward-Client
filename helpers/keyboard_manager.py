from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List


class KeyboardManager:
    @staticmethod
    def settings_menu() -> InlineKeyboardMarkup:
        """Main settings menu keyboard"""
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📥 Forward From", callback_data="forward_from_menu"
                    ),
                    InlineKeyboardButton(
                        "📤 Forward To", callback_data="forward_to_menu"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🔄 Current Settings", callback_data="show_settings"
                    )
                ],
            ]
        )

    @staticmethod
    def forward_from_menu() -> InlineKeyboardMarkup:
        """Forward from management keyboard"""
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Add Channel", callback_data="add_forward_from"
                    ),
                    InlineKeyboardButton(
                        "➖ Remove Channel", callback_data="remove_forward_from"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🗑️ Clear All", callback_data="clear_forward_from"
                    ),
                    InlineKeyboardButton(
                        "📋 List All", callback_data="list_forward_from"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🔙 Back to Settings", callback_data="back_to_settings"
                    )
                ],
            ]
        )

    @staticmethod
    def forward_to_menu() -> InlineKeyboardMarkup:
        """Forward to management keyboard"""
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Add Channel", callback_data="add_forward_to"
                    ),
                    InlineKeyboardButton(
                        "➖ Remove Channel", callback_data="remove_forward_to"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🗑️ Clear All", callback_data="clear_forward_to"
                    ),
                    InlineKeyboardButton(
                        "📋 List All", callback_data="list_forward_to"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🔙 Back to Settings", callback_data="back_to_settings"
                    )
                ],
            ]
        )

    @staticmethod
    def confirmation_keyboard() -> InlineKeyboardMarkup:
        """Confirmation keyboard"""
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("✅ Confirm", callback_data="confirm"),
                    InlineKeyboardButton("❌ Cancel", callback_data="cancel"),
                ]
            ]
        )

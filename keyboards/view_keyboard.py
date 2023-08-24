from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Buttons for main view commands
start_help_button = KeyboardButton("start")
watched_button = KeyboardButton("watched")
active_button = KeyboardButton("active")
random_button = KeyboardButton("random")

kb_view = ReplyKeyboardMarkup(resize_keyboard=True)
kb_view.row(start_help_button, random_button).row(watched_button, active_button)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Buttons for main view commands
start_help_button = KeyboardButton(text="start")
watched_button = KeyboardButton(text="watched")
active_button = KeyboardButton(text="active")
random_button = KeyboardButton(text="random")


kb_view = ReplyKeyboardMarkup(
    keyboard=[
        [start_help_button, random_button],
        [watched_button, active_button],
    ],
    resize_keyboard=True
)

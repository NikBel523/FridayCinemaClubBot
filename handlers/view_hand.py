from aiogram import types, Dispatcher

from create_bot import dp
from data_base.sqlite_db import sql_show_suggestions, sql_fetch_random
from keyboards.view_keyboard import kb_view


list_of_keywords = """
a '+' sign followed by a film name to add a film to list
a '-' sign followed by a film name to set film status to "watched"
keywords "watched" or "active" in the message text displays a list of films that match the specified status
"""


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(f"Hi!\n Here the list of keywords, that you can use with me:\n {list_of_keywords}",
                        reply_markup=kb_view)


@dp.message_handler(lambda message: "watched" in message.text or "active" in message.text)
async def show_films(message: types.Message):
    """
    Displays a list of films based on their status.

    Depending on the presence of the keywords "watched" or "active" in the message text,
    this function retrieves and displays a list of films that match the specified status.

    :param message: The user's message containing keywords "watched" or "active".
    :return: None
    """
    if "watched" in message.text:
        await sql_show_suggestions(message, ("watched",))
    elif "active" in message.text:
        await sql_show_suggestions(message, ("active",))


@dp.message_handler(lambda message: "random" in message.text)
async def random_films(message: types.Message):
    """
    Handle messages containing requests for random films.

    This function is a message handler designed to respond to messages that contain the word "random."
    It fetches a specified number of random films from a database and sends the information as a response.

    :param message: The incoming message containing the user's request.
    :type message: types.Message

    :return: None
    """
    if len(message.text) == 6:
        num_films = 1
    else:
        num_films = int(message.text[7:])
    await sql_fetch_random(message, num_films)


@dp.message_handler()
async def show_info(message: types.Message):
    """
    Provides information about available commands.

    This function is triggered when no specific command matches the user's message.
    It responds by informing the user that there is no such command and then provides
    a list of active commands that the user can use.

    :param message: The user's message triggering the function.
    :return: None
    """
    # Inform the user about the absence of a matching command
    await message.answer("There is no such command or keyword.")

    # Provide a list of active commands
    await message.answer(f"Here is a list of active commands:\n {list_of_keywords}")


def register_view_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(show_films)
    dp.register_message_handler(random_films)
    dp.register_message_handler(show_info)

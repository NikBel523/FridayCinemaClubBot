from aiogram import types, Dispatcher

from create_bot import dp
from data_base.sqlite_db import sql_add_film, sql_change_status, sql_delete_film


@dp.message_handler(lambda message: "+" in message.text)
async def add_film(message: types.Message):
    """
    Adds a film to the database with the default status set to 'active'.

    This function handles messages that contain a '+' sign followed by a film name.
    The provided film name is extracted from the message text, and the film is then added
    to the database with its status set to 'active'.

    :param message: The message from the user, which includes the '+' sign and the film name.
    :return: None
    """
    # Extract the film name from the message text and set its status to 'active'
    film_name = message.text[2:]
    film = (film_name, "active")

    # Add the film to the database
    await sql_add_film(film)

    # Notify the user about the successful addition of the film
    await message.answer(f"Added '{film_name}' to the database.")


@dp.message_handler(lambda message: "-" in message.text)
async def check(message: types.Message):
    """
    Changes the status of a film to "watched".

    This function handles messages that contain a '-' sign followed by a film name.
    The provided film name is extracted from the message text, and the status of the
    corresponding film is changed to 'watched' in the database.

    :param message: The user's message containing the '-' sign and the film name.
    :return: None
    """
    # Extract the film name from the message text
    film_name = message.text[2:]

    # Change the status of the film to 'watched' in the database
    film = (film_name,)
    await sql_change_status(film)

    # Notify the user about the successful status change
    await message.answer(f"Status of '{film_name}' changed to 'watched'.")


@dp.message_handler(lambda message: "delete" in message.text)
async def delete_films(message: types.Message):
    """
    Deletes a film from the database.

    This function handles messages that contain the keyword "delete" followed by a film name.
    The provided film name is extracted from the message text, and the corresponding film is
    deleted from the database.

    :param message: The user's message containing the "delete" keyword and the film name.
    :return: None
    """
    # Extract the film name from the message text
    film_name = message.text[7:]

    # Delete the film from the database
    film = (film_name,)
    await sql_delete_film(film)

    # Notify the user about the successful deletion
    await message.answer(f"Film '{film_name}' deleted.")


def register_manage_handlers(dp: Dispatcher):
    dp.register_message_handler(add_film)
    dp.register_message_handler(check)
    dp.register_message_handler(delete_films)

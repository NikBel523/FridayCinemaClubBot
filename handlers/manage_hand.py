from aiogram import types, Dispatcher

from create_bot import dp
from data_base.sqlite_db import sql_add_film, sql_change_status, sql_delete_film


@dp.message_handler(lambda message: "+++" in message.text)
async def add_films(message: types.Message):
    """
    Adds several films to the database with the default status set to 'active'.

    This function handles messages that contain a '+++' sign followed by a film name separate by a '\n'.
    The provided films names are extracted from the message text, and films is then added
    to the database with their status set to 'active'.

    :param message: The message from the user, which includes the '+++' sign and several films names.
    :return: None
    """
    # Extract the list films names from the message text
    films_list = message.text.split("\n")
    # Extract the films names from the message text and set its status to 'active'
    for i in range(1, len(films_list)):
        result = await sql_add_film(films_list[i])
        # Add the film to the database
        await message.answer(result)


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
    result = await sql_add_film(film_name)
    # Add the film to the database
    await message.answer(result)


@dp.message_handler(lambda message: "---" in message.text or "—-" in message.text)
async def check_films(message: types.Message):
    """
    Changes the status of several films to "watched".

    This function handles messages that contain a '---' or '—-' signs
    followed by several names of films separated by a '\n'.
    The provided films names are extracted from the message text, and the status of the
    corresponding films is changed to 'watched' in the database.

    :param message: The user's message containing the '---' or '—-' signs and several names of films.
    :return: None
    """
    # Extract all names from the message text to a list
    films_list = message.text.split("\n")
    # Change the status of each film to 'watched' in the database and notify the user about the successful status change
    for i in range(1, len(films_list)):
        film = films_list[i]
        result = await sql_change_status(film)
        await message.answer(result)


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
    result = await sql_change_status(film_name)
    # Change the status of the film to 'watched' in the database and notify the user about the successful status change
    await message.answer(result)


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

    result = await sql_delete_film(film_name)
    # Delete the film from the database and notify the user about the successful deletion
    await message.answer(result)


def register_manage_handlers(dp: Dispatcher):
    dp.register_message_handler(add_films)
    dp.register_message_handler(add_film)
    dp.register_message_handler(check_films)
    dp.register_message_handler(check)
    dp.register_message_handler(delete_films)

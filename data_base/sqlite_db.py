import random
import sqlite3 as sq

from create_bot import bot


def sql_start():
    """
    Establishes a connection to the database and creates the films table if it doesn't exist.

    This function initializes a connection to the SQLite database named "friday_films.db".
    It creates a cursor for database operations and checks the connection status.
    The films table is created if it doesn't already exist, with columns 'film' and 'status'.

    :return: None
    """
    global base, cur
    base = sq.connect("friday_films.db")
    cur = base.cursor()
    if base:
        print("Database connection established.")
    base.execute("CREATE TABLE IF NOT EXISTS films(film TEXT, status TEXT)")
    base.commit()


async def sql_add_film(film: str):
    """
    Adds a film to the films table in the database.

    This asynchronous function inserts a new film entry into the films table
    with the provided film name and status. It then commits the changes to the database.

    :param film: A string containing the film name and its status.
    :return: None
    """
    cur.execute("INSERT INTO films VALUES (?, 'active')", (film,))
    base.commit()


async def sql_change_status(film: str):
    """
    Changes the status of a film to 'watched' in the films table.

    This asynchronous function updates the status of a film in the films table
    to 'watched' based on the provided film name. It then commits the changes to the database.

    :param film: A string containing the film name.
    :return: None
    """
    cur.execute("UPDATE films SET status = 'watched' WHERE film = ?", (film,))
    base.commit()


async def sql_show_suggestions(message, status):
    """
    Retrieves and sends film suggestions based on the provided status.

    This asynchronous function queries the films table for films with the specified status.
    It sends film suggestions to the user's ID using the provided message object.

    :param message: The user's message triggering the function.
    :type message: types.Message
    :param status: The desired status of films to retrieve.
    :type status: str
    :return: None
    """
    for film in cur.execute("SELECT film FROM films WHERE status = ?", (status,)):
        await bot.send_message(message.from_user.id, text=film[0])


async def sql_delete_film(film: str):
    """
    Deletes a film from the films table in the database.

    This asynchronous function removes a film entry from the films table based on the provided film name.
    It then commits the changes to the database.

    :param film: A str containing the film name.
    :return: None
    """
    cur.execute("DELETE FROM films WHERE film == ?", (film,))
    base.commit()


async def sql_fetch_random(message, num_films):
    """
    Fetches a specified number of random active films from a database and sends them as messages.

    This asynchronous function queries the database for active films, randomly selects the specified
    number of films, and sends them as messages to the user.

    :param message: The message object to determine the user to send films to.
    :type message: types.Message

    :param num_films: The number of random films to fetch and send.
    :type num_films: int

    :return: None
    """
    list_of_active_films = list(cur.execute("SELECT film FROM films WHERE status = 'active'"))
    print(list_of_active_films)
    random_list = random.choices(list_of_active_films, k=num_films)
    for film in random_list:
        await bot.send_message(message.from_user.id, text=film[0])

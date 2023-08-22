from aiogram import types, Dispatcher

from create_bot import dp, bot
from data_base.sqlite_db import sql_add_film, sql_change_status, sql_show_suggestions, sql_delete_film


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm soon became a FridayCinemaClubBot! Unfortunately, I'm not it now.")


@dp.message_handler(lambda message: "+" in message.text)
async def add_film(message: types.Message):
    film = (message.text[2:], "active")
    await sql_add_film(film)
    await message.answer(f"add {message.text[2:]} to db")


@dp.message_handler(lambda message: "-" in message.text)
async def check(message: types.Message):
    film = (message.text[2:],)
    await sql_change_status(film)
    await message.answer(f"status {message.text} changed to watched")


@dp.message_handler(lambda message: "watched" or "active" in message.text)
async def show_films(message: types.Message):
    if "watched" in message.text:
        await sql_show_suggestions(message, ("watched",))
    else:
        await sql_show_suggestions(message, ("active",))


@dp.message_handler(lambda message: "delete" in message.text)
async def delete_films(message: types.Message):
    film = (message.text[7:],)
    await sql_delete_film(film)
    await message.answer(f"Film {film} deleted")


@dp.message_handler()
async def show_info(message: types.Message):
    await message.answer("There is no such command.")
    await message.answer("Here is a list of active commands:")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(add_film)
    dp.register_message_handler(check)
    dp.register_message_handler(show_films)
    dp.register_message_handler(show_info)
from aiogram import types, Dispatcher

from create_bot import dp, bot
from data_base.sqlite_db import sql_add_film


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm soon became a FridayCinemaClubBot! Unfortunately, I'm not it now.")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])

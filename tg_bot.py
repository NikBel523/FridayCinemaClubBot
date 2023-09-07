import os

from aiogram.utils import executor
from create_bot import dp, bot
from data_base import sqlite_db
from handlers import manage_hand, view_hand

import config

URL_APP = os.environ.get("URL_CINEMA_APP")


async def on_startup(_):
    print("Bot online")
    sqlite_db.sql_start()


async def on_startup_webhook(_):
    print("Bot online")
    sqlite_db.sql_start()
    await bot.set_webhook(URL_APP)


async def on_shutdown(dp):
    await bot.delete_webhook()


manage_hand.register_manage_handlers(dp=dp)
view_hand.register_view_handlers(dp=dp)


if __name__ == "__main__":
    if config.START_UP == "polling":
        print(f"working with {config.START_UP}")
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    else:
        print(f"working with {config.START_UP}")
        executor.start_webhook(
            dispatcher=dp,
            webhook_path="",
            on_startup=on_startup_webhook,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 5000))
        )

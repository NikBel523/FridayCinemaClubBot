import logging
import sys
from aiogram import Bot, Dispatcher, Router
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

import config
from create_bot import bot, router
from data_base import sqlite_db
from handlers import manage_hand, view_hand


async def on_startup(bot: Bot):
    print("Bot online")
    sqlite_db.sql_start()
    await bot.set_webhook(f"{config.BASE_WEBHOOK_URL}{config.WEBHOOK_PATH}")


async def on_shutdown(bot: Bot):
    await bot.delete_webhook()


def main(bot: Bot, router: Router) -> None:

    dp = Dispatcher()
    dp.include_router(router)

    dp.startup.register(on_startup)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    # Register webhook handler on application
    webhook_requests_handler.register(app, path=config.WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    # And finally start webserver
    web.run_app(app, host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main(bot, router)

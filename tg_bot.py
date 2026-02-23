import logging
import ssl
import sys
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

import config
from create_bot import bot, router
from data_base import sqlite_db
from handlers import view_hand, manage_hand

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    logger.info("Bot starting in %s mode.", config.BOT_MODE.upper())

    sqlite_db.sql_start()

    if config.BOT_MODE == "webhook":
        webhook_url = f"{config.BASE_WEBHOOK_URL}:{config.WEB_SERVER_PORT}{config.WEBHOOK_PATH}"
        await bot.set_webhook(
            webhook_url,
            certificate=open(config.CERT_PATH, "rb") if config.CERT_PATH else None
        )
        logger.info("Webhook set to: %s", webhook_url)
    else:
        await bot.delete_webhook()
        logger.info("Webhook deleted, bot will use polling")


async def on_shutdown(bot: Bot):
    logger.info("Bot shutting down...")
    if config.BOT_MODE == "webhook":
        await bot.delete_webhook()
    await bot.session.close()


async def start_polling():
    dp = Dispatcher()
    dp.include_router(router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    logger.info("Starting polling...")
    await dp.start_polling(bot)


def start_webhook():
    dp = Dispatcher()
    dp.include_router(router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=config.WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(
        config.CERT_PATH,
        config.CERT_KEY
    )

    logger.info(f"Starting webhook on %s:%s", config.WEB_SERVER_HOST, config.WEB_SERVER_PORT)

    web.run_app(
        app,
        host=config.WEB_SERVER_HOST,
        port=config.WEB_SERVER_PORT,
        ssl_context=ssl_context
    )


async def main():
    if config.BOT_MODE == "webhook":
        start_webhook()
    else:
        await start_polling()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        stream=sys.stdout
    )

    try:
        if config.BOT_MODE == "webhook":
            main()
        else:
            asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nBot stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)

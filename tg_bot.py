import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application


from create_bot import bot, router
from data_base import sqlite_db
from handlers import manage_hand, view_hand

import config


# Test handlers
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@router.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


# async def on_startup(_):
#     print("Bot online")
#     sqlite_db.sql_start()


async def on_startup(bot: Bot):
    print("Bot online")
    sqlite_db.sql_start()
    await bot.set_webhook(f"{config.BASE_WEBHOOK_URL}{config.WEBHOOK_PATH}")


async def on_shutdown(bot: Bot):
    await bot.delete_webhook()


# manage_hand.register_manage_handlers(dp=dp)
# view_hand.register_view_handlers(dp=dp)


def main(bot: Bot) -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Register startup hook to initialize webhook
    dp.startup.register(on_startup)

    # bot = Bot(token=config.TG_TOKEN_API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Initialize Bot instance with default bot properties which will be passed to all API calls
    # bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Create aiohttp.web.Application instance
    app = web.Application()

    # Create an instance of request handler,
    # aiogram has few implementations for different cases of usage
    # In this example we use SimpleRequestHandler which is designed to handle simple cases
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        # secret_token=WEBHOOK_SECRET,
    )
    # Register webhook handler on application
    webhook_requests_handler.register(app, path=config.WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    # And finally start webserver
    web.run_app(app, host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main(bot)




# if __name__ == "__main__":
#     if config.START_UP == "polling":
#         print(f"working with {config.START_UP}")
#         executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
#     else:
#         print(f"working with {config.START_UP}")
#         executor.start_webhook(
#             dispatcher=dp,
#             webhook_path="",
#             on_startup=on_startup_webhook,
#             on_shutdown=on_shutdown,
#             skip_updates=True,
#             host="0.0.0.0",
#             port=int(os.environ.get("PORT", 5000))
#         )

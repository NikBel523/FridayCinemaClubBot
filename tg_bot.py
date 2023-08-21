from aiogram.utils import executor
from create_bot import dp

import handlers

async def on_startup(_):
    print("Bot online")


handlers.register_handlers(dp=dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

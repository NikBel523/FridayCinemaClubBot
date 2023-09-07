import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher


TG_TOKEN_API = os.environ.get("TG_TOKEN_API")

bot = Bot(token=TG_TOKEN_API)
dp = Dispatcher(bot)

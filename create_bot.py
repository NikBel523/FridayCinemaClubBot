from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from config import TG_TOKEN_API


bot = Bot(token=TG_TOKEN_API)
dp = Dispatcher(bot)

import os

from aiogram import Bot, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


TG_TOKEN_API = os.environ.get("TG_TOKEN_API")

bot = Bot(token=TG_TOKEN_API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

router = Router()

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot_admin.bot.data.config import token_api
from tgbot_admin.bot.app.middlewares.i18n import i18n

storage = MemoryStorage()
bot = Bot(token_api, parse_mode="html")
dp = Dispatcher(bot=bot, storage=storage)

_ = i18n.gettext
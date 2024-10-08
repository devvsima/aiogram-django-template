from aiogram import Dispatcher
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import Throttled

from tgbot_admin.bot.loader import _
from tgbot_admin.bot.data.config import RATE_LIMIT

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float = RATE_LIMIT, key_prefix: str = 'antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: Message, data: dict[str]):
        await self._throttle(message, data)

    async def on_process_callback_query(self, query: CallbackQuery, data: dict[str]):
        await self._throttle(query.message, data)

    async def _throttle(self, message: Message, data: dict[str]):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f'{self.prefix}_{handler.__name__}')
        else:
            limit = self.rate_limit
            key = f'{self.prefix}_message'
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as throttled:
            if throttled.exceeded_count <= 2:
                await message.reply(_('Too many requests!'))

            raise CancelHandler()
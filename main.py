import logging

from aiogram import Bot, Dispatcher

from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.config.config_reader import config

from telegram_bot.handlers.common import router
import asyncio
from telegram_bot.utils.commands import set_commands

# Установка спииска комманд


async def start_bot(bot: Bot):
    await set_commands(bot=bot)


async def main():


    bot = Bot(token=config.bot_token.get_secret_value(),
              parse_mode=ParseMode.HTML)
    #await bot.session.close()

    dp = Dispatcher(storage=MemoryStorage())
    dp.startup.register(start_bot)
    dp.include_router(router=router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    await bot.close()


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

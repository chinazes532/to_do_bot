import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from app.handlers.user_message import user
from app.handlers.stop_message import stop
from app.handlers.task_message import task
from app.handlers.find_message import find

from app.database import create_db


async def main():
    print("Bot is starting...")

    await create_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user)
    dp.include_router(task)
    dp.include_router(find)
    dp.include_router(stop)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
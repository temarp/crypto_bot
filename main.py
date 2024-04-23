import asyncio
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import Bot, Dispatcher

from commands import set_commands
from database.models import async_main
from database.requests import add_user, get_text
from routers.main_router import main_router
from routers.admin_router import admin_router
from config import TOKEN

bot = Bot(token=TOKEN, parse_mode='HTML')

dp = Dispatcher()


async def main():
    dp.include_router(main_router)
    dp.include_router(admin_router)
    await async_main()
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

async def on_startup(bot: Bot):
    await set_commands(bot)
    # await bot.set_my_description(description='Hello!\n\nTo get started, press START button at the bottom of the screen')

if __name__ == '__main__':
    asyncio.run(main())
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from configs import BOT_TOKEN
from db import create_tables


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "سلام 👋\n"
        "به ربات فروش کانفینگ خوش آمدید."
    )


@dp.message()
async def echo(message: Message):
    await message.answer(
        "لطفاً از منوی ربات استفاده کنید."
    )


async def main():
    create_tables()

    print("Bot is running...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

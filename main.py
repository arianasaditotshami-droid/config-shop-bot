import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = "8952198918:AAGuTIHUt49LzI97goCQf7Mesa0bBdOCWQM"

CARD_NUMBER = "6104337300101910"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id

    await message.answer(
        f"سلام 👋\n"
        f"آیدی عددی شما:\n{user_id}\n\n"
        f"برای خرید از این شماره کارت پرداخت کنید:\n"
        f"{CARD_NUMBER}"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

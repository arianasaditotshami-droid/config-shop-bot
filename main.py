import asyncio
from database import add_order, get_orders
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
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="خرید کانفیگ")],
        [KeyboardButton(text="سفارش‌های من")]
    ],
    resize_keyboard=True
)


@dp.message(lambda message: message.text == "خرید کانفیگ")
async def buy(message: Message):
    await message.answer(
        "حجم مورد نظر را انتخاب کنید:\n"
        "1- 3GB\n"
        "2- 5GB\n"
        "3- 10GB"
    )


@dp.message(lambda message: message.text in ["3GB", "5GB", "10GB"])
async def order(message: Message):
    add_order(
        message.from_user.id,
        message.text
    )

    await message.answer(
        "سفارش شما ثبت شد ✅"
    )


@dp.message(lambda message: message.text == "سفارش‌های من")
async def my_orders(message: Message):
    orders = get_orders(message.from_user.id)

    if not orders:
        await message.answer("سفارشی ندارید.")
        return

    text = "سفارش‌های شما:\n"

    for order in orders:
        text += f"- {order[0]}\n"

    await message.answer(text)

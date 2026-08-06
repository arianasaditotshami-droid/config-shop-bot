import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

from database import add_user, add_order, get_orders


TOKEN = "8952198918:AAHtAKqvPEy00TA92O5LxyjD0wW46FmnYaw"

CARD_NUMBER = "6104337300101910"


bot = Bot(token=TOKEN)
dp = Dispatcher()


menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 خرید کانفیگ")],
        [KeyboardButton(text="📦 سفارش‌های من")],
        [KeyboardButton(text="🎁 گیفت")]
    ],
    resize_keyboard=True
)


packages = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="3GB")],
        [KeyboardButton(text="5GB")],
        [KeyboardButton(text="10GB")],
        [KeyboardButton(text="15GB")],
        [KeyboardButton(text="20GB")]
    ],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start(message: Message):

    user_id = message.from_user.id
    username = message.from_user.username or "None"

    add_user(user_id, username)

    await message.answer(
        f"سلام 👋\n"
        f"آیدی عددی شما:\n{user_id}\n\n"
        f"شماره کارت پرداخت:\n{CARD_NUMBER}",
        reply_markup=menu
    )


@dp.message(lambda m: m.text == "🛒 خرید کانفیگ")
async def buy(message: Message):

    await message.answer(
        "حجم مورد نظر را انتخاب کنید:",
        reply_markup=packages
    )


@dp.message(lambda m: m.text in [
    "3GB",
    "5GB",
    "10GB",
    "15GB",
    "20GB"
])
async def select_package(message: Message):

    add_order(
        message.from_user.id,
        message.text
    )

    await message.answer(
        f"سفارش {message.text} ثبت شد ✅\n"
        "بعد از تایید پرداخت کانفیگ ارسال می‌شود.",
        reply_markup=menu
    )


@dp.message(lambda m: m.text == "📦 سفارش‌های من")
async def orders(message: Message):

    data = get_orders(message.from_user.id)

    if not data:
        await message.answer("هنوز سفارشی ندارید.")
        return

    text = "سفارش‌های شما:\n\n"

    for item in data:
        text += f"حجم: {item[0]}\nوضعیت: {item[1]}\n\n"

    await message.answer(text)


@dp.message(lambda m: m.text == "🎁 گیفت")
async def gift(message: Message):

    await message.answer(
        "کد گیفت را ارسال کنید."
    )


async def main():

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

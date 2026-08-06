import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

BOT_TOKEN = "8952198918:AAGuTIHUt49LzI97goCQf7Mesa0bBdOCWQM"

ADMIN_ID = 8635403087

CARD_NUMBER = "6104337300101910"



bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛒 خرید کانفینگ"),
            KeyboardButton(text="🎁 وارد کردن کد هدیه")
        ],
        [
            KeyboardButton(text="📦 کانفینگ های خریداری شده من"),
            KeyboardButton(text="💳 شارژ حساب")
        ],
        [
            KeyboardButton(text="⭐ امتیاز های من"),
            KeyboardButton(text="👥 زیر مجموعه گیری")
        ],
        [
            KeyboardButton(text="🛠 پشتیبانی")
        ]
    ],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start(message: Message):

    await message.answer(
        "سلام 👋\nبه ربات فروش کانفینگ خوش آمدید.",
        reply_markup=user_menu
    )


@dp.message()
async def menu(message: Message):

    user_id = message.from_user.id


    if message.text == "🛒 خرید کانفینگ":
        await message.answer(
            f"🛒 خرید کانفینگ\n\n"
            f"💳 شماره کارت:\n{CARD_NUMBER}\n\n"
            "بعد از پرداخت رسید را ارسال کنید."
        )


    elif message.text == "🎁 وارد کردن کد هدیه":
        await message.answer(
            "🎁 کد هدیه خود را ارسال کنید."
        )


    elif message.text == "📦 کانفینگ های خریداری شده من":
        await message.answer(
            "📦 لیست کانفینگ های شما:\n"
            "هنوز سفارشی ندارید."
        )


    elif message.text == "💳 شارژ حساب":
        await message.answer(
            f"💳 شارژ حساب\n\n"
            f"واریز به کارت:\n{CARD_NUMBER}\n\n"
            "رسید را ارسال کنید."
        )


    elif message.text == "⭐ امتیاز های من":
        await message.answer(
            "⭐ امتیاز شما: 0"
        )


    elif message.text == "👥 زیر مجموعه گیری":

        info = await bot.get_me()

        link = f"https://t.me/{info.username}?start={user_id}"

        await message.answer(
            f"👥 لینک دعوت شما:\n\n{link}\n\n"
            "با دعوت دوستان امتیاز بگیرید."
        )


    elif message.text == "🛠 پشتیبانی":
        await message.answer(
            "🛠 پیام خود را برای پشتیبانی ارسال کنید."
        )


async def main():

    print("Bot Started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

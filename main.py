import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

from db import (
    create_tables,
    add_user,
    get_points,
    get_configs
)


# =====================
# تنظیمات ربات
# =====================

BOT_TOKEN = "8952198918:AAGuTIHUt49LzI97goCQf7Mesa0bBdOCWQM"

ADMIN_ID = 8635403087

CARD_NUMBER = "6104337300101910"


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



# =====================
# منوی کاربر
# =====================

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

    add_user(
        message.from_user.id,
        message.from_user.username
    )

    await message.answer(
        "سلام 👋\n"
        "به ربات فروش کانفینگ خوش آمدید.",
        reply_markup=user_menu
    )



@dp.message()
async def buttons(message: Message):

    user_id = message.from_user.id


    if message.text == "🛒 خرید کانفینگ":

        await message.answer(
            "🛒 خرید کانفینگ\n\n"
            "حجم مورد نظر خود را ارسال کنید.\n\n"
            f"💳 شماره کارت:\n{CARD_NUMBER}\n\n"
            "بعد از پرداخت عکس رسید را ارسال کنید."
        )


    elif message.text == "🎁 وارد کردن کد هدیه":

        await message.answer(
            "🎁 کد هدیه را ارسال کنید."
        )


    elif message.text == "📦 کانفینگ های خریداری شده من":

        configs = get_configs(user_id)

        if configs:

            text = "📦 کانفینگ های شما:\n\n"

            for c in configs:
                text += f"• {c[0]}\n"

            await message.answer(text)

        else:

            await message.answer(
                "❌ هنوز کانفینگی خریداری نکرده‌اید."
            )


    elif message.text == "💳 شارژ حساب":

        await message.answer(
            "💳 شارژ حساب\n\n"
            f"شماره کارت:\n{CARD_NUMBER}\n\n"
            "رسید پرداخت را ارسال کنید."
        )


    elif message.text == "⭐ امتیاز های من":

        points = get_points(user_id)

        await message.answer(
            f"⭐ امتیاز شما: {points}"
        )


    elif message.text == "👥 زیر مجموعه گیری":

        info = await bot.get_me()

        link = f"https://t.me/{info.username}?start={user_id}"

        await message.answer(
            "👥 لینک زیرمجموعه گیری شما:\n\n"
            f"{link}"
        )


    elif message.text == "🛠 پشتیبانی":

        await message.answer(
            "🛠 پیام خود را ارسال کنید."
        )


    elif message.photo:

        await bot.send_photo(
            ADMIN_ID,
            message.photo[-1].file_id,
            caption=(
                "🧾 رسید پرداخت جدید\n\n"
                f"👤 آیدی کاربر: {user_id}"
            )
        )

        await message.answer(
            "✅ رسید شما برای مدیریت ارسال شد."
        )



async def main():

    create_tables()

    print("Bot Started")

    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command


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



# =====================
# منوی ادمین
# =====================

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎁 ساخت کد هدیه"),
            KeyboardButton(text="💳 درخواست های شارژ")
        ],
        [
            KeyboardButton(text="📢 پیام همگانی"),
            KeyboardButton(text="⚙️ تنظیمات ربات")
        ],
        [
            KeyboardButton(text="📦 سفارشات"),
            KeyboardButton(text="🗂 مدیریت پکیج ها")
        ],
        [
            KeyboardButton(text="👥 کاربران"),
            KeyboardButton(text="👑 پنل مدیریت")
        ],
        [
            KeyboardButton(text="⭐ افزودن امتیاز"),
            KeyboardButton(text="➕ افزودن ادمین")
        ]
    ],
    resize_keyboard=True
)



@dp.message(Command("start"))
async def start(message: Message):

    if message.from_user.id == ADMIN_ID:

        await message.answer(
            "👑 پنل مدیریت",
            reply_markup=admin_menu
        )

    else:

        await message.answer(
            "سلام 👋\nبه ربات فروش کانفینگ خوش آمدید.",
            reply_markup=user_menu
        )



@dp.message()
async def buttons(message: Message):

    user_id = message.from_user.id


    if message.text == "🛒 خرید کانفینگ":

        await message.answer(
            f"🛒 خرید کانفینگ\n\n"
            f"💳 شماره کارت:\n{CARD_NUMBER}\n\n"
            "بعد از پرداخت رسید را ارسال کنید."
        )


    elif message.text == "🎁 وارد کردن کد هدیه":

        await message.answer("🎁 کد هدیه را ارسال کنید.")


    elif message.text == "📦 کانفینگ های خریداری شده من":

        await message.answer("📦 لیست کانفینگ های شما")


    elif message.text == "💳 شارژ حساب":

        await message.answer(
            f"💳 واریز به کارت:\n{CARD_NUMBER}\n\n"
            "رسید را ارسال کنید."
        )


    elif message.text == "⭐ امتیاز های من":

        await message.answer("⭐ امتیاز شما: 0")


    elif message.text == "👥 زیر مجموعه گیری":

        info = await bot.get_me()

        link = f"https://t.me/{info.username}?start={user_id}"

        await message.answer(
            f"👥 لینک دعوت شما:\n{link}"
        )


    elif message.text == "🛠 پشتیبانی":

        await message.answer("🛠 پیام خود را ارسال کنید.")



async def main():

    print("Bot Started")

    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())

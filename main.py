import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.filters import Command


# =====================
# تنظیمات ربات
# =====================

BOT_TOKEN = "8952198918:AAGuTIHUt49LzI97goCQf7Mesa0bBdOCWQM"

ADMIN_ID = 8635403087

CARD_NUMBER = "6104337300101910"
"


bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()


# ذخیره موقت رسیدها
receipts = {}



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



# دکمه های رسید برای ادمین

receipt_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ تایید رسید",
                callback_data="accept_receipt"
            ),
            InlineKeyboardButton(
                text="❌ رد رسید",
                callback_data="reject_receipt"
            )
        ]
    ]
)
@dp.message(Command("start"))
async def start(message: Message):

    await message.answer(
        "سلام 👋\n"
        "به ربات فروش کانفینگ خوش آمدید.",
        reply_markup=user_menu
    )



@dp.message()
async def user_buttons(message: Message):

    user_id = message.from_user.id


    # خرید کانفینگ
    if message.text == "🛒 خرید کانفینگ":

        await message.answer(
            "🛒 خرید کانفینگ\n\n"
            "حجم مورد نظر خود را ارسال کنید.\n\n"
            f"💳 شماره کارت:\n{CARD_NUMBER}\n\n"
            "بعد از پرداخت عکس رسید را ارسال کنید."
        )


    # کد هدیه
    elif message.text == "🎁 وارد کردن کد هدیه":

        await message.answer(
            "🎁 کد هدیه خود را ارسال کنید."
        )


    # کانفینگ های خریداری شده
    elif message.text == "📦 کانفینگ های خریداری شده من":

        await message.answer(
            "📦 هنوز کانفینگی خریداری نکرده‌اید."
        )


    # شارژ حساب
    elif message.text == "💳 شارژ حساب":

        await message.answer(
            "💳 شارژ حساب\n\n"
            f"شماره کارت:\n{CARD_NUMBER}\n\n"
            "رسید پرداخت را ارسال کنید."
        )


    # امتیاز
    elif message.text == "⭐ امتیاز های من":

        await message.answer(
            "⭐ امتیاز شما: 0"
        )


    # زیرمجموعه
    elif message.text == "👥 زیر مجموعه گیری":

        info = await bot.get_me()

        link = f"https://t.me/{info.username}?start={user_id}"

        await message.answer(
            "👥 لینک زیرمجموعه گیری شما:\n\n"
            f"{link}"
        )


    # پشتیبانی
    elif message.text == "🛠 پشتیبانی":

        await message.answer(
            "🛠 پیام خود را برای پشتیبانی ارسال کنید."
        )


    # دریافت رسید عکس
    elif message.photo:

        receipts[user_id] = True

        await bot.send_photo(
            ADMIN_ID,
            message.photo[-1].file_id,
            caption=(
                "🧾 رسید پرداخت جدید\n\n"
                f"👤 آیدی کاربر:\n{user_id}"
            ),
            reply_markup=receipt_buttons
        )


        await message.answer(
            "✅ رسید شما ارسال شد.\n"
            "منتظر تایید پشتیبانی باشید."
        )



# =====================
# تایید رسید
# =====================

@dp.callback_query(F.data == "accept_receipt")
async def accept_receipt(call: CallbackQuery):

    text = call.message.caption

    user_id = int(
        text.split(":")[-1].strip()
    )


    await bot.send_message(
        user_id,
        "✅ پرداخت شما توسط پشتیبانی تایید شد.\n\n"
        "لطفاً منتظر ارسال کانفینگ باشید."
    )


    await call.answer(
        "رسید تایید شد"
    )



# =====================
# رد رسید
# =====================

@dp.callback_query(F.data == "reject_receipt")
async def reject_receipt(call: CallbackQuery):

    text = call.message.caption

    user_id = int(
        text.split(":")[-1].strip()
    )


    await bot.send_message(
        user_id,
        "❌ رسید شما توسط پشتیبانی رد شد."
    )


    await call.answer(
        "رسید رد شد"
    )



async def main():

    print("Bot Started")

    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())

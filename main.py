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

from db import get_points, get_referrals


# =====================
# تنظیمات
# =====================

BOT_TOKEN = "8952198918:AAGuTIHUt49LzI97goCQf7Mesa0bBdOCWQM"

ADMIN_ID = 8635403087

CARD_NUMBER = "6104337300101910"


bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()



# =====================
# منوی اصلی
# =====================

user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛒 خرید کانفینگ"),
            KeyboardButton(text="⭐ خرید با امتیاز")
        ],
        [
            KeyboardButton(text="📦 کانفینگ های خریداری شده من"),
            KeyboardButton(text="💳 شارژ حساب")
        ],
        [
            KeyboardButton(text="🎁 وارد کردن کد هدیه"),
            KeyboardButton(text="⭐ امتیاز های من")
        ],
        [
            KeyboardButton(text="👥 زیر مجموعه گیری"),
            KeyboardButton(text="🛠 پشتیبانی")
        ]
    ],
    resize_keyboard=True
)



# =====================
# دکمه برگشت
# =====================

back_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ برگشت")
        ]
    ],
    resize_keyboard=True
)



# =====================
# قیمت ها
# =====================

packages = {

    "⭐ 10 گیگ + 1 ماه": "150 تومان",

    "⭐ 15 گیگ + 1 ماه": "225 تومان",

    "⭐ 20 گیگ + 1 ماه": "300 تومان",

    "⭐ 30 گیگ + 1 ماه": "375 تومان",

    "⭐ 40 گیگ + 2 ماه": "465 تومان",

    "⭐ 50 گیگ + 2 ماه": "555 تومان",

    "⭐ 100 گیگ + 4 ماه": "700 تومان"

}



package_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=x)]
        for x in packages
    ]
    +
    [
        [KeyboardButton(text="⬅️ برگشت")]
    ],
    resize_keyboard=True
)



# =====================
# تایید رسید
# =====================

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
# =====================
# شروع
# =====================

@dp.message(Command("start"))
async def start(message: Message):

    await message.answer(
        "سلام 👋\n"
        "به ربات فروش کانفینگ خوش آمدید.",
        reply_markup=user_menu
    )



# =====================
# برگشت
# =====================

@dp.message(F.text == "⬅️ برگشت")
async def back(message: Message):

    await message.answer(
        "🏠 منوی اصلی",
        reply_markup=user_menu
    )



# =====================
# پنل کاربر
# =====================

@dp.message()
async def user_buttons(message: Message):

    user_id = message.from_user.id



    if message.text == "🛒 خرید کانفینگ":

        await message.answer(
            "🛒 لیست قیمت های کانفینگ ⭐️\n\n"
            "یک پکیج را انتخاب کنید:",
            reply_markup=package_menu
        )



    elif message.text in packages:

        price = packages[message.text]

        await message.answer(
            f"✅ پکیج انتخابی:\n\n"
            f"{message.text}\n"
            f"💰 قیمت: {price}\n\n"
            f"💳 شماره کارت:\n{CARD_NUMBER}\n\n"
            "بعد از پرداخت عکس رسید را ارسال کنید.",
            reply_markup=back_menu
        )



    elif message.text == "⭐ امتیاز های من":

        points = get_points(user_id)
        referrals = get_referrals(user_id)

        await message.answer(
            f"⭐ امتیاز شما: {points}\n\n"
            f"👥 تعداد زیرمجموعه‌ها: {referrals}",
            reply_markup=back_menu
        )



    elif message.text == "👥 زیر مجموعه گیری":

        me = await bot.get_me()

        link = f"https://t.me/{me.username}?start={user_id}"

        referrals = get_referrals(user_id)

        await message.answer(
            f"👥 لینک زیرمجموعه شما:\n\n"
            f"{link}\n\n"
            f"👤 تعداد دعوت‌ها: {referrals}\n"
            f"🎁 پاداش هر نفر: 5 امتیاز",
            reply_markup=back_menu
        )



    elif message.text == "⭐ خرید با امتیاز":

        await message.answer(
            "⭐ خرید با امتیاز به زودی فعال می‌شود.",
            reply_markup=back_menu
        )



    elif message.text == "🎁 وارد کردن کد هدیه":

        await message.answer(
            "🎁 کد هدیه را ارسال کنید.",
            reply_markup=back_menu
        )



    elif message.text == "📦 کانفینگ های خریداری شده من":

        await message.answer(
            "📦 هنوز کانفینگی ثبت نشده است.",
            reply_markup=back_menu
        )



    elif message.text == "💳 شارژ حساب":

        await message.answer(
            f"💳 شماره کارت:\n{CARD_NUMBER}\n\n"
            "رسید پرداخت را ارسال کنید.",
            reply_markup=back_menu
        )



    elif message.text == "🛠 پشتیبانی":

        await message.answer(
            "🛠 پیام خود را ارسال کنید.",
            reply_markup=back_menu
        )



    elif message.photo:

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
            "✅ رسید شما ارسال شد."
)
# =====================
# تایید رسید
# =====================

@dp.callback_query(F.data == "accept_receipt")
async def accept_receipt(call: CallbackQuery):

    user_id = int(
        call.message.caption.split(":")[-1].strip()
    )

    await bot.send_message(
        user_id,
        "✅ پرداخت شما توسط پشتیبانی تایید شد.\n\n"
        "لطفاً منتظر ارسال کانفینگ باشید."
    )

    await call.answer("رسید تایید شد")



# =====================
# رد رسید
# =====================

@dp.callback_query(F.data == "reject_receipt")
async def reject_receipt(call: CallbackQuery):

    user_id = int(
        call.message.caption.split(":")[-1].strip()
    )

    await bot.send_message(
        user_id,
        "❌ رسید شما توسط پشتیبانی رد شد."
    )

    await call.answer("رسید رد شد")



# =====================
# اجرای ربات
# =====================

async def main():

    print("Bot Started")

    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())        

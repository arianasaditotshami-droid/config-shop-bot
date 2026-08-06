from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from main import bot


router = Router()


# دکمه های رسید
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


# تایید رسید
@router.callback_query(F.data == "accept_receipt")
async def accept_receipt(call: CallbackQuery):

    user_id = call.message.caption.split(": ")[1]

    await bot.send_message(
        int(user_id),
        "✅ پرداخت شما توسط پشتیبانی تایید شد.\n\n"
        "لطفاً منتظر ارسال کانفینگ باشید."
    )

    await call.answer("رسید تایید شد")


# رد رسید
@router.callback_query(F.data == "reject_receipt")
async def reject_receipt(call: CallbackQuery):

    user_id = call.message.caption.split(": ")[1]

    await bot.send_message(
        int(user_id),
        "❌ رسید شما توسط پشتیبانی رد شد."
    )

    await call.answer("رسید رد شد")

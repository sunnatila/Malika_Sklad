from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def admin_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📦 Mahsulotlar bo'limi")
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def product_buttons() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Mahsulot qo'shish"),
                KeyboardButton(text="📋 Mahsulotlar ro'yxati"),
            ],
            [
                KeyboardButton(text="🔙 Orqaga"),
            ],
        ],
        resize_keyboard=True
    )


def product_type_buttons() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔋 Batareyka"),
                KeyboardButton(text="🔌 Zaryadka"),
            ],
            [
                KeyboardButton(text="🔙 Orqaga"),
            ],
        ],
        resize_keyboard=True
    )


def skip_button() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="⏭ O'tkazib yuborish"),
            ],
            [
                KeyboardButton(text="❌ Bekor qilish"),
            ],
        ],
        resize_keyboard=True
    )


def cancel_button() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="❌ Bekor qilish"),
            ],
        ],
        resize_keyboard=True
    )


remove_keyboard = ReplyKeyboardRemove()
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def admin_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📦 Mahsulotlar bo'limi")]],
        resize_keyboard=True, one_time_keyboard=True
    )


def product_buttons() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Mahsulot qo'shish"), KeyboardButton(text="📋 Mahsulotlar ro'yxati")],
            [KeyboardButton(text="🔙 Orqaga")],
        ],
        resize_keyboard=True
    )


def product_type_buttons() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔋 Batareyka"), KeyboardButton(text="🔌 Zaryadka")],
            [KeyboardButton(text="🖥 Display")],
            [KeyboardButton(text="🔙 Orqaga")],
        ],
        resize_keyboard=True
    )


def watt_buttons() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="45W"), KeyboardButton(text="65W"), KeyboardButton(text="90W")],
            [KeyboardButton(text="100W"), KeyboardButton(text="110W"), KeyboardButton(text="130W")],
            [KeyboardButton(text="135W"), KeyboardButton(text="150W"), KeyboardButton(text="170W")],
            [KeyboardButton(text="180W"), KeyboardButton(text="200W"), KeyboardButton(text="230W")],
            [KeyboardButton(text="240W"), KeyboardButton(text="280W"), KeyboardButton(text="300W")],
            [KeyboardButton(text="330W")],
            [KeyboardButton(text="⏭ O'tkazib yuborish")],
            [KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True
    )


def volt_buttons() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="19V"), KeyboardButton(text="19.5V"), KeyboardButton(text="20V")],
            [KeyboardButton(text="⏭ O'tkazib yuborish")],
            [KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True
    )


def hz_buttons() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="60Hz"), KeyboardButton(text="90Hz")],
            [KeyboardButton(text="120Hz"), KeyboardButton(text="144Hz")],
            [KeyboardButton(text="165Hz"), KeyboardButton(text="240Hz")],
            [KeyboardButton(text="⏭ O'tkazib yuborish")],
            [KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True
    )


def pin_buttons() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="20pin"), KeyboardButton(text="30pin")],
            [KeyboardButton(text="40pin"), KeyboardButton(text="50pin")],
            [KeyboardButton(text="⏭ O'tkazib yuborish")],
            [KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True
    )


def skip_button() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏭ O'tkazib yuborish")],
            [KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True
    )


def cancel_button() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True
    )


remove_keyboard = ReplyKeyboardRemove()

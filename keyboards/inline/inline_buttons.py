from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_yes"),
                InlineKeyboardButton(text="🔄 Qayta kiritish", callback_data="confirm_no"),
            ]
        ]
    )


def product_confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Saqlash", callback_data="product_save"),
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="product_cancel"),
            ]
        ]
    )


def product_list_keyboard(products, product_type) -> InlineKeyboardMarkup:
    """Mahsulotlar ro'yxatini inline button sifatida ko'rsatish"""
    buttons = []
    for product in products:
        buttons.append([
            InlineKeyboardButton(
                text=f"📌 {product['title']} ({product['count']} dona)",
                callback_data=f"product_view_{product['id']}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def product_detail_keyboard(product_id) -> InlineKeyboardMarkup:
    """Mahsulot tafsilotidagi amallar tugmalari"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📥 Qo'shish",
                    callback_data=f"product_increase_{product_id}"
                ),
                InlineKeyboardButton(
                    text="📤 Chiqarish",
                    callback_data=f"product_reduce_{product_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🗑 O'chirib tashlash",
                    callback_data=f"product_delete_{product_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Ortga qaytish",
                    callback_data=f"product_back_{product_id}"
                ),
            ]
        ]
    )


def product_delete_confirm_keyboard(product_id) -> InlineKeyboardMarkup:
    """O'chirishni tasdiqlash"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Ha, o'chirish",
                    callback_data=f"product_delete_yes_{product_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Yo'q, qaytish",
                    callback_data=f"product_delete_no_{product_id}"
                ),
            ]
        ]
    )


def product_reduce_cancel_keyboard(product_id) -> InlineKeyboardMarkup:
    """Chiqarish jarayonida bekor qilish"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data=f"product_reduce_cancel_{product_id}"
                ),
            ]
        ]
    )


def product_increase_cancel_keyboard(product_id) -> InlineKeyboardMarkup:
    """Qo'shish jarayonida bekor qilish"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data=f"product_increase_cancel_{product_id}"
                ),
            ]
        ]
    )
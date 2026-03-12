from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def product_confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="✅ Saqlash", callback_data="product_save"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="product_cancel"),
        ]]
    )


def product_list_keyboard(products, prefix) -> InlineKeyboardMarkup:
    """prefix: bat, chr, dsp"""
    buttons = []
    for p in products:
        buttons.append([
            InlineKeyboardButton(
                text=f"📌 {p['title']} ({p['count']} dona)",
                callback_data=f"{prefix}_view_{p['id']}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def product_detail_keyboard(product_id, prefix) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📥 Qo'shish", callback_data=f"{prefix}_inc_{product_id}"),
                InlineKeyboardButton(text="📤 Chiqarish", callback_data=f"{prefix}_dec_{product_id}"),
            ],
            [InlineKeyboardButton(text="🗑 O'chirib tashlash", callback_data=f"{prefix}_del_{product_id}")],
            [InlineKeyboardButton(text="⬅️ Ortga qaytish", callback_data=f"{prefix}_back_{product_id}")],
        ]
    )


def product_delete_confirm_keyboard(product_id, prefix) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="✅ Ha, o'chirish", callback_data=f"{prefix}_delyes_{product_id}"),
            InlineKeyboardButton(text="❌ Yo'q, qaytish", callback_data=f"{prefix}_delno_{product_id}"),
        ]]
    )


def action_cancel_keyboard(product_id, prefix, action) -> InlineKeyboardMarkup:
    """action: inc yoki dec"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"{prefix}_{action}cancel_{product_id}"),
        ]]
    )

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def product_confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="✅ Saqlash", callback_data="product_save"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="product_cancel"),
        ]]
    )


# ==================== BRAND FILTER ====================

def brand_filter_keyboard(categories, prefix) -> InlineKeyboardMarkup:
    buttons = []
    # Har bir brandni 2 talik qatorlarda chiqarish
    row = []
    for cat in categories:
        row.append(InlineKeyboardButton(text=f"🏷 {cat}", callback_data=f"{prefix}_brand_{cat}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    # "Barchasi" tugmasi
    buttons.append([InlineKeyboardButton(text="📦 Barchasi", callback_data=f"{prefix}_brand_all")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ==================== MAHSULOT RO'YXATI ====================

def product_list_keyboard(products, prefix, brand_filter=None) -> InlineKeyboardMarkup:
    buttons = []
    for p in products:
        buttons.append([
            InlineKeyboardButton(
                text=f"📌 {p['title']} ({p['count']} dona)",
                callback_data=f"{prefix}_view_{p['id']}"
            )
        ])

    if prefix in ("bat", "chr"):
        buttons.append([InlineKeyboardButton(text="⬅️ Brandlarga qaytish", callback_data=f"{prefix}_brandback_0")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ==================== MAHSULOT TAFSILOTI ====================

def product_detail_keyboard(product_id, prefix) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(text="📥 Qo'shish", callback_data=f"{prefix}_inc_{product_id}"),
            InlineKeyboardButton(text="📤 Chiqarish", callback_data=f"{prefix}_dec_{product_id}"),
        ],
    ]
    # Brand o'zgartirish faqat batareyka va zaryadka uchun
    if prefix in ("bat", "chr"):
        rows.append([InlineKeyboardButton(text="🏷 Brand o'zgartirish", callback_data=f"{prefix}_brchg_{product_id}")])
    rows.append([InlineKeyboardButton(text="🗑 O'chirib tashlash", callback_data=f"{prefix}_del_{product_id}")])
    rows.append([InlineKeyboardButton(text="⬅️ Ortga qaytish", callback_data=f"{prefix}_back_{product_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ==================== BRAND O'ZGARTIRISH ====================

BRANDS = ["HP", "Asus", "Acer", "Lenovo", "Dell", "Samsung",
          "Toshiba", "MSI"]


def brand_change_keyboard(product_id, prefix) -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for brand in BRANDS:
        row.append(InlineKeyboardButton(text=brand, callback_data=f"{prefix}_brnew_{product_id}_{brand}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    # Brand o'chirish
    buttons.append([InlineKeyboardButton(text="🚫 Brandni o'chirish", callback_data=f"{prefix}_brnew_{product_id}_none")])
    buttons.append([InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"{prefix}_brcancel_{product_id}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ==================== O'CHIRISH TASDIQLASH ====================

def product_delete_confirm_keyboard(product_id, prefix) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="✅ Ha, o'chirish", callback_data=f"{prefix}_delyes_{product_id}"),
            InlineKeyboardButton(text="❌ Yo'q, qaytish", callback_data=f"{prefix}_delno_{product_id}"),
        ]]
    )


def action_cancel_keyboard(product_id, prefix, action) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"{prefix}_{action}cancel_{product_id}"),
        ]]
    )

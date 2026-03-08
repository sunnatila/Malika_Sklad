import os
import tempfile

from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

from .start import AdminFilter
from loader import dp, db
from states import ProductReduce, ProductIncrease
from keyboards.default import (
    product_buttons, product_type_buttons
)
from keyboards.inline import (
    product_list_keyboard,
    product_detail_keyboard, product_delete_confirm_keyboard,
    product_reduce_cancel_keyboard, product_increase_cancel_keyboard
)


# ==================== YORDAMCHI FUNKSIYALAR ====================

def format_product_detail(product) -> str:
    """Mahsulot ma'lumotlarini formatlash"""
    product_type_emoji = "🔋" if product['product_type'] == "batareyka" else "🔌"
    type_name = "Batareyka" if product['product_type'] == "batareyka" else "Zaryadka"

    text = (
        f"📋 <b>Mahsulot haqida to'liq ma'lumot:</b>\n\n"
        f"🆔 ID: <b>{product['id']}</b>\n"
        f"{product_type_emoji} Tur: <b>{type_name}</b>\n"
        f"📝 Nomi: <b>{product['title']}</b>\n"
    )
    if product.get('brand_name'):
        text += f"🏭 Brend: <b>{product['brand_name']}</b>\n"
    if product.get('model_name'):
        text += f"📱 Model: <b>{product['model_name']}</b>\n"
    if product.get('watt'):
        text += f"⚡ Quvvat: <b>{product['watt']}</b>\n"
    if product.get('voltage'):
        text += f"🔌 Kuchlanish: <b>{product['voltage']}</b>\n"
    if product.get('capacity'):
        text += f"🔋 Sig'im: <b>{product['capacity']}</b>\n"
    text += f"📦 Soni: <b>{product['count']}</b> dona\n"

    if product.get('created_at'):
        text += f"📅 Qo'shilgan: <b>{product['created_at'].strftime('%d.%m.%Y %H:%M')}</b>\n"

    return text


def generate_products_excel(products, type_name, emoji) -> str:
    """Mahsulotlar ro'yxatini Excel faylga yozish"""
    wb = Workbook()
    ws = wb.active
    ws.title = type_name

    # Stillar
    header_font = Font(name='Arial', bold=True, color='FFFFFF', size=11)
    header_fill = PatternFill('solid', fgColor='2E86AB')
    data_font = Font(name='Arial', size=10)
    border = Border(
        left=Side(style='thin', color='D3D3D3'),
        right=Side(style='thin', color='D3D3D3'),
        top=Side(style='thin', color='D3D3D3'),
        bottom=Side(style='thin', color='D3D3D3')
    )
    center_align = Alignment(horizontal='center', vertical='center')
    left_align = Alignment(horizontal='left', vertical='center')

    # Sarlavha qatori
    headers = ['#', 'Nomi', 'Brend', 'Model', 'Quvvat', 'Kuchlanish', "Sig'im", 'Soni', "Qo'shilgan sana"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = border

    # Ma'lumotlar
    for idx, product in enumerate(products, 1):
        row = idx + 1
        created = product.get('created_at')
        created_str = created.strftime('%d.%m.%Y %H:%M') if created else ''

        row_data = [
            idx,
            product['title'],
            product.get('brand_name', '') or '',
            product.get('model_name', '') or '',
            product.get('watt', '') or '',
            product.get('voltage', '') or '',
            product.get('capacity', '') or '',
            product['count'],
            created_str
        ]

        # Juft/toq qator rangi
        row_fill = PatternFill('solid', fgColor='F0F8FF') if idx % 2 == 0 else PatternFill('solid', fgColor='FFFFFF')

        for col, value in enumerate(row_data, 1):
            cell = ws.cell(row=row, column=col, value=value)
            cell.font = data_font
            cell.border = border
            cell.fill = row_fill
            cell.alignment = center_align if col in [1, 8] else left_align

    # Jami qatori
    total_row = len(products) + 2
    total_fill = PatternFill('solid', fgColor='E8F5E9')
    total_font = Font(name='Arial', bold=True, size=10)

    ws.cell(row=total_row, column=1, value='').border = border
    jami_cell = ws.cell(row=total_row, column=2, value='JAMI:')
    jami_cell.font = total_font
    jami_cell.fill = total_fill
    jami_cell.border = border

    for col in range(3, 8):
        cell = ws.cell(row=total_row, column=col, value='')
        cell.fill = total_fill
        cell.border = border

    total_cell = ws.cell(row=total_row, column=8)
    total_cell.value = f'=SUM(H2:H{total_row - 1})'
    total_cell.font = total_font
    total_cell.fill = total_fill
    total_cell.border = border
    total_cell.alignment = center_align

    ws.cell(row=total_row, column=9, value='').fill = total_fill
    ws.cell(row=total_row, column=9).border = border

    # Ustun kengliklari
    col_widths = [5, 30, 15, 15, 12, 12, 15, 10, 18]
    for i, width in enumerate(col_widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = width

    # Birinchi qatorni muzlatish
    ws.freeze_panes = 'A2'

    # Faylni saqlash
    tmp = tempfile.NamedTemporaryFile(
        suffix='.xlsx',
        prefix=f'{type_name}_',
        delete=False,
        dir=tempfile.gettempdir()
    )
    filepath = tmp.name
    tmp.close()
    wb.save(filepath)

    return filepath


# ======================== MAHSULOTLAR RO'YXATI ========================

@dp.message(AdminFilter(), lambda msg: msg.text == "📋 Mahsulotlar ro'yxati")
async def product_list_start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        "Qaysi turdagi mahsulotlarni ko'rmoqchisiz?",
        reply_markup=product_type_buttons()
    )
    await state.set_state("product_list_type")


@dp.message(AdminFilter(), lambda msg: msg.text in ["🔋 Batareyka", "🔌 Zaryadka"])
async def product_list_by_type(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state != "product_list_type":
        return

    if msg.text == "🔋 Batareyka":
        product_type = "batareyka"
        type_name = "Batareykalar"
        emoji = "🔋"
    else:
        product_type = "zaryadka"
        type_name = "Zaryadkalar"
        emoji = "🔌"

    products = await db.get_products_by_type(product_type)

    if not products:
        await msg.answer(
            f"❗ {emoji} {type_name} bo'yicha mahsulotlar topilmadi",
            reply_markup=product_buttons()
        )
        await state.clear()
        return

    # Inline ro'yxat
    await msg.answer(
        f"{emoji} <b>{type_name}</b> ({len(products)} ta):\n\n"
        f"Batafsil ko'rish uchun mahsulotni tanlang 👇",
        reply_markup=product_list_keyboard(products, product_type)
    )

    # Excel faylni yaratish va yuborish
    try:
        filepath = generate_products_excel(products, type_name, emoji)
        doc = FSInputFile(filepath, filename=f"{type_name}.xlsx")
        await msg.answer_document(
            doc,
            caption=f"📊 {emoji} <b>{type_name}</b> ro'yxati — {len(products)} ta mahsulot"
        )
        os.unlink(filepath)
    except Exception as e:
        await msg.answer(f"❗ Excel faylni yaratishda xatolik: {str(e)}")

    await state.clear()
    await msg.answer("⬇️", reply_markup=product_buttons())


# ======================== MAHSULOT TAFSILOTI ========================

@dp.callback_query(lambda c: c.data.startswith("product_view_"))
async def product_view_detail(call: CallbackQuery):
    product_id = int(call.data.split("_")[-1])
    product = await db.get_product_by_id(product_id)

    if not product:
        await call.answer("❗ Mahsulot topilmadi", show_alert=True)
        return

    text = format_product_detail(product)
    await call.message.edit_text(text, reply_markup=product_detail_keyboard(product_id))


# ======================== ORTGA QAYTISH ========================

@dp.callback_query(lambda c: c.data.startswith("product_back_"))
async def product_back_to_list(call: CallbackQuery):
    product_id = int(call.data.split("_")[-1])
    product = await db.get_product_by_id(product_id)

    if not product:
        await call.answer("❗ Mahsulot topilmadi", show_alert=True)
        return

    product_type = product['product_type']
    products = await db.get_products_by_type(product_type)

    if product_type == "batareyka":
        type_name = "Batareykalar"
        emoji = "🔋"
    else:
        type_name = "Zaryadkalar"
        emoji = "🔌"

    await call.message.edit_text(
        f"{emoji} <b>{type_name}</b> ({len(products)} ta):\n\n"
        f"Batafsil ko'rish uchun mahsulotni tanlang 👇",
        reply_markup=product_list_keyboard(products, product_type)
    )


# ======================== 📥 QO'SHISH (INCREASE) ========================

@dp.callback_query(lambda c: c.data.startswith("product_increase_cancel_"))
async def product_increase_cancel(call: CallbackQuery, state: FSMContext):
    """Qo'shish jarayonini bekor qilish"""
    product_id = int(call.data.split("_")[-1])
    await state.clear()

    product = await db.get_product_by_id(product_id)
    if not product:
        await call.answer("❗ Mahsulot topilmadi", show_alert=True)
        return

    text = format_product_detail(product)
    await call.message.edit_text(text, reply_markup=product_detail_keyboard(product_id))


@dp.callback_query(lambda c: c.data.startswith("product_increase_"))
async def product_increase_start(call: CallbackQuery, state: FSMContext):
    product_id = int(call.data.split("_")[-1])
    product = await db.get_product_by_id(product_id)

    if not product:
        await call.answer("❗ Mahsulot topilmadi", show_alert=True)
        return

    await state.set_state(ProductIncrease.amount)
    await state.update_data(increase_product_id=product_id)

    await call.message.edit_text(
        f"📥 <b>Mahsulot soniga qo'shish</b>\n\n"
        f"📝 Mahsulot: <b>{product['title']}</b>\n"
        f"📦 Hozirgi soni: <b>{product['count']}</b> dona\n\n"
        f"Nechta qo'shilganini kiriting:",
        reply_markup=product_increase_cancel_keyboard(product_id)
    )


@dp.message(ProductIncrease.amount)
async def product_increase_amount(msg: Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get('increase_product_id')

    if not msg.text.isdigit():
        await msg.answer(
            "❗ Iltimos, faqat son kiriting!\n"
            "Harf yoki belgi kiritmang."
        )
        return

    amount = int(msg.text)

    if amount <= 0:
        await msg.answer("❗ Son 0 dan katta bo'lishi kerak!")
        return

    try:
        new_count = await db.increase_product_count(product_id, amount)
        await state.clear()

        await msg.answer(
            f"✅ Muvaffaqiyatli qo'shildi!\n\n"
            f"📥 Qo'shildi: <b>{amount}</b> dona\n"
            f"📦 Jami: <b>{new_count}</b> dona"
        )

        product = await db.get_product_by_id(product_id)
        if product:
            text = format_product_detail(product)
            await msg.answer(text, reply_markup=product_detail_keyboard(product_id))

    except Exception as e:
        await state.clear()
        await msg.answer(f"❌ Xatolik yuz berdi: {str(e)}")
        await msg.answer("📦 Mahsulotlar bo'limi", reply_markup=product_buttons())


# ======================== 📤 CHIQARISH (REDUCE) ========================

@dp.callback_query(lambda c: c.data.startswith("product_reduce_cancel_"))
async def product_reduce_cancel(call: CallbackQuery, state: FSMContext):
    """Chiqarish jarayonini bekor qilish"""
    product_id = int(call.data.split("_")[-1])
    await state.clear()

    product = await db.get_product_by_id(product_id)
    if not product:
        await call.answer("❗ Mahsulot topilmadi", show_alert=True)
        return

    text = format_product_detail(product)
    await call.message.edit_text(text, reply_markup=product_detail_keyboard(product_id))


@dp.callback_query(lambda c: c.data.startswith("product_reduce_"))
async def product_reduce_start(call: CallbackQuery, state: FSMContext):
    product_id = int(call.data.split("_")[-1])
    product = await db.get_product_by_id(product_id)

    if not product:
        await call.answer("❗ Mahsulot topilmadi", show_alert=True)
        return

    if product['count'] == 0:
        await call.answer("❗ Mahsulot soni 0 da, chiqarish mumkin emas!", show_alert=True)
        return

    await state.set_state(ProductReduce.amount)
    await state.update_data(reduce_product_id=product_id, product_count=product['count'])

    await call.message.edit_text(
        f"📤 <b>Mahsulotni ombordan chiqarish</b>\n\n"
        f"📝 Mahsulot: <b>{product['title']}</b>\n"
        f"📦 Hozirgi soni: <b>{product['count']}</b> dona\n\n"
        f"Nechta chiqarilganini kiriting (1 dan {product['count']} gacha):",
        reply_markup=product_reduce_cancel_keyboard(product_id)
    )


@dp.message(ProductReduce.amount)
async def product_reduce_amount(msg: Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get('reduce_product_id')
    product_count = data.get('product_count', 0)

    if not msg.text.isdigit():
        await msg.answer(
            "❗ Iltimos, faqat son kiriting!\n"
            "Harf yoki belgi kiritmang."
        )
        return

    amount = int(msg.text)

    if amount <= 0:
        await msg.answer("❗ Son 0 dan katta bo'lishi kerak!")
        return

    if amount > product_count:
        await msg.answer(
            f"❗ Xatolik! Siz <b>{amount}</b> ta kiritdingiz, "
            f"lekin omborda faqat <b>{product_count}</b> ta bor.\n\n"
            f"Iltimos, 1 dan {product_count} gacha son kiriting."
        )
        return

    try:
        new_count = await db.reduce_product_count(product_id, amount)
        await state.clear()

        await msg.answer(
            f"✅ Muvaffaqiyatli chiqarildi!\n\n"
            f"📤 Chiqarildi: <b>{amount}</b> dona\n"
            f"📦 Qoldi: <b>{new_count}</b> dona"
        )

        product = await db.get_product_by_id(product_id)
        if product:
            text = format_product_detail(product)
            await msg.answer(text, reply_markup=product_detail_keyboard(product_id))

    except Exception as e:
        await state.clear()
        await msg.answer(f"❌ Xatolik yuz berdi: {str(e)}")
        await msg.answer("📦 Mahsulotlar bo'limi", reply_markup=product_buttons())


# ======================== 🗑 O'CHIRIB TASHLASH ========================

@dp.callback_query(lambda c: c.data.startswith("product_delete_yes_"))
async def product_delete_confirm_yes(call: CallbackQuery):
    """O'chirishni tasdiqlash"""
    product_id = int(call.data.split("_")[-1])

    try:
        await db.delete_product(product_id)
        await call.message.edit_text("✅ Mahsulot muvaffaqiyatli o'chirildi!")
        await call.message.answer("📦 Mahsulotlar bo'limi", reply_markup=product_buttons())
    except Exception as e:
        await call.message.edit_text(f"❌ Xatolik yuz berdi: {str(e)}")


@dp.callback_query(lambda c: c.data.startswith("product_delete_no_"))
async def product_delete_confirm_no(call: CallbackQuery):
    """O'chirishni bekor qilish - mahsulot tafsilotiga qaytish"""
    product_id = int(call.data.split("_")[-1])
    product = await db.get_product_by_id(product_id)

    if not product:
        await call.answer("❗ Mahsulot topilmadi", show_alert=True)
        return

    text = format_product_detail(product)
    await call.message.edit_text(text, reply_markup=product_detail_keyboard(product_id))


@dp.callback_query(lambda c: c.data.startswith("product_delete_"))
async def product_delete_start(call: CallbackQuery):
    """O'chirishni so'rash"""
    product_id = int(call.data.split("_")[-1])
    product = await db.get_product_by_id(product_id)

    if not product:
        await call.answer("❗ Mahsulot topilmadi", show_alert=True)
        return

    await call.message.edit_text(
        f"🗑 <b>Mahsulotni o'chirib tashlash</b>\n\n"
        f"📝 <b>{product['title']}</b> ni o'chirmoqchimisiz?\n\n"
        f"⚠️ Diqqat! Bu amalni qaytarib bo'lmaydi!",
        reply_markup=product_delete_confirm_keyboard(product_id)
    )
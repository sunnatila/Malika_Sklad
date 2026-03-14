import os
import tempfile

from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

from .start import AdminFilter
from loader import dp, db
from states import ProductReduce, ProductIncrease
from keyboards.default import product_buttons, product_type_buttons
from keyboards.inline import (
    product_list_keyboard, product_detail_keyboard,
    product_delete_confirm_keyboard, action_cancel_keyboard
)

# ==================== KONFIGURATSIYA ====================

TYPE_CONFIG = {
    "batareyka": {
        "prefix": "bat", "name": "Batareyka", "plural": "Batareykalar", "emoji": "🔋",
        "table": "batteries",
        "headers": ['#', 'Nomi', 'Model', 'Soni', "Sana"],
        "widths": [5, 28, 16, 8, 14],
        "soni_col": 4,
        "row_fn": lambda p, i: [
            i, p['title'], p.get('model_name', '') or '',
            p['count'], p['created_at'].strftime('%d.%m.%Y') if p.get('created_at') else ''
        ],
        "get_all": "get_all_batteries", "get_by_id": "get_battery_by_id",
    },
    "zaryadka": {
        "prefix": "chr", "name": "Zaryadka", "plural": "Zaryadkalar", "emoji": "🔌",
        "table": "chargers",
        "headers": ['#', 'Nomi', 'Quvvat', 'Kuchlanish', 'Soni', "Sana"],
        "widths": [5, 28, 10, 12, 8, 14],
        "soni_col": 5,
        "row_fn": lambda p, i: [
            i, p['title'], p.get('watt', '') or '', p.get('voltage', '') or '',
            p['count'], p['created_at'].strftime('%d.%m.%Y') if p.get('created_at') else ''
        ],
        "get_all": "get_all_chargers", "get_by_id": "get_charger_by_id",
    },
    "display": {
        "prefix": "dsp", "name": "Display", "plural": "Displaylar", "emoji": "🖥",
        "table": "displays",
        "headers": ['#', 'Nomi', 'Hz', 'Pin', 'Soni', "Sana"],
        "widths": [5, 28, 10, 10, 8, 14],
        "soni_col": 5,
        "row_fn": lambda p, i: [
            i, p['title'], p.get('hz', '') or '', p.get('pin', '') or '',
            p['count'], p['created_at'].strftime('%d.%m.%Y') if p.get('created_at') else ''
        ],
        "get_all": "get_all_displays", "get_by_id": "get_display_by_id",
    },
}

PREFIX_MAP = {v["prefix"]: k for k, v in TYPE_CONFIG.items()}


def get_config_by_prefix(prefix):
    ptype = PREFIX_MAP.get(prefix)
    return TYPE_CONFIG[ptype] if ptype else None


# ==================== YORDAMCHI ====================

def format_detail(product, ptype) -> str:
    cfg = TYPE_CONFIG[ptype]
    text = (
        f"📋 <b>Mahsulot haqida to'liq ma'lumot:</b>\n\n"
        f"🆔 ID: <b>{product['id']}</b>\n"
        f"{cfg['emoji']} Tur: <b>{cfg['name']}</b>\n"
        f"📝 Nomi: <b>{product['title']}</b>\n"
    )
    if product.get('model_name'):
        text += f"📱 Model: <b>{product['model_name']}</b>\n"
    if product.get('voltage'):
        text += f"🔌 Kuchlanish: <b>{product['voltage']}</b>\n"
    if product.get('watt'):
        text += f"⚡ Quvvat: <b>{product['watt']}</b>\n"
    if product.get('hz'):
        text += f"📺 Chastota: <b>{product['hz']}</b>\n"
    if product.get('pin'):
        text += f"🔌 Pin: <b>{product['pin']}</b>\n"
    text += f"📦 Soni: <b>{product['count']}</b> dona\n"
    if product.get('created_at'):
        text += f"📅 Qo'shilgan: <b>{product['created_at'].strftime('%d.%m.%Y')}</b>\n"
    return text


def generate_excel(products, cfg) -> str:
    wb = Workbook()
    ws = wb.active
    ws.title = cfg['plural']

    hfont = Font(name='Arial', bold=True, color='FFFFFF', size=11)
    hfill = PatternFill('solid', fgColor='2E86AB')
    dfont = Font(name='Arial', size=10)
    brd = Border(
        left=Side(style='thin', color='D3D3D3'), right=Side(style='thin', color='D3D3D3'),
        top=Side(style='thin', color='D3D3D3'), bottom=Side(style='thin', color='D3D3D3')
    )
    ca = Alignment(horizontal='center', vertical='center')
    la = Alignment(horizontal='left', vertical='center')

    for col, h in enumerate(cfg['headers'], 1):
        c = ws.cell(row=1, column=col, value=h)
        c.font, c.fill, c.alignment, c.border = hfont, hfill, ca, brd

    for idx, p in enumerate(products, 1):
        row = idx + 1
        row_data = cfg['row_fn'](p, idx)
        rf = PatternFill('solid', fgColor='F0F8FF' if idx % 2 == 0 else 'FFFFFF')
        for col, val in enumerate(row_data, 1):
            c = ws.cell(row=row, column=col, value=val)
            c.font, c.border, c.fill = dfont, brd, rf
            c.alignment = ca if col in [1, cfg['soni_col']] else la

    tr = len(products) + 2
    tf = PatternFill('solid', fgColor='E8F5E9')
    tbf = Font(name='Arial', bold=True, size=10)
    for col in range(1, len(cfg['headers']) + 1):
        c = ws.cell(row=tr, column=col, value='')
        c.fill, c.border = tf, brd
    ws.cell(row=tr, column=2, value='JAMI:').font = tbf
    sl = ws.cell(row=1, column=cfg['soni_col']).column_letter
    tc = ws.cell(row=tr, column=cfg['soni_col'])
    tc.value, tc.font, tc.alignment = f'=SUM({sl}2:{sl}{tr-1})', tbf, ca

    for i, w in enumerate(cfg['widths'], 1):
        ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = w
    ws.freeze_panes = 'A2'

    tmp = tempfile.NamedTemporaryFile(suffix='.xlsx', prefix=f'{cfg["plural"]}_', delete=False, dir=tempfile.gettempdir())
    fp = tmp.name
    tmp.close()
    wb.save(fp)
    return fp


# ======================== RO'YXAT ========================

@dp.message(AdminFilter(), lambda msg: msg.text == "📋 Mahsulotlar ro'yxati")
async def product_list_start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Qaysi turdagi mahsulotlarni ko'rmoqchisiz?", reply_markup=product_type_buttons())
    await state.set_state("product_list_type")


@dp.message(AdminFilter(), lambda msg: msg.text in ["🔋 Batareyka", "🔌 Zaryadka", "🖥 Display"])
async def product_list_by_type(msg: Message, state: FSMContext):
    current = await state.get_state()
    if current != "product_list_type":
        return

    tmap = {"🔋 Batareyka": "batareyka", "🔌 Zaryadka": "zaryadka", "🖥 Display": "display"}
    ptype = tmap[msg.text]
    cfg = TYPE_CONFIG[ptype]

    products = await getattr(db, cfg['get_all'])()

    if not products:
        await state.clear()
        return await msg.answer(f"❗ {cfg['emoji']} {cfg['plural']} topilmadi", reply_markup=product_buttons())

    await msg.answer(
        f"{cfg['emoji']} <b>{cfg['plural']}</b> ({len(products)} ta):\n\nMahsulotni tanlang 👇",
        reply_markup=product_list_keyboard(products, cfg['prefix'])
    )

    try:
        fp = generate_excel(products, cfg)
        doc = FSInputFile(fp, filename=f"{cfg['plural']}.xlsx")
        await msg.answer_document(doc, caption=f"📊 {cfg['emoji']} <b>{cfg['plural']}</b> — {len(products)} ta mahsulot")
        os.unlink(fp)
    except Exception as e:
        await msg.answer(f"❗ Excel xatolik: {str(e)}")

    await state.clear()
    await msg.answer("⬇️", reply_markup=product_buttons())


# ======================== TAFSILOT ========================

@dp.callback_query(lambda c: c.data.split("_")[1] == "view")
async def product_view(call: CallbackQuery):
    parts = call.data.split("_")
    prefix, pid = parts[0], int(parts[2])
    cfg = get_config_by_prefix(prefix)
    if not cfg:
        return
    product = await getattr(db, cfg['get_by_id'])(pid)
    if not product:
        return await call.answer("❗ Topilmadi", show_alert=True)
    await call.message.edit_text(format_detail(product, PREFIX_MAP[prefix]), reply_markup=product_detail_keyboard(pid, prefix))


# ======================== ORTGA ========================

@dp.callback_query(lambda c: c.data.split("_")[1] == "back")
async def product_back(call: CallbackQuery):
    prefix = call.data.split("_")[0]
    cfg = get_config_by_prefix(prefix)
    if not cfg:
        return
    products = await getattr(db, cfg['get_all'])()
    await call.message.edit_text(
        f"{cfg['emoji']} <b>{cfg['plural']}</b> ({len(products)} ta):\n\nMahsulotni tanlang 👇",
        reply_markup=product_list_keyboard(products, prefix)
    )


# ======================== QO'SHISH ========================

@dp.callback_query(lambda c: c.data.split("_")[1] == "inccancel")
async def inc_cancel(call: CallbackQuery, state: FSMContext):
    parts = call.data.split("_")
    prefix, pid = parts[0], int(parts[2])
    cfg = get_config_by_prefix(prefix)
    await state.clear()
    product = await getattr(db, cfg['get_by_id'])(pid)
    if not product:
        return await call.answer("❗ Topilmadi", show_alert=True)
    await call.message.edit_text(format_detail(product, PREFIX_MAP[prefix]), reply_markup=product_detail_keyboard(pid, prefix))


@dp.callback_query(lambda c: c.data.split("_")[1] == "inc")
async def inc_start(call: CallbackQuery, state: FSMContext):
    parts = call.data.split("_")
    prefix, pid = parts[0], int(parts[2])
    cfg = get_config_by_prefix(prefix)
    product = await getattr(db, cfg['get_by_id'])(pid)
    if not product:
        return await call.answer("❗ Topilmadi", show_alert=True)
    await state.set_state(ProductIncrease.amount)
    await state.update_data(inc_id=pid, inc_prefix=prefix, inc_table=cfg['table'])
    await call.message.edit_text(
        f"📥 <b>Qo'shish</b>\n\n📝 {product['title']}\n📦 Hozirgi: <b>{product['count']}</b> dona\n\nNechta qo'shilganini kiriting:",
        reply_markup=action_cancel_keyboard(pid, prefix, "inc")
    )


@dp.message(ProductIncrease.amount)
async def inc_amount(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        return await msg.answer("❗ Faqat son kiriting!")
    amount = int(msg.text)
    if amount <= 0:
        return await msg.answer("❗ Son 0 dan katta bo'lishi kerak!")
    data = await state.get_data()
    pid, prefix, table = data['inc_id'], data['inc_prefix'], data['inc_table']
    cfg = get_config_by_prefix(prefix)
    try:
        new_count = await db.increase_count(table, pid, amount)
        await state.clear()
        await msg.answer(f"✅ Qo'shildi!\n\n📥 Qo'shildi: <b>{amount}</b>\n📦 Jami: <b>{new_count}</b> dona")
        product = await getattr(db, cfg['get_by_id'])(pid)
        if product:
            await msg.answer(format_detail(product, PREFIX_MAP[prefix]), reply_markup=product_detail_keyboard(pid, prefix))
    except Exception as e:
        await state.clear()
        await msg.answer(f"❌ Xatolik: {str(e)}")
        await msg.answer("📦 Mahsulotlar bo'limi", reply_markup=product_buttons())


# ======================== CHIQARISH ========================

@dp.callback_query(lambda c: c.data.split("_")[1] == "deccancel")
async def dec_cancel(call: CallbackQuery, state: FSMContext):
    parts = call.data.split("_")
    prefix, pid = parts[0], int(parts[2])
    cfg = get_config_by_prefix(prefix)
    await state.clear()
    product = await getattr(db, cfg['get_by_id'])(pid)
    if not product:
        return await call.answer("❗ Topilmadi", show_alert=True)
    await call.message.edit_text(format_detail(product, PREFIX_MAP[prefix]), reply_markup=product_detail_keyboard(pid, prefix))


@dp.callback_query(lambda c: c.data.split("_")[1] == "dec")
async def dec_start(call: CallbackQuery, state: FSMContext):
    parts = call.data.split("_")
    prefix, pid = parts[0], int(parts[2])
    cfg = get_config_by_prefix(prefix)
    product = await getattr(db, cfg['get_by_id'])(pid)
    if not product:
        return await call.answer("❗ Topilmadi", show_alert=True)
    if product['count'] == 0:
        return await call.answer("❗ Soni 0, chiqarish mumkin emas!", show_alert=True)
    await state.set_state(ProductReduce.amount)
    await state.update_data(dec_id=pid, dec_prefix=prefix, dec_table=cfg['table'], dec_count=product['count'])
    await call.message.edit_text(
        f"📤 <b>Chiqarish</b>\n\n📝 {product['title']}\n📦 Hozirgi: <b>{product['count']}</b> dona\n\n"
        f"Nechta chiqarilganini kiriting (1 dan {product['count']} gacha):",
        reply_markup=action_cancel_keyboard(pid, prefix, "dec")
    )


@dp.message(ProductReduce.amount)
async def dec_amount(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        return await msg.answer("❗ Faqat son kiriting!")
    amount = int(msg.text)
    if amount <= 0:
        return await msg.answer("❗ Son 0 dan katta bo'lishi kerak!")
    data = await state.get_data()
    pid, prefix, table, pcount = data['dec_id'], data['dec_prefix'], data['dec_table'], data['dec_count']
    cfg = get_config_by_prefix(prefix)
    if amount > pcount:
        return await msg.answer(f"❗ Omborda faqat <b>{pcount}</b> ta bor. 1 dan {pcount} gacha kiriting.")
    try:
        new_count = await db.reduce_count(table, pid, amount)
        await state.clear()
        await msg.answer(f"✅ Chiqarildi!\n\n📤 Chiqarildi: <b>{amount}</b>\n📦 Qoldi: <b>{new_count}</b> dona")
        product = await getattr(db, cfg['get_by_id'])(pid)
        if product:
            await msg.answer(format_detail(product, PREFIX_MAP[prefix]), reply_markup=product_detail_keyboard(pid, prefix))
    except Exception as e:
        await state.clear()
        await msg.answer(f"❌ Xatolik: {str(e)}")
        await msg.answer("📦 Mahsulotlar bo'limi", reply_markup=product_buttons())


# ======================== O'CHIRISH ========================

@dp.callback_query(lambda c: c.data.split("_")[1] == "delyes")
async def del_yes(call: CallbackQuery):
    parts = call.data.split("_")
    prefix, pid = parts[0], int(parts[2])
    cfg = get_config_by_prefix(prefix)
    try:
        await db.delete_product(cfg['table'], pid)
        await call.message.edit_text("✅ Mahsulot o'chirildi!")
        await call.message.answer("📦 Mahsulotlar bo'limi", reply_markup=product_buttons())
    except Exception as e:
        await call.message.edit_text(f"❌ Xatolik: {str(e)}")


@dp.callback_query(lambda c: c.data.split("_")[1] == "delno")
async def del_no(call: CallbackQuery):
    parts = call.data.split("_")
    prefix, pid = parts[0], int(parts[2])
    cfg = get_config_by_prefix(prefix)
    product = await getattr(db, cfg['get_by_id'])(pid)
    if not product:
        return await call.answer("❗ Topilmadi", show_alert=True)
    await call.message.edit_text(format_detail(product, PREFIX_MAP[prefix]), reply_markup=product_detail_keyboard(pid, prefix))


@dp.callback_query(lambda c: c.data.split("_")[1] == "del")
async def del_start(call: CallbackQuery):
    parts = call.data.split("_")
    prefix, pid = parts[0], int(parts[2])
    cfg = get_config_by_prefix(prefix)
    product = await getattr(db, cfg['get_by_id'])(pid)
    if not product:
        return await call.answer("❗ Topilmadi", show_alert=True)
    await call.message.edit_text(
        f"🗑 <b>O'chirib tashlash</b>\n\n📝 <b>{product['title']}</b> ni o'chirmoqchimisiz?\n\n⚠️ Bu amalni qaytarib bo'lmaydi!",
        reply_markup=product_delete_confirm_keyboard(pid, prefix)
    )

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from .start import AdminFilter
from loader import dp, db
from states import ProductAdd
from keyboards.default import (
    product_buttons, product_type_buttons,
    watt_buttons, volt_buttons, hz_buttons, pin_buttons,
    skip_button, cancel_button
)
from keyboards.inline import product_confirm_keyboard

VALID_WATTS = [
    "45W", "65W", "90W", "100W", "110W", "130W", "135W", "150W",
    "170W", "180W", "200W", "230W", "240W", "280W", "300W", "330W",
    "⏭ O'tkazib yuborish"
]
VALID_VOLTS = ["19V", "19.5V", "20V", "⏭ O'tkazib yuborish"]
VALID_HZ = ["60Hz", "90Hz", "120Hz", "144Hz", "165Hz", "240Hz", "⏭ O'tkazib yuborish"]
VALID_PIN = ["20pin", "30pin", "40pin", "50pin", "⏭ O'tkazib yuborish"]


# ======================== MAHSULOT QO'SHISH ========================

@dp.message(AdminFilter(), lambda msg: msg.text == "➕ Mahsulot qo'shish")
async def product_add_start(msg: Message, state: FSMContext):
    await state.set_state(ProductAdd.product_type)
    await msg.answer("Mahsulot turini tanlang:", reply_markup=product_type_buttons())


@dp.message(AdminFilter(), ProductAdd.product_type)
async def product_type_chosen(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        return await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
    if msg.text == "🔙 Orqaga":
        await state.clear()
        return await msg.answer("📦 Mahsulotlar bo'limi", reply_markup=product_buttons())

    types = {
        "🔋 Batareyka": ("batareyka", "Batareyka"),
        "🔌 Zaryadka": ("zaryadka", "Zaryadka"),
        "🖥 Display": ("display", "Display"),
    }
    if msg.text not in types:
        return await msg.answer("❗ Iltimos, tugmalardan birini tanlang:")

    ptype, pname = types[msg.text]
    await state.update_data(product_type=ptype, product_type_name=pname)
    await state.set_state(ProductAdd.title)
    await msg.answer("📝 Mahsulot nomini kiriting:", reply_markup=cancel_button())


@dp.message(AdminFilter(), ProductAdd.title)
async def title_entered(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        return await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())

    await state.update_data(title=msg.text)
    data = await state.get_data()

    if data['product_type'] == 'batareyka':
        await state.set_state(ProductAdd.model_name)
        await msg.answer("📱 Model nomini kiriting:", reply_markup=skip_button())
    elif data['product_type'] == 'zaryadka':
        await state.set_state(ProductAdd.watt)
        await msg.answer("⚡ Quvvatni tanlang:", reply_markup=watt_buttons())
    else:  # display
        await state.set_state(ProductAdd.hz)
        await msg.answer("📺 Chastotani tanlang (Hz):", reply_markup=hz_buttons())


# ========== BATAREYKA: model → count ==========

@dp.message(AdminFilter(), ProductAdd.model_name)
async def model_entered(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        return await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
    await state.update_data(model_name="" if msg.text == "⏭ O'tkazib yuborish" else msg.text)
    await state.set_state(ProductAdd.count)
    await msg.answer("📦 Mahsulot sonini kiriting:", reply_markup=cancel_button())


# ========== ZARYADKA: watt(button) → voltage(button) → count ==========

@dp.message(AdminFilter(), ProductAdd.watt)
async def watt_entered(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        return await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
    if msg.text not in VALID_WATTS:
        return await msg.answer("❗ Iltimos, taklif qilingan variantlardan birini tanlang:")
    await state.update_data(watt="" if msg.text == "⏭ O'tkazib yuborish" else msg.text)
    await state.set_state(ProductAdd.voltage)
    await msg.answer("🔌 Kuchlanishni tanlang:", reply_markup=volt_buttons())


@dp.message(AdminFilter(), ProductAdd.voltage)
async def voltage_entered(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        return await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
    if msg.text not in VALID_VOLTS:
        return await msg.answer("❗ Iltimos, variantlardan birini tanlang:")
    await state.update_data(voltage="" if msg.text == "⏭ O'tkazib yuborish" else msg.text)
    await state.set_state(ProductAdd.count)
    await msg.answer("📦 Mahsulot sonini kiriting:", reply_markup=cancel_button())


# ========== DISPLAY: hz → pin → count ==========

@dp.message(AdminFilter(), ProductAdd.hz)
async def hz_entered(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        return await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
    if msg.text not in VALID_HZ:
        return await msg.answer("❗ Iltimos, variantlardan birini tanlang:")
    await state.update_data(hz="" if msg.text == "⏭ O'tkazib yuborish" else msg.text)
    await state.set_state(ProductAdd.pin)
    await msg.answer("🔌 Pin turini tanlang:", reply_markup=pin_buttons())


@dp.message(AdminFilter(), ProductAdd.pin)
async def pin_entered(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        return await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
    if msg.text not in VALID_PIN:
        return await msg.answer("❗ Iltimos, variantlardan birini tanlang:")
    await state.update_data(pin="" if msg.text == "⏭ O'tkazib yuborish" else msg.text)
    await state.set_state(ProductAdd.count)
    await msg.answer("📦 Mahsulot sonini kiriting:", reply_markup=cancel_button())


# ========== SON VA TASDIQLASH ==========

@dp.message(AdminFilter(), ProductAdd.count)
async def count_entered(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        return await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
    if not msg.text.isdigit():
        return await msg.answer("❗ Iltimos, faqat son kiriting:")

    await state.update_data(count=int(msg.text))
    data = await state.get_data()

    emojis = {"batareyka": "🔋", "zaryadka": "🔌", "display": "🖥"}
    text = (
        f"📋 <b>Mahsulot ma'lumotlari:</b>\n\n"
        f"{emojis.get(data['product_type'], '📦')} Tur: <b>{data['product_type_name']}</b>\n"
        f"📝 Nomi: <b>{data['title']}</b>\n"
    )
    if data.get('model_name'):
        text += f"📱 Model: <b>{data['model_name']}</b>\n"
    if data.get('voltage'):
        text += f"🔌 Kuchlanish: <b>{data['voltage']}</b>\n"
    if data.get('watt'):
        text += f"⚡ Quvvat: <b>{data['watt']}</b>\n"
    if data.get('hz'):
        text += f"📺 Chastota: <b>{data['hz']}</b>\n"
    if data.get('pin'):
        text += f"🔌 Pin: <b>{data['pin']}</b>\n"
    text += f"📦 Soni: <b>{data['count']}</b>\n\n✅ Saqlashni tasdiqlaysizmi?"

    await state.set_state(ProductAdd.confirm)
    await msg.answer(text, reply_markup=product_confirm_keyboard())


@dp.callback_query(lambda c: c.data == "product_save")
async def product_save(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data:
        return await call.answer("❗ Ma'lumotlar topilmadi", show_alert=True)

    try:
        ptype = data['product_type']

        if ptype == 'batareyka':
            pid = await db.add_battery(
                data['title'], data.get('model_name', ''), data['count']
            )
        elif ptype == 'zaryadka':
            pid = await db.add_charger(
                data['title'], data.get('watt', ''),
                data.get('voltage', ''), data['count']
            )
        else:
            pid = await db.add_display(
                data['title'], data.get('hz', ''),
                data.get('pin', ''), data['count']
            )

        await state.clear()
        await call.message.edit_text(f"✅ Mahsulot muvaffaqiyatli saqlandi!\n🆔 ID: {pid}")
        await call.message.answer("📦 Mahsulotlar bo'limi", reply_markup=product_buttons())

    except Exception as e:
        await call.message.edit_text(f"❌ Xatolik yuz berdi: {str(e)}")
        await state.clear()
        await call.message.answer("📦 Mahsulotlar bo'limi", reply_markup=product_buttons())


@dp.callback_query(lambda c: c.data == "product_cancel")
async def product_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("❌ Mahsulot qo'shish bekor qilindi")
    await call.message.answer("📦 Mahsulotlar bo'limi", reply_markup=product_buttons())

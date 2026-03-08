from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from .start import AdminFilter
from loader import dp, db
from states import ProductAdd
from keyboards.default import (
    product_buttons, product_type_buttons,
    skip_button, cancel_button
)
from keyboards.inline import (
    product_confirm_keyboard
)


# ======================== MAHSULOT QO'SHISH ========================

@dp.message(AdminFilter(), lambda msg: msg.text == "➕ Mahsulot qo'shish")
async def product_add_start(msg: Message, state: FSMContext):
    await state.set_state(ProductAdd.product_type)
    await msg.answer(
        "Mahsulot turini tanlang:",
        reply_markup=product_type_buttons()
    )


@dp.message(AdminFilter(), ProductAdd.product_type)
async def product_type_chosen(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
        return

    if msg.text == "🔋 Batareyka":
        await state.update_data(product_type="batareyka", product_type_name="Batareyka")
    elif msg.text == "🔌 Zaryadka":
        await state.update_data(product_type="zaryadka", product_type_name="Zaryadka")
    elif msg.text == "🔙 Orqaga":
        await state.clear()
        await msg.answer("📦 Mahsulotlar bo'limi", reply_markup=product_buttons())
        return
    else:
        await msg.answer("❗ Iltimos, tugmalardan birini tanlang:")
        return

    await state.set_state(ProductAdd.title)
    await msg.answer("📝 Mahsulot nomini kiriting:", reply_markup=cancel_button())


@dp.message(AdminFilter(), ProductAdd.title)
async def product_title_entered(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
        return

    await state.update_data(title=msg.text)
    await state.set_state(ProductAdd.brand)
    await msg.answer("🏭 Brendni kiriting:", reply_markup=skip_button())


@dp.message(AdminFilter(), ProductAdd.brand)
async def product_brand_entered(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
        return

    if msg.text == "⏭ O'tkazib yuborish":
        await state.update_data(brand="")
    else:
        await state.update_data(brand=msg.text)

    await state.set_state(ProductAdd.model_name)
    await msg.answer("📱 Model nomini kiriting:", reply_markup=skip_button())


@dp.message(AdminFilter(), ProductAdd.model_name)
async def product_model_entered(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
        return

    if msg.text == "⏭ O'tkazib yuborish":
        await state.update_data(model_name="")
    else:
        await state.update_data(model_name=msg.text)

    await state.set_state(ProductAdd.watt)
    await msg.answer("⚡ Quvvatni kiriting (masalan: 20W, 65W):", reply_markup=skip_button())


@dp.message(AdminFilter(), ProductAdd.watt)
async def product_watt_entered(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
        return

    if msg.text == "⏭ O'tkazib yuborish":
        await state.update_data(watt="")
    else:
        await state.update_data(watt=msg.text)

    await state.set_state(ProductAdd.voltage)
    await msg.answer("🔌 Kuchlanishni kiriting (masalan: 3.7V, 12V):", reply_markup=skip_button())


@dp.message(AdminFilter(), ProductAdd.voltage)
async def product_voltage_entered(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
        return

    if msg.text == "⏭ O'tkazib yuborish":
        await state.update_data(voltage="")
    else:
        await state.update_data(voltage=msg.text)

    data = await state.get_data()

    # Batareyka uchun sig'im so'rash, zaryadka uchun o'tkazib yuborish
    if data.get("product_type") == "batareyka":
        await state.set_state(ProductAdd.capacity)
        await msg.answer("🔋 Sig'imni kiriting (masalan: 5000mAh):", reply_markup=skip_button())
    else:
        await state.update_data(capacity="")
        await state.set_state(ProductAdd.count)
        await msg.answer("📦 Mahsulot sonini kiriting:", reply_markup=cancel_button())


@dp.message(AdminFilter(), ProductAdd.capacity)
async def product_capacity_entered(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
        return

    if msg.text == "⏭ O'tkazib yuborish":
        await state.update_data(capacity="")
    else:
        await state.update_data(capacity=msg.text)

    await state.set_state(ProductAdd.count)
    await msg.answer("📦 Mahsulot sonini kiriting:", reply_markup=cancel_button())


@dp.message(AdminFilter(), ProductAdd.count)
async def product_count_entered(msg: Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        await msg.answer("❌ Bekor qilindi", reply_markup=product_buttons())
        return

    if not msg.text.isdigit():
        await msg.answer("❗ Iltimos, faqat son kiriting:")
        return

    await state.update_data(count=int(msg.text))
    data = await state.get_data()

    # Tasdiqlash uchun ma'lumotlarni ko'rsatish
    product_type_emoji = "🔋" if data['product_type'] == "batareyka" else "🔌"
    text = (
        f"📋 <b>Mahsulot ma'lumotlari:</b>\n\n"
        f"{product_type_emoji} Tur: <b>{data.get('product_type_name', '')}</b>\n"
        f"📝 Nomi: <b>{data['title']}</b>\n"
    )
    if data.get('brand'):
        text += f"🏭 Brend: <b>{data['brand']}</b>\n"
    if data.get('model_name'):
        text += f"📱 Model: <b>{data['model_name']}</b>\n"
    if data.get('watt'):
        text += f"⚡ Quvvat: <b>{data['watt']}</b>\n"
    if data.get('voltage'):
        text += f"🔌 Kuchlanish: <b>{data['voltage']}</b>\n"
    if data.get('capacity'):
        text += f"🔋 Sig'im: <b>{data['capacity']}</b>\n"
    text += f"📦 Soni: <b>{data['count']}</b>\n"
    text += "\n✅ Saqlashni tasdiqlaysizmi?"

    await state.set_state(ProductAdd.confirm)
    await msg.answer(text, reply_markup=product_confirm_keyboard())


@dp.callback_query(lambda c: c.data == "product_save")
async def product_save_callback(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if not data:
        await call.answer("❗ Ma'lumotlar topilmadi", show_alert=True)
        return

    try:
        category_name = data.get('product_type_name', 'Boshqa')
        category_id = await db.get_or_create_category(category_name)

        brand_id = None
        if data.get('brand'):
            brand_id = await db.get_or_create_brand(data['brand'])

        product_id = await db.add_product(
            title=data['title'],
            product_type=data['product_type'],
            category_id=category_id,
            brand_id=brand_id,
            model_name=data.get('model_name', ''),
            watt=data.get('watt', ''),
            voltage=data.get('voltage', ''),
            capacity=data.get('capacity', ''),
            count=data['count']
        )

        await state.clear()
        await call.message.edit_text(
            f"✅ Mahsulot muvaffaqiyatli saqlandi!\n"
            f"🆔 ID: {product_id}"
        )
        await call.message.answer(
            "📦 Mahsulotlar bo'limi",
            reply_markup=product_buttons()
        )

    except Exception as e:
        await call.message.edit_text(f"❌ Xatolik yuz berdi: {str(e)}")
        await state.clear()
        await call.message.answer(
            "📦 Mahsulotlar bo'limi",
            reply_markup=product_buttons()
        )


@dp.callback_query(lambda c: c.data == "product_cancel")
async def product_cancel_callback(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("❌ Mahsulot qo'shish bekor qilindi")
    await call.message.answer(
        "📦 Mahsulotlar bo'limi",
        reply_markup=product_buttons()
    )



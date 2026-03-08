
from aiogram import types
from aiogram.filters import CommandStart, BaseFilter

from data.config import ADMINS
from loader import dp
from keyboards.default import admin_menu, product_buttons



class AdminFilter(BaseFilter):
    async def __call__(self, msg: types.Message,  *args, **kwargs):
        return str(msg.from_user.id) in ADMINS



@dp.message(AdminFilter(),CommandStart())
async def bot_start(message: types.Message):
    await message.answer("Assalomu Alaykum. Admin panelga xush kelibsiz.\n"
                         "Kerakli tugmachani bo'sing", reply_markup=admin_menu())



@dp.message(AdminFilter(),lambda msg: msg.text == "📦 Mahsulotlar bo'limi")
async def product_panel_func(message: types.Message):
    await message.answer("Mahsulotlar bo'limi", reply_markup=product_buttons())


@dp.message(AdminFilter(),lambda msg: msg.text == "🔙 Orqaga")
async def back_func(message: types.Message):
    await message.answer("Iltimos, kerakli kategoriyani tanlang 😊", reply_markup=admin_menu())


from aiogram.fsm.state import StatesGroup, State

class ProductAdd(StatesGroup):
    product_type = State()
    title = State()             # mahsulot nomi
    brand = State()             # brend
    model_name = State()        # model nomi
    watt = State()              # quvvat (W)
    voltage = State()           # kuchlanish (V)
    capacity = State()          # sig'im (mAh) - faqat batareyka uchun
    count = State()             # soni
    confirm = State()           # tasdiqlash

class ProductReduce(StatesGroup):
    amount = State()


class ProductIncrease(StatesGroup):
    amount = State()
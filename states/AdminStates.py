from aiogram.fsm.state import StatesGroup, State


class ProductAdd(StatesGroup):
    product_type = State()
    title = State()
    # Battery
    model_name = State()
    # Charger
    watt = State()
    voltage = State()
    # Display
    hz = State()
    pin = State()
    # Umumiy
    count = State()
    confirm = State()


class ProductReduce(StatesGroup):
    amount = State()


class ProductIncrease(StatesGroup):
    amount = State()

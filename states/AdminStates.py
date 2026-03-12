from aiogram.fsm.state import StatesGroup, State


class ProductAdd(StatesGroup):
    product_type = State()      # batareyka, zaryadka yoki display
    title = State()
    brand = State()
    model_name = State()
    # Batareyka / Zaryadka
    watt = State()
    voltage = State()
    capacity = State()          # faqat batareyka
    # Display
    hz = State()
    pin = State()
    count = State()
    confirm = State()


class ProductReduce(StatesGroup):
    amount = State()


class ProductIncrease(StatesGroup):
    amount = State()
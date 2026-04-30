"""FSM-состояния для оформления заказа"""
from aiogram.fsm.state import State, StatesGroup


class CheckoutForm(StatesGroup):
    name = State()
    phone = State()
    address = State()
    confirm = State()

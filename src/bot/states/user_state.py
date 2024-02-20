from aiogram.fsm.state import StatesGroup, State


class UserSetPriceForElectricityState(StatesGroup):
    price = State()


class AlgorithmState(StatesGroup):
    terahesh = State()
    consumption = State()

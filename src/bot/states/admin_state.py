from aiogram.fsm.state import StatesGroup, State


class NewsletterState(StatesGroup):
    photo_or_video = State()
    text = State()
    end = State()

    products_set = State()

from aiogram.dispatcher.filters.state import State, StatesGroup

class link(StatesGroup):
    link = State()

class mailing(StatesGroup):
    text = State()

class newAlbum(StatesGroup):
    title = State()
    artist = State()

class editFile(StatesGroup):
    link = State()
    file = State()
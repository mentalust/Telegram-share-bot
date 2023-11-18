from aiogram import types
from aiogram.types import Message

main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(types.KeyboardButton(text='Меню'))

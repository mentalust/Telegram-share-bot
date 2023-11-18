from aiogram import types
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton as ib
from aiogram.types import InlineKeyboardMarkup as im
import config
from data import sql as databs

adm = im()
adm.add(ib('Изменить линк на канал', callback_data='change_link_channel'))
adm.add(ib('Файлы', callback_data='all_files'))
adm.add(ib('Рассылка', callback_data='mailing'))
adm.add(ib('Изменить файл', callback_data='change_file'))
adm.add(ib('Альбомы', callback_data='albums'))

cancel = im()
cancel.add(ib('Отмена', callback_data='cancel'))

albums = im()
albums.add(ib('Создать новый', callback_data='new_album'))
albums.add(ib('Удалить', callback_data='delete_album'))

async def all_files():
    menu = im(row_width=1)
    for i in await databs.count_all_files():
        if i == 20:
            break
        menu.add(ib(f'{i[2]} - {i[3]}', callback_data=f'delete_file_{i[0]}'))
    return menu

async def all_albums():
    menu = im(row_width=1)
    for i in await databs.count_all_albums():
        if i == 20:
            break
        menu.add(ib(f'{i[2]} - {i[3]}', callback_data=f'info_album_{i[0]}'))
    return menu

mail = im()
mail.add(ib(text='📨 Начать', callback_data='go_mail'))

async def add_file():
    menu = im()
    menu.add(ib('Single', callback_data='addFileSingle'))
    for i in await databs.count_all_albums():
        menu.add(ib(f'{i[2]} - {i[3]}', callback_data=f'addToAlbum_{i[0]}'))
    return menu

powered = im()
powered.add(ib('Powered by @cakels', 't.me/cakels'))
from typing import Tuple
import aiogram
from aiogram import executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
import json
import datetime
import random
from datetime import timedelta
now = datetime.datetime.now()
import asyncio

import config

from loader import bot, dp
from keyboards import inl as inl
from keyboards import reply as reply
from data import sql as databs

from state import states

import sqlite3
db = sqlite3.connect('db.db', check_same_thread=False)
sql = db.cursor()


async def change_link_channel(c: types.CallbackQuery):
    await c.message.answer('Введите новый линк')
    await states.link.link.set()

async def all_files(c):
    await c.message.edit_text('Вот первые 20 файлов', reply_markup=await inl.all_files())

async def delete_file(c):
    link = c.data.split('_')[2]
    if sql.execute('SELECT * FROM files WHERE link = ?;', (link,)).fetchone() is None:
        await c.answer('Ошибка')
        await all_files(c)
        return
    info = sql.execute('SELECT * FROM files WHERE link = ?;', (link,)).fetchone()
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton('Открыть', f'https://t.me/{config.username_bot}?start={info[0]}'))
    menu.add(types.InlineKeyboardButton('Удалить', callback_data=f'confirm_delete_{info[0]}'))
    await c.message.edit_text(f'Вы точно хотите удалить "{info[2]} - {info[3]}"?\nСтатистика: {info[4]}\nЛинк: https://t.me/{config.username_bot}?start={info[0]}', reply_markup=menu)

async def confirm_delete(c):
    link = c.data.split('_')[2]
    if sql.execute('SELECT * FROM files WHERE link = ?;', (link,)).fetchone() is None:
        await c.answer('Ошибка')
        await all_files(c)
        return
    sql.execute('DELETE FROM files WHERE link = ?;', (link,))
    db.commit()
    await c.answer('Успешно удалено')
    await all_files(c)

async def mailing(c):
    await c.message.edit_text('Введите текст рассылки')
    await states.mailing.text.set()

async def go_mail(c):
    text = c.message.text
    await c.message.edit_text(text)
    info = sql.execute('SELECT id FROM users;').fetchall()
    a = 0
    b = 0
    count = sql.execute(f'SELECT COUNT(*) FROM users;').fetchone()[0]
    n = await c.message.answer(f'Рассылка начата {datetime.datetime.now().strftime("%H:%M:%S")}')
    for i in range(len(info)):
        try:
            await bot.send_message(info[i][0], text, parse_mode='HTML')
            a += 1
        except:
            b += 1
    await n.edit_text(n.text + '\n\n'
            f'✅ Рассылка завершена! {datetime.datetime.now().strftime("%H:%M:%S")}\nВсего: {count}\nУспешно: {a}\nНе успешно: {b}')

async def change_file(c):
    await c.message.edit_text('Введите линк')
    await states.editFile.link.set()

async def albums(c):
    await c.message.edit_text('Действие:', reply_markup=inl.albums)

async def new_album(c):
    await c.message.edit_text('Введите название альбома')
    await states.newAlbum.title.set()

async def delete_album(c):
    await c.message.edit_text('Вот все альбомы', reply_markup=await inl.all_albums())

async def info_album(c):
    link = c.data.split('_')[2]
    data = sql.execute('SELECT * FROM files WHERE link = ?;', (link,)).fetchone()
    if data[5] != 'album':
        await c.message.edit_text('Это не альбом')
        return
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton('Удалить', callback_data=f'AlbDelete_{data[0]}'))
    menu.add(types.InlineKeyboardButton('Назад', callback_data='delete_album'))
    if data[1] is None:
        count = '0'
    else:
        count = len(data[1].split(','))-1
    await c.message.edit_text(f'{data[2]} - {data[3]}\n'
        f'Кол. треков: {count}\n'
        f'Link: https://t.me/{config.username_bot}?start={data[0]}', reply_markup=menu)

async def AlbDelete(c):
    link = c.data.split('_')[1]
    sql.execute('DELETE FROM files WHERE link = ?;', (link,))
    db.commit()
    await c.answer('Успешно удалено')
    await delete_album(c)

async def addFileSingle(c):
    a = c.message.reply_to_message.audio
    title = a.title
    artist = a.performer
    file_id = a.file_id
    chars = 'abcdefghyjklmnopqrstuvwxyz'
    chars += chars.upper()
    chars += '1234567890'
    pas = ''.join(random.sample(chars, 6))
    await databs.add_track(title, artist, file_id, pas)
    await c.message.edit_text(f'Успешно добавлено как Single!\n\nhttps://t.me/{config.username_bot}?start={pas}')

async def addToAlbum(c):
    link = c.data.split('_')[1]
    perv = sql.execute('SELECT * FROM files WHERE link = ?;', (link,)).fetchone()[1]
    if perv is None:
        perv = c.message.reply_to_message.audio.file_id + ','
    else:
        perv += c.message.reply_to_message.audio.file_id + ','
    sql.execute('UPDATE files SET id = ? WHERE link = ?', (perv, link,))
    db.commit()
    await c.message.edit_text(f'Успешно добавлено в альбом\n\nhttps://t.me/{config.username_bot}?start={link}')

async def cancel(c, state):
    await c.message.delete()
    await state.finish()
    await c.message.answer('Админ панель', reply_markup=inl.adm)

def startup(dp):
    dp.register_callback_query_handler(change_link_channel, text='change_link_channel', state='*')
    dp.register_callback_query_handler(all_files, text='all_files', is_admin=True)
    dp.register_callback_query_handler(mailing, text='mailing', is_admin=True)
    dp.register_callback_query_handler(go_mail, text='go_mail', is_admin=True)
    dp.register_callback_query_handler(change_file, text='change_file', is_admin=True)
    dp.register_callback_query_handler(albums, text='albums', is_admin=True)
    dp.register_callback_query_handler(new_album, text='new_album', is_admin=True)
    dp.register_callback_query_handler(delete_album, text='delete_album', is_admin=True)

    dp.register_callback_query_handler(cancel, text='cancel', is_admin=True, state='*')

    dp.register_callback_query_handler(addFileSingle, text='addFileSingle', is_admin=True)

    dp.register_callback_query_handler(delete_file, text_startswith='delete_file_', state='*', is_admin=True)
    dp.register_callback_query_handler(confirm_delete, text_startswith='confirm_delete_', state='*', is_admin=True)
    dp.register_callback_query_handler(info_album, text_startswith='info_album_', is_admin=True)
    dp.register_callback_query_handler(AlbDelete, text_startswith='AlbDelete_', is_admin=True)

    dp.register_callback_query_handler(addToAlbum, text_startswith='addToAlbum_', is_admin=True)
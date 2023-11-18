# - *- coding: utf- 8 - *-
import asyncio
from logging import error
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares import logging

import config
from handlers.default import startup as default
from handlers.inline import startup as inline
from utils.error import stratup as errors
from others.set_bot_commands import set_commands
import middlewares
from filters.filters import binds


from loader import bot, dp

async def on_startup():
	await bot.send_message(our telegram id, 'Бот перезапущен')


async def main():
	print('Started')

	# фильтры
	binds(dp)

	# дефолт хендлеры для обработки инлайна и текста
	default(dp)
	inline(dp)

	# обработка ошибок и логгирование
	errors(dp)

	# антифлуд
	# middlewares.setup(dp)

	# установка комманд
	await set_commands(dp)

	await on_startup()

	try:
		await dp.start_polling()
	finally:
		await dp.storage.close()
		await dp.storage.wait_closed()
		await bot.session.close()





if __name__ == "__main__":
	try:
		asyncio.run(main())
	except (KeyboardInterrupt, SystemExit):
		print('Bot STOPPED!!!')

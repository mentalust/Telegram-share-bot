from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config

bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=MemoryStorage())

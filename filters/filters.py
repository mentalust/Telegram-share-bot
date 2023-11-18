import typing

from aiogram import Bot, Dispatcher,  executor, types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types.base import TelegramObject

from loader import dp, bot
from keyboards import inl as inl
from keyboards import reply as reply

import config

class IsAdmin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.isin = is_admin

    async def check(self, m: types.Message):
        return m.from_user.id in config.admins


def binds(dp):
    dp.filters_factory.bind(IsAdmin)
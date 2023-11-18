import logging
from aiogram.bot.bot import Bot
from aiogram.utils import exceptions

from aiogram.utils.exceptions import InvalidQueryID, MessageNotModified, NetworkError, MessageIsTooLong, MessageTextIsEmpty, WrongFileIdentifier

from loader import dp

logging.basicConfig(
    level=logging.ERROR,
    format=u'[%(levelname)s] [%(asctime)s] | [%(filename)s LINE:%(lineno)d] | %(message)s',
    datefmt="%d-%b-%y %H:%M:%S"
    )

async def error_handler(update, e):
    logging.error(e)
    return True


def stratup(dp):
    dp.register_errors_handler(error_handler, exception=MessageNotModified)
    dp.register_errors_handler(error_handler, exception=InvalidQueryID)
    dp.register_errors_handler(error_handler, exception=NetworkError)
    dp.register_errors_handler(error_handler, exception=MessageIsTooLong)
    dp.register_errors_handler(error_handler, exception=MessageTextIsEmpty)
    dp.register_errors_handler(error_handler, exception=WrongFileIdentifier)
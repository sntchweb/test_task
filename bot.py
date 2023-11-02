import asyncio
import json
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv

from calculations import calc_result

load_dotenv()
dp = Dispatcher()
TOKEN = os.getenv('TG_TOKEN')


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f'Hi, {hbold(message.from_user.full_name)}!')


@dp.message()
async def message_handler(message: types.Message):
    try:
        user_message_to_dict = json.loads(message.text)
        result = await calc_result(
            user_message_to_dict.get('dt_from'),
            user_message_to_dict.get('dt_upto'),
            user_message_to_dict.get('group_type')
        )
        await message.answer(str(result))
    except TypeError:
        await message.answer('Невалидный запрос. Пример запроса: '
                             '{"dt_from": "2022-09-01T00:00:00", '
                             '"dt_upto": "2022-12-31T23:59:00", '
                             '"group_type": "month"}')


async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

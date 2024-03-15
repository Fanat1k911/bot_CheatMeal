import asyncio
import datetime
import logging
import os

from aiogram import Dispatcher, types, F, Bot, Router
from aiogram.filters import CommandStart, BaseFilter
from aiogram.filters.command import Command

from aiobot_cheatmeal.bot.settings import config
from aiobot_cheatmeal.bot.keyboards import keyboards
from aiobot_cheatmeal.bot.common.list_commands import cmds
from aiobot_cheatmeal.bot.handlers.commands import command_router

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

time_now = datetime.datetime.now().strftime('%H:%M')
today_now = datetime.datetime.date(datetime.datetime.now()).strftime('%d.%m.%Y')

logging.basicConfig(
    filename='/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/logging/logging.log',
    level=logging.INFO)
dp = Dispatcher()
bot = Bot(token=os.getenv('TOKEN_API'), parse_mode='HTML')


async def main():
    dp.include_router(command_router)

    await bot.delete_my_commands()
    await bot.set_my_commands(commands=cmds)
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)


if __name__ == '__main__':
    asyncio.run(main())

# C:\Users\HomeMachine\Desktop\ngrok.exe http 8080
# Emoji : win+.
# botID = 6373698793
# from aiogram.enums.dice_emoji import DiceEmoji  - класс эмоджи игровая группа
#############################################################################################
# Чтобы убрать кнопку из inline-клавиатуры после нажатия на нее в Telegram,
# вам нужно отправить запрос на обновление сообщения с обновленной inline-клавиатурой.
#
# Вот пример кода, как это можно сделать с использованием aiogram 3.2:

# Обработчик нажатия на кнопку
# @dp.callback_query_handler(lambda callback_query: True)
# async def process_callback_button(callback_query: types.CallbackQuery):
#     # Убираем кнопку из inline-клавиатуры
#     await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
#                                         message_id=callback_query.message.message_id,
#                                         reply_markup=None)
#     await bot.answer_callback_query(callback_query.id, text='Button removed')

# В этом примере при нажатии на кнопку будет вызываться обработчик,
# который сначала убирает кнопку из inline-клавиатуры с помощью метода `edit_message_reply_markup`,
# а затем отправляет ответ пользователю с помощью метода `answer_callback_query`.

import asyncio
import datetime
import logging
import os

from aiogram import Dispatcher, types, F, Bot, Router
from aiogram.filters import CommandStart, BaseFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

import aiobot_cheatmeal.bot.handlers.commands
from aiobot_cheatmeal.bot.settings import config
from aiobot_cheatmeal.bot.keyboards import keyboards
from aiobot_cheatmeal.bot.utils.states import Location
from aiobot_cheatmeal.bot.handlers.locations.Poolbar import poolbar_router
from aiobot_cheatmeal.bot.handlers.locations.Window import window_router
from aiobot_cheatmeal.bot.handlers.locations.Tubing import tubing_router
from aiobot_cheatmeal.bot.handlers.commands import command_router
from aiobot_cheatmeal.bot.handlers.categories import categories_router
from aiobot_cheatmeal.bot.data.dictdata import Poolbar, Window, Curds, result_report, result, report
from aiobot_cheatmeal.bot.utils import is_admin

time_now = datetime.datetime.now().strftime('%H:%M')
today_now = datetime.datetime.date(datetime.datetime.now()).strftime('%d.%m.%Y')

logging.basicConfig(level=logging.INFO)
dp = Dispatcher(storage=result_report)
bot = Bot(token=config.TOKEN_API, parse_mode='HTML')


@dp.message(Location.any_report, F.text == 'ДА')
async def go_more_report(msg: Message, state: FSMContext):
    print(msg.text, 'Были еще локации с продажами, будем заполнять')
    await state.set_state(Location.choose_location)
    await msg.answer('Выберите локацию продаж:', reply_markup=keyboards.inline_area_kb)


@dp.message(Location.any_report, F.text == 'НЕТ')
async def go_more_report(msg: Message, state: FSMContext):
    await state.set_state(Location.wastes)
    print('Других локаций с прибылью не было')
    await msg.answer('Хорошо! Сегодня были траты наличных?', reply_markup=keyboards.yes_or_no_kb)

    print('result_report >>>', result_report.storage.items())
    print('result >>>', result.items())
    print(keyboards.inline_area_kb.model_dump()['inline_keyboard'][0][0]['callback_data'])
    # TODO: доступ к кнопке получили,теперь нужно ее попробовать удалить из общего списка кнопок


async def main():
    dp.include_router(router=command_router)
    dp.include_router(router=poolbar_router)
    dp.include_router(router=window_router)
    dp.include_router(router=tubing_router)
    dp.include_router(router=categories_router)
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

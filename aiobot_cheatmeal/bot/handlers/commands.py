import datetime
import json

import aiogram.loggers
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, CommandObject

import aiobot_cheatmeal.iiko.apis.cash_day
import aiobot_cheatmeal.iiko.apis.result_report

from aiobot_cheatmeal.bot.keyboards import keyboards
from aiobot_cheatmeal.bot.utils.states import Location
from aiobot_cheatmeal.bot.utils import is_admin
from aiobot_cheatmeal.iiko.apis.URLgenerator import today, yesterday

command_router = Router()


@command_router.message(CommandStart())
async def cmd_start(msg: Message) -> None:
    await msg.answer(f'<b>Привет, {msg.from_user.first_name.capitalize()}</b> 👋')


@command_router.message(Command('sendreportday'))
async def send_report_of_the_day(msg: Message) -> Message:
    aiobot_cheatmeal.iiko.apis.cash_day.getCashDay()
    aiobot_cheatmeal.iiko.apis.result_report.getResultReport()
    # await msg.answer('здесь будет ежедневный отчет')
    with open(
            '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/everyDayReports/' + today + '.json',
            'r', encoding='utf-8') as file:
        stringer = json.load(file)

    await msg.answer(str(stringer)
                     .replace("'", '')
                     .replace(',', '\n')
                     .replace('[', '')
                     .replace(']', '')
                     .replace('\\n', '\n'))
    print('Отчет отправлен в телеграм')


@command_router.message(Command('reports'), is_admin.IsAdmin(is_admin.admin_ids))
async def command_vision(msg: Message, state: FSMContext):
    await msg.answer('Выберите локацию продаж:', reply_markup=keyboards.inline_area_kb)
    await state.set_state(Location.CHOOSE_LOCATION)


@command_router.message(Command('help'))
async def cmd_help(msg: Message) -> None:
    await msg.answer(text='/start - запуск/перезапуск бота')
    await msg.answer(text='/reports - заполнить отчет')
    await msg.answer(text='/sendreportday - отправка ежедневного отчета в чат')
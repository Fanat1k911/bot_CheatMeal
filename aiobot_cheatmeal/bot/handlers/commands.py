import datetime
import json
import logging

import aiogram.loggers
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink
from aiogram.filters import CommandStart, Command, CommandObject
from aiobot_cheatmeal.iiko.functions.all_funcs import getCashDay, getResultReport
from aiobot_cheatmeal.googlesheets.liteFunc import getEmployees

from aiobot_cheatmeal.bot.keyboards import keyboards
from aiobot_cheatmeal.iiko.functions.all_funcs import today, yesterday, clean_logger

command_router = Router()


@command_router.message(CommandStart())
async def cmd_start(msg: Message) -> Message:
    await msg.answer(
        f'<b>Привет, {msg.from_user.first_name.capitalize()}👋</b>' + '\n' +
        f'Я - виртуальный помощник. Я помогаю в некоторых вопросах по части автоматизации')


@command_router.message(Command('staff'))
async def cmd_staff(msg: Message) -> Message:
    logging.info('Запрос на персонал в смене')
    await msg.answer('Сейчас посмотрю ..')
    staff = getEmployees()
    await msg.answer(staff)


@command_router.message(Command('status'))
async def send_report_of_the_day(msg: Message) -> Message:
    logging.info('Выполняем запрос на получение ежедневного отчета ...')
    getCashDay()
    getResultReport()
    # await msg.answer('здесь будет ежедневный отчет')
    with open(
            '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/everyDay/afterProcessing/' + today + '.json',
            mode='r',
            encoding='utf-8') as file:
        stringer = json.load(file)

    await msg.answer(str(stringer)
                     .replace("'", '')
                     .replace(',', '\n')
                     .replace('[', '')
                     .replace(']', '')
                     .replace('\\n', '\n'))
    logging.info('Отчет отправлен в телеграмм')


@command_router.message(Command('help'))
async def cmd_help(msg: Message) -> Message:
    await msg.answer(text='/start - запуск/перезапуск бота')
    await msg.answer(text='/status - отправка ежедневного отчета в чат')


@command_router.message(Command('about'))
async def cmd_about(msg: Message) -> Message:
    text = hlink('Наш сайт', 'https://cheatmealohta.ru/')
    await msg.answer(text=text)

from aiogram import types, fsm, filters, F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from aiobot_cheatmeal.bot.utils.states import Location

fillMain_router = Router()


@fillMain_router.message(Location.HAVE_LOC)
async def question_loc(msg: Message, state: FSMContext):
    await msg.answer('Сегодня работали следующие локации, выберите ту, с которой готовы начать заполнение отчета')

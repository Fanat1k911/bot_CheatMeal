from aiogram import types, fsm, filters, F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from aiobot_cheatmeal.bot.keyboards.keyboards import yes_or_no_kb, category_kb
from aiobot_cheatmeal.bot.utils import is_admin
from aiobot_cheatmeal.bot.utils.states import Location

tubing_router = Router()

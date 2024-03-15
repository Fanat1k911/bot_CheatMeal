from aiogram import types, Router, F, Bot
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from aiobot_cheatmeal.bot.keyboards import keyboards
from aiobot_cheatmeal.bot.utils.states import Location
from aiobot_cheatmeal.bot.data.dictdata import Poolbar, Window, Curds, result_report

categories_router = Router()

categories = {'Products': 'Продукты',
              'Household': 'Хозтовары',
              'RepairHouse': 'Ремонт и содержание помещений',
              'Connection': 'Связь',
              'BuyingTechno': 'Покупка оборудования',
              'RepairTechno': 'Ремонт оборудования',
              'Marketing': 'Маркетинг',
              'TransportCost': 'Транспортные расходы',
              'Tips': 'Чаевые',
              'DeliveryOrder': 'Доставка заказов',
              'Anything': 'Прочие расходы'}

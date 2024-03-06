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


@categories_router.callback_query(F.data.in_(categories), Location.CATEGORY_CHOOSED)
async def fill_wastes(call: CallbackQuery, state: FSMContext):
    await state.set_state(Location.MONEY_WASTES)
    name_category = call.data
    print(f'Были траты на {categories[name_category]}')
    name = categories[name_category]
    Poolbar[name] = 0
    await call.message.answer(f'Введите сумму расходов на категорию "{categories[name_category]}" :')
    await call.answer()
    await call.message.delete_reply_markup()


@categories_router.message(Location.MONEY_WASTES)
async def set_wastes(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        for n in Poolbar.keys():
            if n in categories.values() and Poolbar[n] == 0:
                Poolbar[n] = msg.text
        print(Poolbar.items())
    else:
        await msg.answer('Введите, пожалуйста, только цифры без знаков препинаний и символов')
    await msg.answer('Отлично! Еще были дополнительные расходы?',
                     reply_markup=keyboards.yes_or_no_kb)
    await state.set_state(Location.MORE_WASTES)


@categories_router.message(Location.MORE_WASTES)
async def more_wastes(msg: Message, state: FSMContext):
    if msg.text.lower() == 'да':
        await state.set_state(Location.CATEGORY_CHOOSED)
        await msg.answer('Выберите категорию трат', reply_markup=keyboards.category_kb)
    elif msg.text.lower() == 'нет':
        await state.set_state(Location.SET_DESCRIPTION)
        await msg.answer('Расскажите, как прошел день?')

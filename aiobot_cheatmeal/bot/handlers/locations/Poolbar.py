import pprint

from aiogram import types, fsm, filters, F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from aiobot_cheatmeal.bot.settings.config import TODAY_NOW
from aiobot_cheatmeal.bot.keyboards.keyboards import yes_or_no_kb, category_kb
from aiobot_cheatmeal.bot.utils import is_admin
from aiobot_cheatmeal.bot.utils.states import Location
from aiobot_cheatmeal.bot.data.dictdata import Poolbar, result_report

poolbar_router = Router()


# ПОСЛЕ НАЖАТИЯ НА ОТЧЕТЫ ИЗ ОБЩЕГО МЕНЮ (МОЖЕТ ТОЛЬКО ЧЕЛОВЕК, КОТОРЫЙ В СПИСКЕ "АДМИНОВ")
# НАЧИНАЕМ ЗАПОЛНЯТЬ ОТЧЕТ ПУЛБАРА
@poolbar_router.message(Location.CHOOSE_LOCATION, is_admin.IsAdmin(is_admin.admin_ids))
@poolbar_router.callback_query(F.data == 'poolbar_area')
async def to_poolbar(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await callback.answer('Выбрана локация <ПУЛБАР>')
    await callback.message.answer(f"Введите сумму <b>безналичных</b> оплат:")
    await state.set_state(Location.POOLBAR_CHOOSED)


@poolbar_router.message(Location.POOLBAR_CHOOSED)
@poolbar_router.callback_query(F.data == 'poolbar_area')
async def poolbar_info(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        Poolbar['Отчёт за:'] = TODAY_NOW
        Poolbar['Безналичные'] = msg.text
        await state.set_state(Location.SET_CASH)
        await msg.answer(f'Введите сумму <b>наличных</b> оплат:')
    else:
        await msg.reply('Введите, пожалуйста, сумму цифрами без пробелов и знаков препинаний')


@poolbar_router.message(Location.SET_CASH)
@poolbar_router.callback_query(F.data == 'poolbar_area')
async def poolbar_to_cash(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        await state.set_state(Location.SET_WASTES)
        Poolbar['Наличные'] = msg.text
        await msg.answer('Хорошо! Сегодня были траты наличных?', reply_markup=yes_or_no_kb)
    else:
        await msg.reply('Введите, пожалуйста, сумму цифрами без пробелов и знаков препинаний')


@poolbar_router.message(Location.SET_WASTES)
async def go_wastes(msg: Message, state: FSMContext):
    if msg.text.lower() == 'да':
        await state.set_state(Location.CATEGORY_CHOOSED)
        await msg.answer('Выберите категорию трат:', reply_markup=category_kb)
    elif msg.text.lower() == 'нет':
        Poolbar['Дополнительные расходы'] = 'не было'
        print('Дополнительных расходов не было')
        await msg.answer('Отлично! Опишите, пожалуйста, как прошла смена в свободной форме')
        await state.set_state(Location.SET_DESCRIPTION)


@poolbar_router.message(Location.SET_DESCRIPTION)
async def fill_desc(msg: Message, state: FSMContext):
    Poolbar['Итог по смене:'] = msg.text
    await msg.answer('Спасибо! Кассовая смена закрыта <b>без</b> расхождений по безналичным и наличным платежам?',
                     reply_markup=yes_or_no_kb)
    await state.set_state(Location.VARIANCE)


@poolbar_router.message(Location.VARIANCE)
async def fill_variance(msg: Message, state: FSMContext):
    if msg.text.lower() == 'да':
        Poolbar['Расхождения по кассе'] = 'расхождений нет, касса в норме'
        await msg.answer('В Кассе есть размен?1', reply_markup=yes_or_no_kb)
        await state.set_state(Location.VARIANCE_GOOD)
    elif msg.text.lower() == 'нет':
        await msg.answer('Опишите расхождения по кассе в свободной форме:')
        await state.set_state(Location.VARIANCE_BAD)


@poolbar_router.message(Location.VARIANCE_BAD)
async def fill_variance_bad(msg: Message, state: FSMContext):
    Poolbar['Расхождения по кассе'] = msg.text
    await msg.answer('Ничего страшного, это поправимо, завтра выявим причину')
    await msg.answer('В Кассе есть размен?2', reply_markup=yes_or_no_kb)
    await state.set_state(Location.HALL)


@poolbar_router.message(Location.VARIANCE_GOOD)
async def fill_variance_good_or_bad(msg: Message, state: FSMContext):
    Poolbar['Размен в кассе'] = msg.text
    # print(Poolbar.items())
    await msg.answer('Зал готов к работе следующего дня?', reply_markup=yes_or_no_kb)
    await state.set_state(Location.HALL)


@poolbar_router.message(Location.HALL)
async def fill_hall_cleaning(msg: Message, state: FSMContext):
    if msg.text.lower() == 'да':
        Poolbar['Зал'] = 'готов к работе'
        # print(Poolbar.items())
        await msg.answer('Поставлены ли на зарядку телефон, банковские терминалы, рации?',
                         reply_markup=yes_or_no_kb)
        await state.set_state(Location.BATTARY)
    elif msg.text.lower() == 'нет':
        await msg.answer('Напишите, пожалуйста, в свободной форме что не готово к работе')
        await state.set_state(Location.HALL_BAD)


@poolbar_router.message(Location.HALL_BAD)
async def fill_hall_bad(msg: Message, state: FSMContext):
    Poolbar['Зал'] = msg.text
    print(Poolbar.items())
    await msg.answer('Поставлены ли на зарядку телефон, банковские терминалы, рации?',
                     reply_markup=yes_or_no_kb)
    await state.set_state(Location.BATTARY)


# TODO: в доп расходах категории "прочие" надо указать в свободной форме причину расходов

@poolbar_router.message(Location.BATTARY)
async def fill_battary(msg: Message, state: FSMContext):
    if msg.text.lower() == 'да':
        Poolbar['Техника поставлена на зарядку'] = 'Да'
        await state.set_state(Location.BATTARY_GOOD)
    elif msg.text.lower() == 'нет':
        await msg.answer('Все гаджеты нужно поставить на зарядку!')
        await msg.answer('Поставлены ли на зарядку телефон, банковские терминалы, рации?',
                         reply_markup=yes_or_no_kb)


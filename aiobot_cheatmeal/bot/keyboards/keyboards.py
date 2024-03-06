from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отчеты'),
            KeyboardButton(text='Сотрудники')
        ],
        [
            KeyboardButton(text='Стоп-лист БАР'),
            KeyboardButton(text='Стоп-лист КУХНЯ')
        ]
    ],
    resize_keyboard=True,  # Адаптация размеров клавиатуры под любое устройство
    one_time_keyboard=True,  # Скрывать клавиатуру после первого нажатия на кнопку
    input_field_placeholder='Выберите что-то из меню..',  # Надпись (подсказка) в поле для ввода
    selective=True  # Клавиатура будет активирована только у того, кто ее вызвал
)

# inline main report keyboard
today_report_btn = InlineKeyboardButton(text='Отчет ДНЯ', callback_data='today_report')
week_report_btn = InlineKeyboardButton(text='Отчет НЕДЕЛИ', callback_data='week_report')
month_report_btn = InlineKeyboardButton(text='Отчет МЕСЯЦА', callback_data='month_report')
cancel_btn = InlineKeyboardButton(text='Отменить', callback_data='cancel')

inline_report_kb = InlineKeyboardMarkup(inline_keyboard=[
    [today_report_btn],
    [week_report_btn],
    [month_report_btn],
    [cancel_btn]
])

# inline_kb area-working
poolbar_btn = InlineKeyboardButton(text='Пулбар', callback_data='poolbar_area')
window_btn = InlineKeyboardButton(text='Окошко', callback_data='window_area')
Curd_btn = InlineKeyboardButton(text='Ватрушки', callback_data='curds_area')
show_report_btn = InlineKeyboardButton(text='Посмотреть итоговый отчет', callback_data='show_report')
cancel_btn = InlineKeyboardButton(text='Отменить', callback_data='cancel')

inline_area_kb = InlineKeyboardMarkup(inline_keyboard=[
    [poolbar_btn],
    [window_btn],
    [Curd_btn],
    [show_report_btn],
    [cancel_btn]
])

# Reply_kb yes/no
yes_or_no_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='ДА')],
        [KeyboardButton(text='НЕТ')]
    ], resize_keyboard=True, one_time_keyboard=True, selective=True)

# inline_kb category
Products_Btn = InlineKeyboardButton(text='Продукты', callback_data='Products')
Household_Btn = InlineKeyboardButton(text='Хозтовары', callback_data='Household')
RepairHouse_Btn = InlineKeyboardButton(text='Ремонт и содержание помещений', callback_data='RepairHouse')
Connection_Btn = InlineKeyboardButton(text='Связь', callback_data='Connection')
BuyingTechno_Btn = InlineKeyboardButton(text='Покупка оборудования', callback_data='BuyingTechno')
RepairTechno_Btn = InlineKeyboardButton(text='Ремонт оборудования', callback_data='RepairTechno')
Marketing_Btn = InlineKeyboardButton(text='Маркетинг', callback_data='Marketing')
TransportCost_Btn = InlineKeyboardButton(text='Транспортные расходы', callback_data='TransportCost')
Tips_Btn = InlineKeyboardButton(text='Чаевые', callback_data='Tips')
DeliveryOrder_Btn = InlineKeyboardButton(text='Доставка заказов', callback_data='DeliveryOrder')
Anything_Btn = InlineKeyboardButton(text='Прочие', callback_data='Anything')

category_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [Connection_Btn, Products_Btn, Marketing_Btn],
        [Household_Btn, Tips_Btn, Anything_Btn],
        [DeliveryOrder_Btn],
        [TransportCost_Btn],
        [RepairTechno_Btn],
        [BuyingTechno_Btn],
        [RepairHouse_Btn]
    ])

# keyboards.py
# inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
#
# #bot.py
# @dp.message_handler(commands=['1'])
# async def process_command_1(message: types.Message):
#     await message.reply("Первая инлайн кнопка", reply_markup=kb.inline_kb1)
# ___________
# @dp.callback_query_handler(func=lambda c: c.data == 'button1')
# async def process_callback_button1(callback_query: types.CallbackQuery):
#     await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')

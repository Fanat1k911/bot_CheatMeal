import datetime
import pprint
import time
from typing import List

import gspread
import gspread_formatting as fmt
from gspread import Client, spreadsheet, worksheet, utils
from aiobot_cheatmeal.googlesheets.storage.address import id_keys
from aiobot_cheatmeal.googlesheets.storage.service_files import list_employees
from aiobot_cheatmeal.googlesheets.storage.service_files.dict_days_week import days
from aiobot_cheatmeal.googlesheets.storage.service_files import const_variables, formatting
from aiobot_cheatmeal.iiko.functions.all_funcs import mk_dict_employees_roles
from aiobot_cheatmeal.googlesheets.storage.service_files.decorators import timer

gc = gspread.service_account(
    '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/'
    'googlesheets/storage/service_files/service_account.json')

global merge_list_2_cells


@timer
def getEmployees():
    listEmployees = []
    strEmp = ''
    day = gc.open_by_key(id_keys.IdTabelCM_Ohta).get_worksheet_by_id(871969104).get('A1:A2')
    poolbar = gc.open_by_key(id_keys.IdTabelCM_Ohta).get_worksheet_by_id(871969104).get('B1:b9')
    kitchen = gc.open_by_key(id_keys.IdTabelCM_Ohta).get_worksheet_by_id(871969104).get('c1:c9')
    # toobing = gc.open_by_key(id_keys.IdTabelCM_Ohta).get_worksheet_by_id(871969104).get('d1:d9')
    listEmployees.append(day)
    listEmployees.append(poolbar)
    listEmployees.append(kitchen)
    # listEmployees.append(toobing)
    for step1 in listEmployees:
        strEmp += '\n'
        for step2 in step1:
            for step3 in step2:
                strEmp += step3 + '\n'
    return strEmp


@timer
def insert_col(spreadsheetId, idList: int, startIndex, endIndex):
    sht = gc.open_by_key(spreadsheetId)
    requests = []
    requests.append({
        "insertDimension": {
            "range": {
                "sheetId": idList,
                "dimension": "COLUMNS",
                "startIndex": startIndex,  # где начать вносить пустые столбцы
                "endIndex": endIndex  # где закончить вносить пустые столбцы
            },
            # "inheritFromBefore": True
        }
    })

    body = {
        'requests': requests
    }
    sht.batch_update(body)


@timer
def insert_rows_for_percent(spreadsheet_key: str, sheet_name: str):
    # берем строки с персоналом пулбара,
    # сохр их в переменную а потом вставляем их с 19 строки (строки должны быть созданы в таблице)
    sheet = gc.open_by_key(spreadsheet_key).worksheet(sheet_name)
    percent_list = sheet.get_all_values()
    row = 0
    for lst in percent_list:
        if lst[0] == 'КУХНЯ':
            break
        row += 1
    selected_data = percent_list[0:row]
    print(len(selected_data))
    # определение последней строки в таблице
    lr = sheet.row_count

    # Вставка подтаблички "Процент" с ФИ сотрудников и профессией
    sheet.append_rows(selected_data, table_range=f'A{lr + 3}')

    # Вставка названия подтаблички "Процент"
    sheet.update([['Процент']], range_name=f'A{lr + 2}')
    sheet.insert_row(['Табель'], index=1)

    #####################################################################
    # ищем первое число месяца в подтаблице "процент"
    start_month_day = sheet.findall('1')
    # ищем последнее число месяца в подтаблице "процент"
    end_month_day = sheet.findall(str(const_variables.DAYS_COUNT_OF_MONTH[const_variables.NEXT_MONTH]))

    # множественное присвоение параметров строк и стобцов, найденного методом поиска
    start_row, start_col = start_month_day[-1].row + 1, start_month_day[-1].col
    end_row, end_col = end_month_day[-1].row + 7, end_month_day[-1].col

    start_index = utils.rowcol_to_a1(start_row, start_col)
    end_index = utils.rowcol_to_a1(end_row, end_col)

    print(start_index, end_index)
    cell_values = sheet.range(f'{start_index}:{end_index}')
    lst_helper = []
    f1st_col = start_month_day[-1].col

    for col in range(len(selected_data) - 1):  # cols
        for row in range(const_variables.DAYS_COUNT_OF_MONTH[const_variables.NEXT_MONTH] + 2):  # rows
            lst_helper.append(
                (f'=IF(NOT(ISBLANK({utils.rowcol_to_a1(f1st_col + col, 3 + row)}));'
                 f'INDIRECT("\'кудир апрель бар\'!$C$"&VALUE({utils.rowcol_to_a1(3, 3 + row)}))'
                 f'*IFERROR({utils.rowcol_to_a1(f1st_col + col, 3 + row)}/'
                 f'(SUM({utils.rowcol_to_a1(f1st_col, 3 + row)}:{utils.rowcol_to_a1(9, 3 + row)})));)'))

    for item in range(len(cell_values)):
        cell_values[item].value = lst_helper[item]

    sheet.update_cells(cell_list=cell_values, value_input_option="USER_ENTERED")
    #####################################################################

    sheet.update(
        values=[[f'=sum(C{i}:Q{i})'] for i in range(22, 29)],
        range_name='S22:S28',
        raw=False
    )
    sheet.update(
        values=[[f'=sum(T{i}:AI{i})'] for i in range(22, 29)],
        range_name=f'{utils.rowcol_to_a1(end_row - 6, end_col + 2)}:{utils.rowcol_to_a1(end_row, end_col + 2)}',
        raw=False
    )
    sheet.update(
        values=[[f'=sum(S{i};AK{i})'] for i in range(22, 29)],
        range_name=f'{utils.rowcol_to_a1(end_row - 6, end_col + 3)}:{utils.rowcol_to_a1(end_row, end_col + 3)}',
        raw=False
    )


@timer
def search_list_in_sh(key: str, worksheet_title: worksheet):
    """
    Функция осуществляет по названия листа name_worksheet в книге spreadsheet
    :param spreadsheet: Книга
    :param name_worksheet: Название листа
    :return: True или False в зависимости от наличия листа в таблице
    """
    flag = False
    gs = gc.open_by_key(key=key)
    for name in gs.worksheets():
        if worksheet_title in str(name):
            flag = True
            break
    return flag


@timer
def get_listdays_of_month(numberOfMonth: int) -> list:
    if numberOfMonth in const_variables.DAYS_COUNT_OF_MONTH.keys():
        lst = [x for x in range(1, const_variables.DAYS_COUNT_OF_MONTH.get(numberOfMonth, 'hz') + 1)]
        return lst


@timer
def getday_of_week_to_rus(month):
    """
    Получает сегодняшнюю дату, берет первое число следующего месяца
     и делает запрос на получение значения у ключа в роли которого
     выступает дата первого числа следующего месяца и с помощью
     генератора создает список, куда заносит все дни до конца месяца
    :param day:today
    :return: list
    """
    list_weekdays = []
    current_year = datetime.date.today().year
    next_month = month + 1
    weekday_num = datetime.date(current_year, next_month, 1).weekday()
    list_days = get_listdays_of_month(next_month)
    for i in range(1, len(list_days) + 1):
        list_weekdays.append(days.get(datetime.date(current_year, next_month, i).weekday(), 'hz'))
    return list_weekdays


@timer
def if_list_created():
    # для тестов удалим таблицу перед запуском функции
    lsParsing = gc.open_by_key(id_keys.IdParsing)
    today = datetime.datetime.today()
    month_year_title = datetime.datetime(year=const_variables.CURRENT_YEAR,
                                         month=const_variables.NEXT_MONTH,
                                         day=1).strftime('%B %y')

    if search_list_in_sh(id_keys.IdParsing, month_year_title) is True:
        idByList = lsParsing.worksheet(month_year_title).id
        print(f'Лист "{month_year_title}" найден. Индекс: {lsParsing.get_worksheet_by_id(idByList).index}')
        lsParsing.del_worksheet_by_id(idByList)
        print(f'Лист "{month_year_title}" удален. Пауза 3 sec')
        time.sleep(2)
    else:
        print(f'Лист {month_year_title} не найден')


# if_list_created()

@timer
def mk_new_sheet_month():
    # сократим название переменных
    C_YEAR = const_variables.CURRENT_YEAR
    N_MTH = const_variables.NEXT_MONTH
    lsParsing = gc.open_by_key(id_keys.IdParsing)

    month_year_title = (datetime.datetime
                        (year=C_YEAR,
                         month=N_MTH,
                         day=1).strftime('%B %y'))

    # удалим лист, если создан
    if_list_created()

    # сохраняем в переменной флаг: создана таблица или нет вызывая для этого функцию поиска листа
    created = search_list_in_sh(id_keys.IdParsing, month_year_title)

    # число последнего дня месяца
    edom = get_listdays_of_month(N_MTH)[-1]

    if const_variables.TODAY.day > 1 and created is False:
        print(month_year_title, 'Пора создать таблицу на следующий месяц, этот уже близится к завершению!')
        # создаем лист с название текущего месяца
        lsParsing.add_worksheet(title=month_year_title, rows=10, cols=5, index=0)

        # сохраним путь к листу в переменную
        lsParsing_title_month = lsParsing.worksheet(month_year_title)

        # получаем id листа
        idByList = lsParsing.worksheet(month_year_title).id

        # устанавливаем буквенное сокращение дня недели
        lsParsing.worksheet(month_year_title).insert_row(get_listdays_of_month(N_MTH))

        # вставляем строку с числами месяца
        lsParsing.worksheet(month_year_title).insert_row(getday_of_week_to_rus(N_MTH - 1))

        # вставляем столбцы по индексу от startIndex до endIndex по id листа
        insert_col(id_keys.IdParsing, idByList, 0, 2)

        # заполняем 2 столбца с ФИ и должностью
        lsParsing.worksheet(month_year_title).batch_update([
            {
                'range': 'A2',
                'values': mk_dict_employees_roles()[0],
            },
            {
                'range': 'B2',
                'values': mk_dict_employees_roles()[1],
            },
            {
                'range': 'A' + str(len(mk_dict_employees_roles()[0]) + 2),
                'values': mk_dict_employees_roles()[2],
            },
            {
                'range': 'B' + str(len(mk_dict_employees_roles()[1]) + 2),
                'values': mk_dict_employees_roles()[3],
            },
        ])

        # Промежуточное автовыравнивание
        lsParsing_title_month.columns_auto_resize(0, len(lsParsing_title_month.row_values(1)))

        # Вставка дополнительных столбцов с промежуточными подсчетами
        lsParsing_title_month.insert_cols([['Доп. часы'], ['Итого часов 1-15']], 18)

        # Вставка результирующих столбцов с подсчетами
        lsParsing_title_month.insert_cols(
            [[f'Доп. часы 16-{edom}'],
             [f'Итого часов 16-{edom}'],
             [f'Итого часов 1-{edom}'],
             ['Доп. доход + комментарий'],
             ['Доп. расход + комментарий']],
            col=len(lsParsing_title_month.row_values(1)) + 1,
            inherit_from_before=True)

        lsParsing_title_month.columns_auto_resize(0, len(lsParsing_title_month.row_values(1)))

        # находим адрес ячейки совпадения с текстом для
        address_result_second_half_month = lsParsing_title_month.find(f'Итого часов 16-{edom}').address

        # Добавим таблицу "процент"
        insert_rows_for_percent(id_keys.IdParsing, month_year_title)

        # lsParsing.worksheet(month_year_title).merge_cells('A1:A2')
        # lsParsing.worksheet(month_year_title).merge_cells('B1:B2')
        # lsParsing.worksheet(month_year_title).merge_cells('R1:R2')
        # lsParsing.worksheet(month_year_title).merge_cells('AH1:AH2')
        # lsParsing.worksheet(month_year_title).merge_cells('AI1:AI2')
        # lsParsing.worksheet(month_year_title).merge_cells('AJ1:AJ2')
        # lsParsing.worksheet(month_year_title).merge_cells('AK1:AK2')
        # lsParsing.worksheet(month_year_title).merge_cells('AL1:AL2')

        # Вставка формул
        lsParsing_title_month.update(
            values=[[f'=sum(C{i}:R{i})'] if i != 10 else [''] for i in range(3, 18)],
            range_name='S3:S17',
            raw=False
        )
        lsParsing_title_month.update(
            values=[[f'=sum(T{i}:AI{i})'] if i != 10 else [''] for i in range(3, 18)],
            range_name='AK3:AK17',
            raw=False
        )
        lsParsing_title_month.update(
            values=[[f'=sum(S{i};AK{i})'] if i != 10 else [''] for i in range(3, 18)],
            range_name='AL3:AL17',
            raw=False
        )
        print('Закончил создание')

        # Форматирование
        # lc = lsParsing.worksheet(month_year_title).column_count
        # lr = lsParsing.worksheet(month_year_title).row_count
        # lsParsing.worksheet(month_year_title).format(ranges='1:2', format=formatting.format_a1_a2_cell)
        # lsParsing.worksheet(month_year_title).format(
        #     ranges=['A1:B', 'R1', 'AH1', 'AI1', 'AJ1', 'AK1', 'AL1'],
        #     format=formatting.format_center)
        # lsParsing.worksheet(month_year_title).format(
        #     ranges=['A1:A', 'B1:B', 'R1:R', 'AH1:AH2', 'AI1:AI2', 'AJ1:AJ2', 'AK1:AK2'],
        #     format=formatting.format_center_middle)
        # lsParsing.worksheet(month_year_title).format(
        #     ranges=['A2:A17', 'B2:B17'],
        #     format=formatting.format_OVERFLOW_CELL)
        # lsParsing.worksheet(month_year_title).format(
        #     ranges=['A11', 'B11'],
        #     format={'textFormat': {'bold': True}})
        # lsParsing.worksheet(month_year_title).format(
        #     ranges=['A1:AL10', 'A12:AL17', 'A22:AL31'],
        #     format=formatting.cell_border_format)
        #
        # # Автовыравнивание
        # lsParsing.worksheet(month_year_title).columns_auto_resize(0, lc)
        # lsParsing.worksheet(month_year_title).rows_auto_resize(0, lr)
        #
        # # Ручное выравнивание
        # # Выравниваем ширину столбцов
        # fmt.set_row_height(lsParsing.worksheet(month_year_title), '1', 30)
        # fmt.set_column_width(lsParsing.worksheet(month_year_title), 'R', 46)
        # fmt.set_column_width(lsParsing.worksheet(month_year_title), 'AH', 50)
        # fmt.set_column_width(lsParsing.worksheet(month_year_title), 'AI', 40)
        # fmt.set_column_width(lsParsing.worksheet(month_year_title), 'AJ', 96)
        # fmt.set_column_width(lsParsing.worksheet(month_year_title), 'AK', 100)
        # fmt.set_column_width(lsParsing.worksheet(month_year_title), 'AL', 50)
        #
        # # Завершение
        # print('Закончил форматирование')
    else:
        print(f"Лист с названием '{month_year_title}' уже создан либо 25 еще не наступило!")


mk_new_sheet_month()


def testformatting():
    parsing_sh = gc.open_by_key(id_keys.IdParsing)
    parsing_table = gc.open_by_key(id_keys.IdParsing).worksheet('May 24')
    # N_MTH = const_variables.NEXT_MONTH
    merge_list_2_cells = ['A1:A2', 'B1:B2', 'R1:R2', 'S1:S2', 'AJ1:AJ2']
    for couple in merge_list_2_cells:
        parsing_table.merge_cells(name=couple, merge_type='merge_columns')
    # TODO: вставить значение в ячейку как формулу
    # value_input_option='USER_ENTERED'
    #  raw=False
    # for cell in range(1, 11):
    #     save_format = fmt.get_user_entered_format(parsing_table, f'A{cell}')
    #     fmt.format_cell_range(parsing_table, f'A{cell + 18}', save_format)
    #     print(f'done for A{cell}')

# testformatting()

# если таблица не создана - создаем таблицу размером 5х5 по индексу 0
#
#
#
#
#
#
#
#

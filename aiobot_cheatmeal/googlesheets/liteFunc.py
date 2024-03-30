import datetime
import pprint
import time

import gspread
import gspread_formatting as fmt
from gspread import Client, spreadsheet, worksheet
from aiobot_cheatmeal.googlesheets.storage.address import id_keys
from aiobot_cheatmeal.googlesheets.storage.service_files import list_employees
from aiobot_cheatmeal.googlesheets.storage.service_files.dict_days_week import days
from aiobot_cheatmeal.googlesheets.storage.service_files import const_variables, formatting

gc = gspread.service_account(
    '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/'
    'googlesheets/storage/service_files/service_account.json')


def getEmployees():
    listEmployees = []
    strEmp = ''
    day = gc.open_by_key(id_keys.IdTabelCM_Ohta).get_worksheet_by_id(871969104).get('A1:A2')
    poolbar = gc.open_by_key(id_keys.IdTabelCM_Ohta).get_worksheet_by_id(871969104).get('B1:b9')
    kitchen = gc.open_by_key(id_keys.IdTabelCM_Ohta).get_worksheet_by_id(871969104).get('c1:c9')
    toobing = gc.open_by_key(id_keys.IdTabelCM_Ohta).get_worksheet_by_id(871969104).get('d1:d9')
    listEmployees.append(day)
    listEmployees.append(poolbar)
    listEmployees.append(kitchen)
    listEmployees.append(toobing)
    for step1 in listEmployees:
        strEmp += '\n'
        for step2 in step1:
            for step3 in step2:
                strEmp += step3 + '\n'
    return strEmp


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
    lr = sheet.row_count
    sheet.append_rows(selected_data, table_range=f'A{lr + 5}')


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


def get_listdays_of_month(numberOfMonth: int) -> list:
    # days_count_of_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30,
    #                        12: 31}  # не весокосный год
    if numberOfMonth in const_variables.DAYS_COUNT_OF_MONTH.keys():
        lst = [x for x in range(1, const_variables.DAYS_COUNT_OF_MONTH.get(numberOfMonth, 'hz') + 1)]
        return lst


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
        time.sleep(3)
    else:
        print(f'{month_year_title} не найден')


# if_list_created()


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

    # сохраняем в переменной флаг: создана таблица или нет вызывая для этого функцию
    created = search_list_in_sh(id_keys.IdParsing, month_year_title)

    # число последнего дня месяца
    end_day_of_month = get_listdays_of_month(N_MTH)[-1]

    # Кол-во списков в списке с сотрудниками

    if const_variables.TODAY.day > 15 and created is False:
        print(month_year_title, 'Пора создать таблицу на следующий месяц, этот уже близится к завершению!')
        lsParsing.add_worksheet(title=month_year_title, rows=11, cols=5, index=0)
        idByList = lsParsing.worksheet(month_year_title).id
        lsParsing.worksheet(month_year_title).insert_row(get_listdays_of_month(N_MTH))
        lsParsing.worksheet(month_year_title).insert_row(getday_of_week_to_rus(N_MTH - 1))
        insert_col(id_keys.IdParsing, idByList, 0, 2)
        lsParsing.worksheet(month_year_title).batch_update([
            {
                'range': 'A2',
                'values': [i[0] for i in list_employees.employees[0]],
            },
            {
                'range': 'A11',
                'values': [j[0] for j in list_employees.employees[1]],
            },
            {
                'range': 'B2',
                'values': [i[0][1] for i in list_employees.employees[0]]
            },
            {
                'range': 'B11',
                'values': [j[1] for j in list_employees.employees[1]]
            },
        ])
        insert_col(id_keys.IdParsing, idByList, 17, 18)
        lsParsing.worksheet(month_year_title).add_cols(5)
        lsParsing.worksheet(month_year_title).update([['Итого часов 1-15']], 'R1')
        lsParsing.worksheet(month_year_title).update([[f'Итого часов 16-{end_day_of_month}']], 'AH1')
        lsParsing.worksheet(month_year_title).update([['Доп. часы']], 'AI1')
        lsParsing.worksheet(month_year_title).update([['Доп. доход + комментарий']], 'AJ1')
        lsParsing.worksheet(month_year_title).update([['Доп. расход + комментарий']], 'AK1')
        lsParsing.worksheet(month_year_title).update([['Итого часов за месяц']], 'AL1')
        lsParsing.worksheet(month_year_title).merge_cells('A1:A2')
        lsParsing.worksheet(month_year_title).merge_cells('B1:B2')
        lsParsing.worksheet(month_year_title).merge_cells('R1:R2')
        lsParsing.worksheet(month_year_title).merge_cells('AH1:AH2')
        lsParsing.worksheet(month_year_title).merge_cells('AI1:AI2')
        lsParsing.worksheet(month_year_title).merge_cells('AJ1:AJ2')
        lsParsing.worksheet(month_year_title).merge_cells('AK1:AK2')
        lsParsing.worksheet(month_year_title).merge_cells('AL1:AL2')
        # Вставка формул
        lsParsing.worksheet(month_year_title).update(
            values=[[f'=sum(C{i}:Q{i})'] if i != 11 and i != 18 else [''] for i in range(3, 18)],
            range_name='R3:R17',
            raw=False)
        print('Закончил создание')

        # Добавим таблицу "процент"
        insert_rows_for_percent(id_keys.IdParsing, 'April 24')

        # Форматирование
        lc = lsParsing.worksheet(month_year_title).column_count
        lr = lsParsing.worksheet(month_year_title).row_count
        lsParsing.worksheet(month_year_title).format(ranges='1:2', format=formatting.format_a1_a2_cell)
        lsParsing.worksheet(month_year_title).format(
            ranges=['A1:B', 'R1', 'AH1', 'AI1', 'AJ1', 'AK1', 'AL1'],
            format=formatting.format_center)
        lsParsing.worksheet(month_year_title).format(
            ranges=['A1:A', 'B1:B', 'R1:R', 'AH1:AH2', 'AI1:AI2', 'AJ1:AJ2', 'AK1:AK2'],
            format=formatting.format_center_middle)
        lsParsing.worksheet(month_year_title).format(
            ranges=['A2:A17', 'B2:B17'],
            format=formatting.format_OVERFLOW_CELL)
        lsParsing.worksheet(month_year_title).format(
            ranges=['A11', 'B11'],
            format={'textFormat': {'bold': True}})
        lsParsing.worksheet(month_year_title).format(
            ranges=['A1:AL10', 'A12:AL17', 'A22:AL31'],
            format=formatting.cell_border_format)

        # Автовыравнивание
        lsParsing.worksheet(month_year_title).columns_auto_resize(0, lc)
        lsParsing.worksheet(month_year_title).rows_auto_resize(0, lr)

        # Ручное выравнивание
        # Выравниваем ширину столбцов
        fmt.set_row_height(lsParsing.worksheet(month_year_title), '1', 30)
        fmt.set_column_width(lsParsing.worksheet(month_year_title), 'R', 46)
        fmt.set_column_width(lsParsing.worksheet(month_year_title), 'AH', 50)
        fmt.set_column_width(lsParsing.worksheet(month_year_title), 'AI', 40)
        fmt.set_column_width(lsParsing.worksheet(month_year_title), 'AJ', 96)
        fmt.set_column_width(lsParsing.worksheet(month_year_title), 'AK', 100)
        fmt.set_column_width(lsParsing.worksheet(month_year_title), 'AL', 50)

        # Завершение
        print('Закончил форматирование')
    else:
        print(f"Лист с названием '{month_year_title}' уже создан либо 25 еще не наступило!")


mk_new_sheet_month()


def testformatting():
    parsing_table = gc.open_by_key(id_keys.IdParsing).worksheet('April 24')
    # formating = fmt.get_user_entered_format(parsing_table, 'A1')
    print(parsing_table.get_values(range_name='1:2'))
    # print(formating)
    # percent_before = parsing_table.get_all_values(range_name='1:10')
    # percent_after = parsing_table.get_all_values(range_name='19:28')

    # TODO: вставить значение в ячейку как формулу
    # value_input_option='USER_ENTERED'
    #  raw=False
    # for cell in range(1, 11):
    #     save_format = fmt.get_user_entered_format(parsing_table, f'A{cell}')
    #     fmt.format_cell_range(parsing_table, f'A{cell + 18}', save_format)
    #     print(f'done for A{cell}')

# testformatting()

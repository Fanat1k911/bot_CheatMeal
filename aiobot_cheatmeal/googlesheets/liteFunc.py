import datetime

import gspread
from gspread import Client, spreadsheet, worksheet
from aiobot_cheatmeal.googlesheets.storage.address import id_keys
from aiobot_cheatmeal.googlesheets.storage.service_files import list_employees

gc = gspread.service_account(
    '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/googlesheets/storage/service_files/service_account.json')


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


def search_list_in_sh(key: str, name_worksheet: worksheet):
    """
    Функция осуществляет по названия листа name_worksheet в книге spreadsheet
    :param spreadsheet: Книга
    :param name_worksheet: Название листа
    :return: True или False в зависимости от наличия листа в таблице
    """
    flag = False
    gs = gc.open_by_key(key=key)
    for name in gs.worksheets():
        if name_worksheet in str(name):
            flag = True
    return flag


def get_listdays_of_month(numberOfMonth: int) -> list:
    days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}  # не весокосный год
    if numberOfMonth in days.keys():
        lst = [x for x in range(1, days.get(numberOfMonth, 'hz') + 1)]
        return lst

def getday_of_week_to_rus(day):
    pass
# get_listdays_of_month(2)


def mk_new_sheet_month():
    lsParsing = gc.open_by_key(id_keys.IdParsing)
    today = datetime.datetime.today()
    month = today.month
    month_year_title = today.date().strftime('%B %y')
    created = search_list_in_sh(id_keys.IdParsing, month_year_title)
    if today.day > 15 and created is False:
        print(month_year_title, 'на сегодня уже больше 15 числа!')
        lsParsing.add_worksheet(title=month_year_title, rows=5, cols=5, index=0)
        idByList = lsParsing.worksheet(month_year_title).id
        lsParsing.worksheet(month_year_title).insert_row(get_listdays_of_month(3))
        insert_col(id_keys.IdParsing, idByList, 0, 2)
        lsParsing.worksheet(month_year_title).batch_update([
            {
                'range': 'A2',
                'values': list_employees.list_names
            }, {
                'range': 'B2',
                'values': list_employees.list_skills
            }])
        lc = lsParsing.worksheet(month_year_title).column_count
        lsParsing.worksheet(month_year_title).columns_auto_resize(0, lc)
    else:
        print(f"Лист с названием '{month_year_title}' уже создан либо 25 еще не наступило!")
        print(today.month)


mk_new_sheet_month()


def mk_rows_cols_for_new_sh_of_month(list_days: list) -> tuple:
    endmonth = int(str(list_days[-1]).replace('[', '').replace(']', ''))
    cols = 2 + 15 + int(abs(16 - endmonth)) + 4
    print(cols)

# mk_rows_cols_for_new_sh_of_month(get_listdays_of_month(2))
# кол-во "cols" в таблице:
# 2 столца до нумерации дней месяца,
# 1 столбец промежуточный (итог 1-15),
# 4 столбца после нумерации дней месяца,
# итого столбцов: 2+15+1+[16:endmonth]+4 = 37 столбцов (актуально для марта)

import datetime
import requests
import json
import os
from xml.etree import ElementTree
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

today = str(datetime.date.today())  # формат даты  "2024-01-19" / "ГГГГ-ММ-ДД"
yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
totime = datetime.datetime.today()  # формат "2024-01-19 22:45:49.529225"
today_for_department_url = str(datetime.date.today().strftime('%d.%m.%Y'))  # формат '18.02.2024' / 'ДД.ММ.ГГГГ'
yerstoday_for_department_url = datetime.date.today() - datetime.timedelta(days=1)  # формат '17.02.2024' / 'ДД.ММ.ГГГГ'
yerstoday_for_department_url = str(yerstoday_for_department_url.strftime('%d.%m.%Y'))
# print(today, totime.strftime('%d/%m/%Y'))

id_department_tubing = '52f6b2d9-58ec-4f87-bcb0-934178916e76'
id_department_poolbar = '19589761-94fa-141d-017e-573be2660011'

url_new_token = 'https://cheat-meal-co.iiko.it:443/resto/api/auth?login=admin2&pass=' + os.getenv('HASH_PASSWORD')
token = requests.get(url_new_token).text
url_cash_today = (
        'https://cheat-meal-co.iiko.it:443/resto/api/v2/cashshifts/list?status=ANY&openDateFrom=' +
        today + '&openDateTo=' + today + '&key=' + token)
url_get_products_day = (
        'https://cheat-meal-co.iiko.it:443/resto/api/reports/productExpense?key=' + token +
        '&department=52f6b2d9-58ec-4f87-bcb0-934178916e76&dateFrom=' + today_for_department_url +
        '&dateTo=' + today_for_department_url + '&hourFrom=10&hourTo=23#326ca6; text-decoration: none')


def getManById(idMan, token):
    url_get_by_id = 'https://cheat-meal-co.iiko.it:443/resto/api/employees/byId/' + idMan + '?key=' + token
    resp = requests.get(url_get_by_id).text
    with open('/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/' + idMan + '.xml',
              'w', encoding='utf-8') as xFile:
        xFile.write(resp)
    tree = ElementTree.parse(
        '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/' + idMan + '.xml')
    root = tree.getroot()
    return root[2].text


def getProductsOfDepartment(id_department, token):
    url_get_products_day = (
            'https://cheat-meal-co.iiko.it:443/resto/api/reports/productExpense?key=' + token +
            '&department=' + id_department + '&dateFrom=' + today_for_department_url +
            '&dateTo=' + today_for_department_url + '&hourFrom=11&hourTo=23#326ca6; text-decoration: none')
    resp = requests.get(url_get_products_day).text
    with open(
            '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/everyDay/ProductConsumption/' + id_department + '.xml',
            'w', encoding='utf-8') as ProdFile:
        ProdFile.write(resp)
    # TODO: выкорчевать из словаря нужные элементы!
    # tree = ElementTree.parse(
    #     '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/everyDay/ProductConsumption/' + id_department + '.xml')
    # root = tree.getroot()
    # for i in (root[0].items()):
    #     print(i)
    size_file = (os.path.getsize(
        '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/'))
    print('Размер файла: ', size_file / 1000, 'kB')


# TODO: здесь будет функция получения списка продаж для выявления кол-ва чеков и среднего
def getSalesList(token):
    """
    Получает список продаж для подсчета кол-ва чеков на локации
    :return: кортеж из: Кол-во чеков Пулбара, Кол-во чеков Ватрушек
    """
    url_get_sales = ('https://cheat-meal-co.iiko.it:443/resto/api/reports/olap?'
                     'key=' + token +
                     '&report=SALES'
                     '&from=' + today_for_department_url +
                     '&to=' + today_for_department_url +
                     '&groupRow=Department'
                     '&groupRow=OpenTime'
                     '&groupRow=UniqOrderId'
                     '&agr=fullSum'
                     '&agr=DishDiscountSumInt.average'
                     '&groupRow=DiscountPercent')
    responce = requests.get(url_get_sales).text
    with open(
            '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/everyDay/sales/'
            + today_for_department_url + '.xml',
            'w', encoding='utf-8') as file:
        file.write(responce)
    tree = ElementTree.parse(
        '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/everyDay/sales/'
        + today_for_department_url + '.xml')
    root = tree.getroot()
    # TODO: дерево получили, надо посчитать кол-во заказов методом подбора по названию
    # TODO: можно считать одну локацию, а потом из общего кол-ва вычесть и получить кол-во другой локации
    toobingOrders = 0
    poolbarOrders = 0
    outOrdersPoolbar = 0
    outOrdersToobing = 0
    resultOrdersPoolbar = 0
    resultOrdersToobing = 0
    for i in range(len(root)):
        if root[i][1].text == 'CHEAT MEAL. Vatrushki':
            toobingOrders += 1
            if root[i][4].text == '1.0000':
                outOrdersToobing += 1
        elif root[i][1].text == 'Cheat meal!':
            poolbarOrders += 1
            if root[i][4].text == '1.0000':
                outOrdersPoolbar += 1
    resultOrdersPoolbar = poolbarOrders - outOrdersPoolbar
    resultOrdersToobing = toobingOrders - outOrdersToobing
    # print('toobing >>>', outOrdersToobing, toobingOrders, resultOrdersToobing)
    # print('poolbar >>>', outOrdersPoolbar, poolbarOrders, resultOrdersPoolbar)
    return resultOrdersPoolbar, resultOrdersToobing


# getSalesList(token=token)
# print(getSalesList(token=token))
getProductsOfDepartment(id_department_poolbar, token=token)
# getManagerById(token)

# https://cheat-meal-co.iiko.it:443/resto/api/employees/byId/cd6dc22c-2267-4921-9121-0d8c8d113c9b?key=2cff9be6-f545-7ad0-0361-6c7cacd2de7e
# print(token)
# print(today)

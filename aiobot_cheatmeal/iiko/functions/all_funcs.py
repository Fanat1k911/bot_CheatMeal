import datetime
import os
import time
import math
from xml.etree import ElementTree

import requests
import json
from dotenv import load_dotenv, find_dotenv
import logging

load_dotenv(find_dotenv())

today = str(datetime.date.today())  # формат даты  "2024-01-19" / "ГГГГ-ММ-ДД"
yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
totime = datetime.datetime.today()  # формат "2024-01-19 22:45:49.529225"
today_for_department_url = str(datetime.date.today().strftime('%d.%m.%Y'))  # формат '18.02.2024' / 'ДД.ММ.ГГГГ'
yerstoday_for_department_url = datetime.date.today() - datetime.timedelta(days=1)  # формат '17.02.2024' / 'ДД.ММ.ГГГГ'
yerstoday_for_department_url = str(yerstoday_for_department_url.strftime('%d.%m.%Y'))

logging.basicConfig(
    filename='/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/logging/logging.log',
    level=logging.INFO)

id_department_tubing = '52f6b2d9-58ec-4f87-bcb0-934178916e76'
id_department_poolbar = '19589761-94fa-141d-017e-573be2660011'


def getNewToken():
    """
    Получает новый TOKEN для отправки запроов на сервер iiko
    :return: token
    """
    logging
    url_new_token = 'https://cheat-meal-co.iiko.it:443/resto/api/auth?login=admin2&pass=' + os.getenv('HASH_PASSWORD')
    token = requests.get(url_new_token).text
    logging.info(f'New iiko token : {token}')
    return token


def getCashDay():
    """
    Получает отчет из iiko для дальнейшей обработки
    :return: Сохраненный отчет в формате json
    """
    token = getNewToken()
    url_cash_today = (
            'https://cheat-meal-co.iiko.it:443/resto/api/v2/cashshifts/list?status=ANY&openDateFrom=' + today +
            '&openDateTo=' + today +
            '&key=' + token)

    logging.info(f'Status code :  {requests.get(url_cash_today).status_code}')
    data_collecting = False
    flagFalse = 0

    while data_collecting is False:
        with open(
                '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/'
                'everyDay/beforeProcessing/' + today + '.json',
                'w', encoding='utf-8') as file:
            response = requests.get(url_cash_today)
            if response.status_code == 200:
                try:
                    data = requests.get(url_cash_today).json()
                    dataj = json.dumps(data, indent=2)
                    file.write(dataj)
                    logging.info('Отчет успешно получен с сервера iiko')
                    data_collecting = True
                except:
                    logging.info(f'Попытка не удалась, STATUS_CODE = {response.status_code}')
                    time.sleep(5)
                    flagFalse += 1
                    if flagFalse == 5:
                        data_collecting = True
                        logging.info(f'Проверьте импорты. '
                                     'Попробуйте еще раз запросить отчет. '
                                     'Нужен перезапуск приложения')
                        break
            else:
                logging.info(f'Статус-код другой: {response.status_code}, Пауза 5 секунд..')
                time.sleep(5)
                flagFalse += 1
                if flagFalse == 5:
                    data_collecting = True
                    logging.info(f'Попробуйте еще раз запросить отчет. Нужен перезапуск приложения')
                    break


def getResultReport():
    daynow = datetime.datetime.today().strftime('%d.%m.%Y')

    dict_day = {}
    list_day = []
    end_day = []
    all_summ = 0
    all_bn = 0
    all_cash = 0

    with open(
            '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/everyDay/beforeProcessing/' +
            today + '.json', 'r',
            encoding='utf-8') as file:
        data_json = file.read()
        result = json.loads(data_json)

    for step in range(0, len(result)):
        dict_day['Локация'] = result[step]['pointOfSaleId']
        dict_day['Рабочий день № '] = result[step]['sessionNumber']
        dict_day['Смена открыта'] = result[step]['openDate']
        dict_day['Смена закрыта'] = result[step]['closeDate']
        dict_day['Общая выручка'] = result[step]['payOrders']
        all_summ += result[step]['payOrders']
        dict_day['Б/н'] = result[step]['salesCard']
        all_bn += result[step]['salesCard']
        dict_day['Наличные'] = result[step]['salesCash']
        all_cash += result[step]['salesCash']

        # TODO: как вариант передавать в качестве аргумента в функцию название локации и возвращать нужное знаение
        # ниже будет вызываться функция для получения данных по id из файла xml
        idMan = result[step]['managerId']
        nameManager = getManById(idMan, token=getNewToken())
        dict_day['Кассир'] = nameManager
        if step == len(result) - 1:
            end_day.append('Общая выручка: ' + str(all_summ))
            end_day.append('Наличные за смену: ' + str(all_cash))

        poolbarOrders = str(getSalesList(token=getNewToken())[0])
        toobingOrders = str(getSalesList(token=getNewToken())[1])

        # собираем отчет
        for item in dict_day.keys():
            if dict_day[item] == '430adbeb-2e88-4d5b-8102-8b28e8cdcacc':
                list_day.append(str(item) + ': ' + 'Ватрушки')
                list_day.append('Всего чеков: ' + toobingOrders)
                if toobingOrders != 0 and int(result[step]['payOrders']) != 0:
                    list_day.append(
                        'Средний чек: ' + str(math.trunc(int(result[step]['payOrders']) / int(toobingOrders))))
                continue
            if dict_day[item] == '1631ec4d-17b8-4ee2-bd00-521016feb192':
                list_day.append(str(item) + ': ' + 'Пулбар')
                list_day.append('Всего чеков: ' + poolbarOrders)
                if poolbarOrders != 0 and int(result[step]['payOrders']) != 0:
                    list_day.append(
                        'Средний чек: ' + str(math.trunc(int(result[step]['payOrders']) / int(poolbarOrders))))
                continue
            if str(item) == 'Смена открыта' or str(item) == 'Смена закрыта':
                if dict_day[item] != None:
                    list_day.append(str(item) + ': ' + str(dict_day[item][11:19]))
                else:
                    list_day.append(str(item) + ': ' + 'СМЕНА НЕ ЗАКРЫТА')
            else:
                list_day.append(str(item) + ': ' + str(dict_day[item]))
    logging.info('Отчет сформирован')
    list_day.insert(0, daynow)
    for i in range(len(end_day)):
        list_day.insert(i + 1, end_day[i])
        if i == len(end_day) - 1:
            list_day.insert(1, '\n')
            list_day.insert(4, '\n')
            list_day.insert(15, '\n')
    # Запись готового отчета в отдельный файл json
    with open(
            '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/everyDay/afterProcessing/' +
            today + '.json',
            'wt+', encoding='UTF-8') as report:
        json.dump(list_day, report, ensure_ascii=False)
    logging.info('Отчет сохранен в отдельный файл')


def getManById(idMan, token):
    token = getNewToken()
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
    token = getNewToken()
    url_get_products_day = (
            'https://cheat-meal-co.iiko.it:443/resto/api/reports/productExpense?key=' + token +
            '&department=' + id_department + '&dateFrom=' + today_for_department_url +
            '&dateTo=' + today_for_department_url + '&hourFrom=11&hourTo=23#326ca6; text-decoration: none')
    resp = requests.get(url_get_products_day).text
    with open(
            '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/everyDay'
            '/ProductConsumption/' + id_department + '.xml',
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
    print('Размер дирректории хранилища: ', size_file / 1000, 'kB')


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
            "/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/"
            "everyDay/sales/"
            + today_for_department_url + '.xml',
            'w', encoding='utf-8') as file:
        file.write(responce)
    tree = ElementTree.parse(
        '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/'
        'everyDay/sales/'
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


def getEmployes():
    """
    Копирует из таблицы ФИ сотрудников на текущий день и отправляет в телеграм-чат Бара
    :return: Список сотрудников
    """

import datetime
import json
import math

import requests
import time
from pprint import pprint

from aiobot_cheatmeal.iiko.apis.URLgenerator import url_new_token, url_cash_today, today, token, getManById, \
    getSalesList


def getResultReport():
    daynow = datetime.datetime.today().strftime('%d.%m.%Y')

    dict_day = {}
    list_day = []
    end_day = []
    all_summ = 0
    all_bn = 0
    all_cash = 0

    with open('/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/' + today + '.json', 'r',
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

        # TODO:  здесь будет добавлено в словарь кол-во чеков по нужной локации. Переделать функцию получения для
        # TODO: каждого подразделения (нужен идентификатор/триггер подразделения)
        # TODO: как вариант разделить на вызов функций при совпадении ватрушек или пулбара
        # TODO: как вариант передавать в качестве аргумента в функцию название локации и возвращать нужное знаение
        # ниже будет вызываться функция для получения данных по id из файла xml
        idMan = result[step]['managerId']
        nameManager = getManById(idMan, token)
        dict_day['Кассир'] = nameManager
        if step == len(result) - 1:
            end_day.append('Общая выручка: ' + str(all_summ))
            # end_day.append('Итого Б/н:' + str(all_bn))
            end_day.append('Наличные за смену: ' + str(all_cash))

        poolbarOrders = str(getSalesList(token=token)[0])
        toobingOrders = str(getSalesList(token=token)[1])

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
    print('Отчет сформирован')
    list_day.insert(0, daynow)
    for i in range(len(end_day)):
        list_day.insert(i + 1, end_day[i])
        if i == len(end_day) - 1:
            list_day.insert(1, '\n')
            list_day.insert(4, '\n')
            list_day.insert(15, '\n')
    # Запись готового отчета в отдельный файл json
    with open(
            '/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/everyDayReports/' + today + '.json',
            'w', encoding='UTF-8') as report:
        json.dump(list_day, report, ensure_ascii=False)
    print('Отчет сохранен в отдельный файл')

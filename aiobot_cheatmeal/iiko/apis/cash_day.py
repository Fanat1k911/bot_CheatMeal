from requests import Response
from aiobot_cheatmeal.iiko.apis.URLgenerator import url_new_token, url_cash_today, today
import json
import requests
import time


def getCashDay():
    # print(requests.get(url_cash_today).status_code)
    data_collecting = False
    flagFalse = 0
    while data_collecting is False:
        with open('/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/' + today + '.json',
                  'w', encoding='utf-8') as file:
            response = requests.get(url_cash_today)
            if response.status_code == 200:
                try:
                    data = requests.get(url_cash_today).json()
                    dataj = json.dumps(data, indent=2)
                    file.write(dataj)
                    print('Отчет успешно получен из iiko')
                    data_collecting = True
                    # файл сохранен, с ним можно работать и вытаскивать нужные данные
                except:
                    print('Попытка не удалась, STATUS_CODE =', response.status_code)
            else:
                print('Статус-код другой:', response.status_code, 'Пауза 5 секунд..')
                time.sleep(5)
                flagFalse += 1
                if flagFalse == 5:
                    data_collecting = True
                    print('Попробуйте еще раз запросить отчет. Нужен перезапуск приложения')
                    break
    # TODO: можно вести логи с указанием времени и происходящими операциями

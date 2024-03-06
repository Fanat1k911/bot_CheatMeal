import json
import datetime
import requests
from aiobot_cheatmeal.iiko.apis.URLgenerator import token
import xml.etree.ElementTree as ET

url_get_by_id = 'https://cheat-meal-co.iiko.it:443/resto/api/employees/byId/cd6dc22c-2267-4921-9121-0d8c8d113c9b?key=' + token

global idsManager
with open('/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/cash_today.json', 'r+',
          encoding='utf-8') as file:
    idsManager = []
    for line in file.readlines():
        if 'id' in (json.dumps(line.split()[0])):
            # print(line.split('"')[3])
            idManager = str(line.split('"')[3])
            idsManager.append(idManager)
    print(idsManager)

with open('/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/idsManagrs.xml', 'a+',
          encoding='utf-8') as ids:
    for i in idsManager:
        data = requests.get(url_get_by_id).text
        ids.writelines(data)
        print()

tree = ET.parse('/Users/a12345/PycharmProjects/bot_CheatMeal/aiobot_cheatmeal/iiko/apis/storage/report.xml')
root = tree.getroot()
for i in root.items():
    print(i)
for elem in root.iter():
    print(elem.tag['para'], 'atttributs =>', elem.attrib)

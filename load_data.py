 #
 # Copyright (c) 2023 Cuerpo de Bomberos de Valparaíso.
 #
 # This program is free software: you can redistribute it and/or modify
 # it under the terms of the GNU General Public License as published by
 # the Free Software Foundation, version 3.
 #
 # This program is distributed in the hope that it will be useful, but
 # WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 # General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 #

import requests
import json
import re
from bs4 import BeautifulSoup

# HTML TO JSON
def html_to_json(content, indent=None):
    soup = BeautifulSoup(content, "html.parser")
    rows = soup.find("tbody").find_all("tr")
    headers = {}
    thead = soup.find("thead")
    if thead:
        thead = thead.find_all("th")
        for i in range(len(thead)):
            headers[i] = thead[i].text.strip().lower()
    data = []
    for row in rows:
        cells = row.find_all(["th", "td"])
        if thead:
            items = {}
            for index in headers:
                items[headers[index]] = cells[index].text
        else:
            items = []
            for index in cells:
                items.append(index.text.strip())
        data.append(items)
    return data

# Header
print(open('./rsc/header.txt', 'r').read())

# Code
BASE_URL = "http://resumen.cbv.cl"
EMERGENCY_ENDPOINT = BASE_URL + "/logic/logic_public.php?type=1"
UNITS_ENDPOINT = BASE_URL + "/logic/logic_public.php?type=4"
listObj = []
lastId = 1
error = 0

# Read existing json and load last id if exist
try:
    listObj = json.loads(open("./result.json", "r").read())
    lastId = int(listObj[-1]["id"]) + 1
except:
    listObj = []


# Formatter and Tab Header
formatter = "{:<7} {:<23} {:<7} {:<7} {:<55} {:<40}"
print(formatter.format("id", "Fecha", "Clave", "Error", "Dirección", "Unidades"))

# Load date and print as tab
while True:
    data = {'id_emer':lastId}
    rEmergency = requests.post(url = EMERGENCY_ENDPOINT, data = data)
    rUnits = requests.post(url = UNITS_ENDPOINT, data = data)
    try:
        emergency = rEmergency.json()["data"]
    except:
        break
    if emergency == "" or rUnits.text == "":
        error = error + 1
        lastId = lastId + 1
        if error > 888:
            break
    else:
        units = html_to_json(rUnits.text)
        delimiter = "  "
        for unit in units:
            my_str = unit["registro del recurso"]
            result = ['{}{}'.format(delimiter, s) for s in my_str.split(delimiter) if s]
            unit["registro del recurso"] = result
        emergency["units"] = units
        listObj.append(emergency)
        uniades = ", ".join(d['recurso'] for d in emergency["units"])
        print(formatter.format(emergency["id"], emergency["fech"], emergency["sigla"], error, emergency["dir"], uniades))
        lastId = lastId + 1
        with open("./result.json", 'w') as file:
            json.dump(listObj, file, indent=4, separators=(',',': '))

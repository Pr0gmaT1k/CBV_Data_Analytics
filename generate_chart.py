import json
from os import path
import os
import shutil
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
import calendar
from calendar import month_name
from collections import Counter
from matplotlib.figure import Figure
from alive_progress import alive_bar
import functools
import operator
import locale

# CONSTANT
font = {'fontname':'Helvetica'}
dateFormatter = '%d/%m/%Y - %H:%M:%S'
chartsPath = "./Charts/"
compagnys = { 0: "CBV", 1: "Primera", 2: "Segunda", 3: "Tercera", 4: "Cuarta", 5: "Quinta", 6: "Sexta", 7: "Séptima", 8: "Octava", 9: "Novena", 10: "Décima", 11: "Undécima", 12: "Duodécima", 13: "Decimotercera", 14: "Decimocuarta", 15: "Decimoquinta", 16: "DecimoSexta" }
colors1 = {
'1': '#ff361d','1-1': '#ff663f', '1-2': '#ff875a', '1-3': '#ffa473',
'2': '#8d2c00', '2-1': '#c45a00', '2-2': '#f88b36', '2-3': '#ffae58',
'3': '#951e51', '3-1': '#ae3967', '3-2': '#c8527d',
'4': '#9da900', '4-1': '#bcc500', '4-2': '#dbe201',
'5': '#00a6a8', '5-1': '#00c3c4', '5-2': '#00e1e1',
'6': '#004dec', '6-1': '#2067ff', '6-2': '#5c7fff', '6-3': '#8098ff', '6-4': '#9fb0ff', '6-5': '#bdc9ff',
'7': '#be0074',
'8': '#f72ca6',
'9': '#901332', '9-1': '#a93145', '9-2': '#c3495a', '9-3': '#de6170',
'10': '#3c6b0e',
'11': '#56852b',
'12': '#71a045',
'13': '#8dbc5f',
'14': '#a9d979',
'15': '#003e4f',
'16': '#5dc4d7',
'default': '#023863'
}

colors = ['#00876c', '#379469', '#58a066', '#78ab63', '#98b561', '#b8bf62', '#dac767', '#deb256', '#e09d4b', '#e18745', '#e06f45', '#dc574a', '#d43d51']

# CONTAINER
listObj = []
days = []
hours = []

# FUNCS
def generatePie(company, month, year):
   # Filter
    unitRange = company * 10
    companyThsEmergencys = [b for b in listObj if ([c for c in b['units'] if (c['unidad'] == str(unitRange + 1) or c['unidad'] == str(unitRange + 2) or c['unidad'] == str(unitRange + 3))])] if company != 0 else listObj
    if not companyThsEmergencys: return
    companyThsEmergencysDate = []
    if year == 0:
        companyThsEmergencysDate = [b for b in companyThsEmergencys if (datetime.strptime(b['fech'], dateFormatter).year >= 2017)]
    elif month == 0:
        companyThsEmergencysDate = [b for b in companyThsEmergencys if (datetime.strptime(b['fech'], dateFormatter).year == year)]
    else:
        companyThsEmergencysDate = [b for b in companyThsEmergencys if (datetime.strptime(b['fech'], dateFormatter).year == year) and (datetime.strptime(b['fech'], dateFormatter).month == month)]
    if not companyThsEmergencysDate: return
    counted = Counter([dic['sigla'] for dic in companyThsEmergencysDate])

    # Count
    join = 0
    filtered = dict([c for c in counted.items() if c[1] <= join])
    key = ", ".join(filtered.keys())
    if len(key) > 18:
        a = key[:len(key)//2]
        b = key[len(key)//2:]
        b = b.replace(', ', ',\n', 1)
        key = a + b
    joined = (key, sum(filtered.values()))
    counted = [a for a in counted.items() if a[1] > join]
    if join != 0:
        counted.append(joined)
    counted = dict(sorted(Counter(counted), key = lambda i: i[1]))
    labels = [(a[0] + ": " + str(a[1])) for a in counted.items()]
    pie2Colors = { a: colors1[a] if a in [*colors1] else colors1['default'] for a in [*counted] }.values()

    # Build chart
    monthTitleStr = "{monthStrr}".format(monthStrr=calendar.month_name[month]) if (month != 0) else ""
    yearStrr = " {y}".format(y=str(year)) if year != 0 else "Desde 2017"

    # First Ring (outside)
    fig, ax = plt.subplots()
    ax.axis('equal')
    print(counted.items())
    ousideData = dict(functools.reduce(operator.add, map(collections.Counter, my_dict)))[{k.split("-")[0]: v} for k,v in counted.items()]
    print(ousideData)
    mypie, _ = ax.pie(counted.values(), labels = labels, radius=1, colors = pie2Colors, textprops={'fontsize': 10})
    plt.setp(mypie, width=0.1, edgecolor='white')

    # Second Ring (Inside)
    mypie2, _ = ax.pie(counted.values(), labels = labels, radius=1-0.1, labeldistance=0.6, colors = pie2Colors, textprops={'fontsize': 8})
    plt.setp(mypie2, width=0.4, edgecolor='white')
    plt.margins(0,0)

    # Title
    plt.title("{companyStr} {monthTitle}{yearStr}: {len} despachos".format(companyStr=compagnys[company], monthTitle=monthTitleStr, yearStr=yearStrr, len=len(companyThsEmergencysDate)), **font)

    # Save chart
    yearPath = "{path}/".format(path=str(year)) if year != 0 else ""
    try: os.makedirs("{path}{companyInt}_{companyStr}/{yearP}".format(path=chartsPath, yearP=yearPath, companyInt=company, companyStr=compagnys[company]))
    except: pass
    yearStrr = "-{y}".format(y=str(year)) if year != 0 else "_Desde_2017"
    fileName = "{companyStr2}{yearStr}.png".format(companyStr2=compagnys[company], yearStr=yearStrr) if month == 0 else "{monthNum}_{companyStr2}-{montName}{yearStr}.png".format(monthNum=month, companyStr2=compagnys[company], montName=calendar.month_name[month], yearStr=yearStrr)
    plt.savefig("{path}{companyInt}_{companyStr}/{yearP}{fileN}".format(path=chartsPath, yearP=yearPath, companyInt=company, companyStr=compagnys[company], fileN=fileName), dpi=300)
    plt.close()

try:
    # Header
    print(open('./rsc/header.txt', 'r').read())
    # Remove old charts if exist
    if path.exists(chartsPath): shutil.rmtree(chartsPath)
    # Set locale for calendar in ES
    locale.setlocale(locale.LC_ALL, 'es_ES')
    # Read existing json and load last id if exist
    listObj = json.loads(open("./result.json", "r").read())
    # Generate
    with alive_bar(1 * (((date.today().year - 2017) * 13) + (date.today().month + 1)) + 1, title='Conteo y tipos de llamados por compañia') as bar:
        generatePie(0,0,0)
        bar()
        #for company in range (0, (15 + 1)):
            #generatePie(company,0,0)
        for year in range (2017, (date.today().year + 1)):
            for month in range (0, 12 + 1):
                if year == date.today().year and month == date.today().month + 1: break
                generatePie(8, month, year)
                bar()

except: pass


#for emergency in listObj:
#    date = datetime.strptime(emergency['fech'], dateFormatter)
#    hours.append(date.hour)
#    days.append(date.weekday())

#emergencyForDays = dict(sorted(Counter(days).items(),key = lambda i: i[0]))

#plt.bar(list(emergencyForDays.keys()), emergencyForDays.values(), color='g')
#plt.title("llamados por dias de la semana desde 2016")
#plt.show()

#emergencyForHour = dict(sorted(Counter(hours).items(),key = lambda i: i[0]))

#plt.bar(list(emergencyForHour.keys()), emergencyForHour.values(), color='r')
#plt.title("llamados por horas del dia desde 2016")
#plt.xticks(list(emergencyForHour.keys()))
#plt.show()

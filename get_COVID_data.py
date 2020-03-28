import requests
import pandas as pd
import datetime
import json

url = 'https://lab.isaaclin.cn/nCoV/api/area'
r = requests.request('GET', url)

data = r.json()
data = data['results']


china_data = []
country_data =[]

for result in data:
    if result['cities'] == None:
        country_data.append(result)
    else:
        china_data.append(result)

china_dict = {}
country_dict = {}

china_dict['data'] = china_data
country_dict['data'] = country_data


fname_country = 'COVID-country-' + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + '.json'
fname_china = 'COVID-china-' + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + '.json'

with open(fname_country,'w',encoding='utf-8') as f:
    json.dump(country_dict,f,ensure_ascii=False,indent = 4)
    print("save country data done!")

with open(fname_china,'w',encoding='utf-8') as f:
    json.dump(china_dict,f,ensure_ascii=False,indent = 4)
    print("save china data done!")

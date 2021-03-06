import requests
import time
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


fname_country = '../DingXiang-COVID-data/COVID-country-data/' + 'COVID-country-' \
                + str(time.strftime('%Y-%m-%d', time.localtime(time.time()))) + '.json'
fname_china = '../DingXiang-COVID-data/COVID-china-data/' + 'COVID-china-' \
              + str(time.strftime('%Y-%m-%d', time.localtime(time.time()))) + '.json'

with open(fname_country,'w',encoding='utf-8') as f:
    json.dump(country_dict,f,ensure_ascii=False,indent = 4)
    print("save country data done!")

with open(fname_china,'w',encoding='utf-8') as f:
    json.dump(china_dict,f,ensure_ascii=False,indent = 4)
    print("save china data done!")

import requests
import json

user_password = {"username": "zilliz", "password": "123456"}

# login
respond = requests.post(url='http://microsoft1:9999/login', json=user_password)
Token = respond.json()['data']['token']
print(respond.json())

headers = {'Content-Type': 'application/json', 'Authorization': 'Token %s' % Token}

# load data
json_file = "./COVID-china.json"
with open(json_file, 'r') as f:
    data_json = json.load(f)
respond = requests.post(url='http://microsoft1:9999/load', json=data_json, headers=headers)


#
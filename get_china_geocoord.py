#!-*- coding:UTF-8 -*-
import json
import requests

my_api_key = "d93cf23be9f207f17d4bfe48619f386d"

geo_coord_result = {}
with open("COVID-china-330.json", "r") as json_file:
    data = json.load(json_file)["data"]
    for i in range(len(data)):
        province_data = data[i]
        cities = data[i]["cities"]
        for j in range(len(cities)):
            city_data = cities[j]
            city_name = city_data["cityName"]
            url = "https://restapi.amap.com/v3/geocode/geo?key=" + my_api_key + "&address=" + city_name
            result = requests.request('GET', url)
            result = result.json()
            if result["status"] == '0' or result["count"] == '0':
                longitude = "null"
                latitude = "null"
            else:
                longitude = result["geocodes"][0]["location"].split(",")[0]
                latitude = result["geocodes"][0]["location"].split(",")[1]
            geo_coord_result[city_name] = [longitude, latitude]

with open("./china_geo_coord.json", "w") as f:
    json.dump(geo_coord_result, f, indent=4, sort_keys=True)

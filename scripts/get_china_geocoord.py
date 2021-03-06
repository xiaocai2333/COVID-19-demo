#!-*- coding:UTF-8 -*-
import json
import requests

my_api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"


def get_city_geo_coord():
    geo_coord_result = {}
    with open("../DingXiang-COVID-data/COVID-china-data/COVID-china-2020-04-09.json", "r") as json_file:
        data = json.load(json_file)["data"]
        for i in range(len(data)):
            province_data = data[i]
            province_name = province_data["provinceEnglishName"]
            cities = data[i]["cities"]
            for j in range(len(cities)):
                city_data = cities[j]
                city_name = city_data["cityName"]
                url = "https://restapi.amap.com/v3/geocode/geo?key=" + my_api_key + "&address=" + city_name
                result = requests.request('GET', url)
                result = result.json()
                if result["status"] == '0' or result["count"] == '0':
                    continue
                else:
                    longitude = result["geocodes"][0]["location"].split(",")[0]
                    latitude = result["geocodes"][0]["location"].split(",")[1]
                    latitude = result["geocodes"][0]["location"].split(",")[1]
                geo_coord_result[city_name] = [longitude, latitude]

    with open("../geo_coord/china_city_geo_coord.json", "w", encoding='utf-8') as f:
        json.dump(geo_coord_result, f, ensure_ascii=False, indent=4, sort_keys=True)


def get_province_geo_coord():
    geo_coord_result = {}
    with open("../DingXiang-COVID-data/COVID-china-data/COVID-china-2020-04-09.json", "r") as json_file:
        data = json.load(json_file)["data"]
        for i in range(len(data)):
            province_data = data[i]
            province_chinese_name = province_data["provinceName"]
            url = "https://restapi.amap.com/v3/geocode/geo?key=" + my_api_key + "&address=" + province_chinese_name
            result = requests.request('GET', url)
            result = result.json()
            if result["status"] == '0' or result["count"] == '0':
                continue
            else:
                longitude = result["geocodes"][0]["location"].split(",")[0]
                latitude = result["geocodes"][0]["location"].split(",")[1]
            geo_coord_result[province_chinese_name] = [longitude, latitude]

    with open("../geo_coord/china_province_geo_coord.json", "w", encoding='utf-8') as f:
        json.dump(geo_coord_result, f, ensure_ascii=False, indent=4, sort_keys=True)


if __name__ == "__main__":
    get_city_geo_coord()
    get_province_geo_coord()

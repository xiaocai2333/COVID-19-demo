import csv
import datetime
import json
import requests
import time
import os
import sys

my_api_key = "d93cf23be9f207f17d4bfe48619f386d"


def convert_json_to_csv_china(input_file, writer):
    fp_city = open("./china_city_geo_coord.json", "r")
    fp_province = open("./china_province_geo_coord.json", "r")
    china_city_geo_coord = json.load(fp_city)
    china_province_geo_coord = json.load(fp_province)
    with open(input_file, "r") as json_file:
        data = json.load(json_file)["data"]
        for i in range(len(data)):
            province_data = data[i]
            continent = province_data["continentEnglishName"]
            country = province_data["countryEnglishName"]
            province = province_data["provinceEnglishName"]
            province_location_id = province_data["locationId"]
            province_current_confirmed_count = province_data["currentConfirmedCount"]
            province_confirmed_count = province_data["confirmedCount"]
            province_suspected_count = province_data["suspectedCount"]
            province_cured_count = province_data["curedCount"]
            province_dead_count = province_data["deadCount"]
            local_time = time.localtime(province_data["updateTime"] / 1000.0)
            update_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            cities = data[i]["cities"]

            if len(cities) == 0:
                city_name = "null"
                city_location_id = "null"
                city_current_confirmed_count = "null"
                city_confirmed_count = "null"
                city_suspected_count = "null"
                city_cured_count = "null"
                city_dead_count = "null"
                if province in china_province_geo_coord:
                    longitude = china_province_geo_coord[province][0]
                    latitude = china_province_geo_coord[province][1]
                else:
                    url = "https://restapi.amap.com/v3/geocode/geo?key=" + my_api_key + "&address=" + province
                    result = requests.request('GET', url)
                    result = result.json()
                    if result["status"] == '0' or result["count"] == '0':
                        with open("./null_geo_coord_china_city.csv", "a+") as f:
                            f.writelines(province)
                        continue
                    else:
                        longitude = result["geocodes"][0]["location"].split(",")[0]
                        latitude = result["geocodes"][0]["location"].split(",")[1]
                row = [continent, country, province, province_location_id, province_current_confirmed_count,
                       province_confirmed_count, province_suspected_count, province_cured_count, province_dead_count,
                       city_name, longitude, latitude, city_location_id, city_current_confirmed_count,
                       city_confirmed_count, city_suspected_count, city_cured_count, city_dead_count, update_time]

                writer.writerow(row)
            else:
                for j in range(len(cities)):
                    city_data = cities[j]
                    city_name = city_data["cityName"]
                    if city_name in china_city_geo_coord:
                        longitude = china_city_geo_coord[city_name][0]
                        latitude = china_city_geo_coord[city_name][1]
                    else:
                        url = "https://restapi.amap.com/v3/geocode/geo?key=" + my_api_key + "&address=" + city_name
                        result = requests.request('GET', url)
                        result = result.json()
                        if result["status"] == '0' or result["count"] == '0':
                            with open("./null_geo_coord_china_city.csv", "a+") as f:
                                f.writelines(city_name)
                            continue
                        else:
                            longitude = result["geocodes"][0]["location"].split(",")[0]
                            latitude = result["geocodes"][0]["location"].split(",")[1]
                    city_location_id = city_data["locationId"]
                    city_current_confirmed_count = city_data["currentConfirmedCount"]
                    city_confirmed_count = city_data["confirmedCount"]
                    city_suspected_count = city_data["suspectedCount"]
                    city_cured_count = city_data["curedCount"]
                    city_dead_count = city_data["deadCount"]
                    row = [continent, country, province, province_location_id, province_current_confirmed_count,
                           province_confirmed_count, province_suspected_count, province_cured_count,
                           province_dead_count, city_name, longitude, latitude, city_location_id,
                           city_current_confirmed_count, city_confirmed_count, city_suspected_count,
                           city_cured_count, city_dead_count, update_time]
                    writer.writerow(row)

    print("convert china data done!")


def convert_json_to_csv_country(input_file, writer):
    fp = open("./country_geo_coord.json", "r")
    geo_file = json.load(fp)

    with open(input_file, "r") as json_file:
        data = json.load(json_file)["data"]
        for i in range(len(data)):
            province_data = data[i]
            continent = province_data["continentEnglishName"]
            country = province_data["countryEnglishName"]
            location_id = province_data["locationId"]
            current_confirmed_count = province_data["currentConfirmedCount"]
            confirmed_count = province_data["confirmedCount"]
            suspected_count = province_data["suspectedCount"]
            cured_count = province_data["curedCount"]
            dead_count = province_data["deadCount"]
            local_time = time.localtime(province_data["updateTime"] / 1000.0)
            update_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            if country in geo_file:
                longitude = geo_file[country][0]
                latitude = geo_file[country][1]
            else:
                with open("./null_geo_coord_china_city.csv", "a+") as f:
                    f.writelines(country)
                continue

            row = [continent, country, location_id, longitude, latitude, current_confirmed_count, confirmed_count,
                   suspected_count, cured_count, dead_count, update_time]
            writer.writerow(row)

    print("convert country data done!")


if __name__ == "__main__":
    opt = sys.argv[-1]
    if opt == '-r':
        rewrite = True
    else:
        rewrite = False

    china_data_path = "./DingXiang-COVID-data/COVID-china-data/"
    country_data_path = "./DingXiang-COVID-data/COVID-country-data/"

    if rewrite:
        china_file_list = os.listdir(china_data_path)
        country_file_list = os.listdir(country_data_path)
        china_output_file = "./COVID-china-data.csv"
        country_output_file = "./COVID-country-data.csv"

        china_schema = ["continent", "country", "province", "provinceLocationId", "provinceCurrentConfirmedCount",
                        "provinceConfirmedCount", "provinceSuspectedCount", "provinceCuredCount", "provinceDeadCount",
                        "cityName", "longitude", "latitude", "cityLocationId", "cityCurrentConfirmedCount",
                        "cityConfirmedCount", "citySuspectedCount", "cityCuredCount", "cityDeadCount", "updateTime"]
        china_fp = open(china_output_file, "w+")
        china_writer = csv.writer()
        china_writer.writerow(china_schema)

        country_schema = ["continent", "country", "locationId", "longitude", "latitude", "currentConfirmedCount",
                          "confirmedCount", "suspectedCount", "curedCount", "deadCount", "updateTime"]
        country_fp = open(country_output_file, "w+")
        country_writer = csv.writer(country_fp)
        country_writer.writerow(country_schema)

        for china_file in china_file_list:
            convert_json_to_csv_china(china_data_path + china_file, china_writer)
        for country_file in country_file_list:
            convert_json_to_csv_country(country_data_path + country_file, country_writer)

        china_fp.close()
        country_fp.close()
    else:
        china_output_file = "./COVID-china-data.csv"
        country_output_file = "./COVID-country-data.csv"
        china_file = 'COVID-china-' + str(time.strftime('%Y-%m-%d', time.localtime(time.time()))) + '.json'
        country_file = 'COVID-country-' + str(time.strftime('%Y-%m-%d', time.localtime(time.time()))) + '.json'

        china_fp = open(china_output_file, "a+")
        country_fp = open(country_output_file, "a+")
        china_writer = csv.writer(china_fp)
        country_writer = csv.writer(country_fp)
        convert_json_to_csv_china(china_data_path + china_file, china_writer)
        convert_json_to_csv_country(country_data_path + country_file, country_writer)

        china_fp.close()
        country_fp.close()


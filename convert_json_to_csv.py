import csv
import datetime
import json
import requests

my_api_key = "XXXXXXXXXXXXXXXXXX"
def convert_json_to_csv_china(input_file, output_file):
    schema = ["continent", "country", "province", "provinceLocationId", "provinceCurrentConfirmedCount",
              "provinceConfirmedCount", "provinceSuspectedCount", "provinceCuredCount", "provinceDeadCount", "cityName",
              "longitude", "latitude", "cityLocationId", "cityCurrentConfirmedCount", "cityConfirmedCount",
              "citySuspectedCount", "cityCuredCount", "cityDeadCount", "updateTime"]
    csv_file = open(output_file, "w+")
    writer = csv.writer(csv_file)
    writer.writerow(schema)

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
            update_time = province_data["updateTime"]
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
                city_location_id = city_data["locationId"]
                city_current_confirmed_count = city_data["currentConfirmedCount"]
                city_confirmed_count = city_data["confirmedCount"]
                city_suspected_count = city_data["suspectedCount"]
                city_cured_count = city_data["curedCount"]
                city_dead_count = city_data["deadCount"]
                row = [continent, country, province, province_location_id, province_current_confirmed_count,
                       province_confirmed_count, province_suspected_count, province_cured_count, province_dead_count,
                       city_name, longitude, latitude, city_location_id, city_current_confirmed_count,
                       city_confirmed_count, city_suspected_count, city_cured_count, city_dead_count, update_time]
                writer.writerow(row)

    csv_file.close()
    print("convert china data done!")


def convert_json_to_csv_country(input_file, output_file):
    schema = ["continent", "country", "locationId", "longitude", "latitude", "currentConfirmedCount", "confirmedCount",
              "suspectedCount", "curedCount", "deadCount", "updateTime"]
    csv_file = open(output_file, "w+")
    writer = csv.writer(csv_file)
    writer.writerow(schema)

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
            update_time = province_data["updateTime"]
            if country in geo_file:
                longitude = geo_file[country][1]
                latitude = geo_file[country][0]
            else:
                longitude = "null"
                latitude = "null"

            row = [continent, country, location_id, longitude, latitude, current_confirmed_count, confirmed_count, suspected_count,
                   cured_count, dead_count, update_time]
            writer.writerow(row)

    csv_file.close()
    print("convert country data done!")


if __name__ == "__main__":
    country_json = 'COVID-country-' + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + '.json'
    china_json = 'COVID-china-' + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + '.json'
    country_csv = 'COVID-country-' + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + '.csv'
    china_csv = 'COVID-china-' + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + '.csv'

    convert_json_to_csv_china(china_json, china_csv)
    convert_json_to_csv_country(country_json, country_csv)


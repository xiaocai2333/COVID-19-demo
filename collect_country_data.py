import csv
import datetime
import json
import math
import pandas as pd
import os
import sys
import time


def convert_str_to_time(string):
    month_s, day_s, year_s = string.split("/")
    year_s, time_s = year_s.split(" ")
    hour_s, minute_s = time_s.split(":")
    second_s = "00"
    if year_s == "20":
        year_s = "2020"
    time_str = str(year_s) + "-" + str(month_s) + "-" + str(day_s) \
               + " " + str(hour_s) + ":" + str(minute_s) + ":" + str(second_s)
    res_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

    return res_time


def collect_row_data_1(input_file, csv_writer, is_time_valid):
    china_geo_coord_file = open("./china_province_geo_coord.json", "r")
    china_geo_coord = json.load(china_geo_coord_file)
    country_geo_coord_file = open("./country_geo_coord.json", "r")
    country_geo_coord = json.load(country_geo_coord_file)
    csv_df = pd.read_csv(input_file)
    for line_num in range(len(csv_df)):
        province = csv_df["Province/State"][line_num]
        if csv_df["Country/Region"][line_num] in ["Mainland China", "Hong Kong", "Taiwan", "Macau"]:
            country = "China"
        else:
            country = csv_df["Country/Region"][line_num]
        if str(province) == "nan":
            province = country
        if province in china_geo_coord:
            longitude = china_geo_coord[province][0]
            latitude = china_geo_coord[province][1]
        elif country in country_geo_coord:
            longitude = country_geo_coord[country][0]
            latitude = country_geo_coord[country][1]
        else:
            with open("./null_geo_coord_country.csv", "a+") as f:
                country_row = country + "," + province
                f.writelines(country_row + "\n")
            continue
        confirmed_count = csv_df["Confirmed"][line_num]
        if math.isnan(confirmed_count):
            confirmed_count = 0
        dead_count = csv_df["Deaths"][line_num]
        if math.isnan(dead_count):
            dead_count = 0
        cured_count = csv_df["Recovered"][line_num]
        if math.isnan(cured_count):
            cured_count = 0
        if not is_time_valid:
            last_update_time = convert_str_to_time(csv_df["Last Update"][line_num])
        else:
            last_update_time = csv_df["Last Update"][line_num].replace("T", " ")

        result_row = [country, province, longitude, latitude, confirmed_count,
                      dead_count, cured_count, last_update_time]
        csv_writer.writerow(result_row)

    china_geo_coord_file.close()
    country_geo_coord_file.close()


def collect_row_data_2(input_file, csv_writer):
    csv_df = pd.read_csv(input_file)
    for line_num in range(len(csv_df)):
        province = csv_df["Province/State"][line_num]
        if csv_df["Country/Region"][line_num] in ["Mainland China", "Hong Kong", "Taiwan", "Macau"]:
            country = "China"
        else:
            country = csv_df["Country/Region"][line_num]
        if str(province) == "nan":
            province = country
        longitude = csv_df["Longitude"][line_num]
        latitude = csv_df["Latitude"][line_num]
        confirmed_count = csv_df["Confirmed"][line_num]
        if math.isnan(confirmed_count):
            confirmed_count = 0
        dead_count = csv_df["Deaths"][line_num]
        if math.isnan(dead_count):
            dead_count = 0
        cured_count = csv_df["Recovered"][line_num]
        if math.isnan(cured_count):
            cured_count = 0
        last_update_time = csv_df["Last Update"][line_num].replace("T", " ")

        result_row = [country, province, longitude, latitude, confirmed_count,
                      dead_count, cured_count, last_update_time]
        csv_writer.writerow(result_row)


def collect_row_data_3(input_file, csv_writer):
    csv_df = pd.read_csv(input_file)
    for line_num in range(len(csv_df)):
        province = csv_df["Province_State"][line_num]
        if csv_df["Country_Region"][line_num] in ["Mainland China", "Hong Kong", "Taiwan", "Macau"]:
            country = "China"
        else:
            country = csv_df["Country_Region"][line_num]
        if str(province) == "nan":
            province = country
        longitude = csv_df["Long_"][line_num]
        latitude = csv_df["Lat"][line_num]
        confirmed_count = csv_df["Confirmed"][line_num]
        if math.isnan(confirmed_count):
            confirmed_count = 0
        dead_count = csv_df["Deaths"][line_num]
        if math.isnan(dead_count):
            dead_count = 0
        cured_count = csv_df["Recovered"][line_num]
        if math.isnan(cured_count):
            cured_count = 0
        last_update_time = csv_df["Last_Update"][line_num].replace("T", " ")

        result_row = [country, province, longitude, latitude, confirmed_count,
                      dead_count, cured_count, last_update_time]
        csv_writer.writerow(result_row)


if __name__ == "__main__":
    opt = sys.argv[-1]
    if opt == '-r':
        rewrite = True
    else:
        rewrite = False

    output_file = "./COVID_country_with_city_data.csv"
    data_path = "/home/zc/work/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports"
    if rewrite:
        file_list = os.listdir(data_path)

        schema = ["Country", "Province", "Longitude", "Latitude", "ConfirmedCount", "DeadCount",
                  "CuredCount", "LastUpdateTime"]

        csv_file = open(output_file, "w+")
        writer = csv.writer(csv_file)
        writer.writerow(schema)

        for file in file_list:
            if file in ["README.md", ".gitignore"]:
                continue
            time_valid = False
            if file.startswith("01") or file.startswith("02-01"):
                collect_row_data_1(data_path + "/" + file, writer, time_valid)
            elif file.startswith("02"):
                time_valid = True
                collect_row_data_1(data_path + "/" + file, writer, time_valid)
            elif file.startswith("03-0") or file.startswith("03-1") or file.startswith("03-20") or file.startswith("03-21"):
                collect_row_data_2(data_path + "/" + file, writer)
            else:
                collect_row_data_3(data_path + "/" + file, writer)

        csv_file.close()
    else:
        file = str(time.strftime('%m-%d-%Y', time.localtime(time.time()))) + '.csv'
        csv_file = open(output_file, "a+")
        writer = csv.writer(csv_file)

        collect_row_data_3(data_path + "/" + file, writer)

        csv_file.close()

    print("collect data done!")


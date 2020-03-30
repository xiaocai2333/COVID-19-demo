import csv
import json

from pyspark.sql import SparkSession


def collect_row_data_1(spark):
    file_list = ["./data/01-*.csv", "./data/02-*.csv"]
    df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
        "Province string, Country string, LastUpdateTime string, Confirmed int, Deaths int, Recovered int"
        ).load(file_list).cache()

    df.createOrReplaceTempView("geo_data")
    df.show()
    rows = df.collect()

    schema = ["Province", "Country", "Longitude", "Latitude", "ConfirmedCount", "DeadCount",
              "CuredCount", "LastUpdateTime"]

    china_geo_coord_file = open("./china_province_geo_coord.json", "r")
    china_geo_coord = json.load(china_geo_coord_file)
    country_geo_coord_file = open("./country_geo_coord.json", "r")
    country_geo_coord = json.load(country_geo_coord_file)

    csv_file = open("./data/COVID-data.csv", "w+")
    writer = csv.writer(csv_file)
    writer.writerow(schema)

    for row in rows:
        if row["Country"] in ["Mainland China", "Hong Kong", "Taiwan", "Macau"]:
            country = "China"
        else:
            country = row["Country"]
        province = row["Province"]
        if province in china_geo_coord:
            longitude = china_geo_coord[province][0]
            latitude = china_geo_coord[province][1]
        elif country in country_geo_coord:
            longitude = country_geo_coord[country][0]
            latitude = country_geo_coord[country][1]
        else:
            longitude = "null"
            latitude = "null"
        confirmed_count = row["Confirmed"]
        dead_count = row["Deaths"]
        cured_count = row["Recovered"]
        last_update_time = row["LastUpdateTime"]

        result_row = [country, province, longitude, latitude, confirmed_count,
                      dead_count, cured_count, last_update_time]
        writer.writerow(result_row)

    china_geo_coord_file.close()
    country_geo_coord_file.close()


def collect_row_data_2(spark):
    file_list = []
    for i in range(1, 22):
        if i < 10:
            file_list.append("./data/03-0" + str(i) + "-2020.csv")
        else:
            file_list.append("./data/03-" + str(i) + "-2020.csv")

    df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
        "Province string, Country string, LastUpdateTime string, Confirmed int, Deaths int, Recovered int,"
        "Latitude double, Longitude double"
    ).load(file_list).cache()

    df.createOrReplaceTempView("geo_data")
    df.show()
    rows = df.collect()

    csv_file = open("./data/COVID-data.csv", "a")
    writer = csv.writer(csv_file)

    for row in rows:
        if row["Country"] in ["Mainland China", "Hong Kong", "Taiwan", "Macau"]:
            country = "China"
        else:
            country = row["Country"]
        province = row["Province"]
        longitude = row["Longitude"]
        latitude = row["Latitude"]
        confirmed_count = row["Confirmed"]
        dead_count = row["Deaths"]
        cured_count = row["Recovered"]
        last_update_time = row["LastUpdateTime"]

        result_row = [country, province, longitude, latitude, confirmed_count,
                      dead_count, cured_count, last_update_time]
        writer.writerow(result_row)


def collect_row_data_3(spark):
    file_list = []
    for i in range(22, 30):
        file_list.append("./data/03-" + str(i) + "-2020.csv")
    df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
        "FIPS string, Admin2 string, Province string, Country string, LastUpdateTime string,"
        "Latitude double, Longitude double, Confirmed int, Deaths int, Recovered int, "
        "Active string, Combined_Key string"
    ).load(file_list).cache()

    df.createOrReplaceTempView("geo_data")
    df.show()
    rows = df.collect()

    csv_file = open("./data/COVID-data.csv", "a")
    writer = csv.writer(csv_file)

    for row in rows:
        if row["Country"] in ["Mainland China", "Hong Kong", "Taiwan", "Macau"]:
            country = "China"
        else:
            country = row["Country"]
        province = row["Province"]
        longitude = row["Longitude"]
        latitude = row["Latitude"]
        confirmed_count = row["Confirmed"]
        dead_count = row["Deaths"]
        cured_count = row["Recovered"]
        last_update_time = row["LastUpdateTime"]

        result_row = [country, province, longitude, latitude, confirmed_count,
                      dead_count, cured_count, last_update_time]
        writer.writerow(result_row)


if __name__ == "__main__":
    spark_session = SparkSession \
        .builder \
        .appName("Python Testmap") \
        .getOrCreate()

    spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    collect_row_data_1(spark_session)
    collect_row_data_2(spark_session)
    collect_row_data_3(spark_session)

    spark_session.stop()

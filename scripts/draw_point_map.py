import datetime

from arctern.util import save_png
from arctern.util.vega import vega_weighted_pointmap

from arctern_pyspark import register_funcs
from arctern_pyspark import weighted_pointmap

from pyspark.sql import SparkSession

country_csv = '../DingXiang-COVID-data/COVID-country-data/' + 'COVID-country-' \
              + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + '.csv'
china_csv = '../DingXiang-COVID-data/COVID-china-data/' + 'COVID-china-' \
            + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + '.csv'
country_with_province_csv = "../data/summary/COVID-country-with-city-data.csv"


def draw_china_weighted_point_map(spark):
    df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
        "continent string, country string, province string, provinceLocationId string, "
        "provinceCurrentConfirmedCount int , provinceConfirmedCount int, provinceSuspectedCount int,"
        "provinceCuredCount int, provinceDeadCount int, cityName string, longitude double, latitude double,"
        "cityLocationId string, cityCurrentConfirmedCount int, cityConfirmedCount int, citySuspectedCount int,"
        "cityCuredCount int, cityDeadCount int, updateTime timestamp").load(
        china_csv).cache()

    spark.catalog.dropGlobalTempView("COVID_china")

    df.createOrReplaceTempView("COVID_china")

    register_funcs(spark)

    # 1
    res1 = spark.sql("select ST_Point(longitude, latitude) as point from COVID_china where ST_Within(ST_Point(longitude, latitude), 'POLYGON ((71.604264 17.258977, 137.319408 17.258977, 137.319408 53.808533, 71.604264 53.808533, 71.604264 17.258977))')")
    res1.createOrReplaceTempView("res1")
    res1 = spark.sql("select * from res1 where point != 'POINT (nan nan)' ")

    vega1 = vega_weighted_pointmap(1024, 896, [71.604264, 17.258977, 137.319408, 53.808533],
                                   "#EEEEEE", [2, 60], [6], 1.0, "EPSG:4326")
    res_png1 = weighted_pointmap(res1, vega1)
    save_png(res_png1, './COVID_china_weighted_point_map1.png')

    # 2
    res2 = spark.sql("select ST_Point(longitude, latitude) as point, provinceConfirmedCount as c from COVID_china "
                     "where ST_Within(ST_Point(longitude, latitude), "
                     "'POLYGON ((71.604264 17.258977, 137.319408 17.258977, 137.319408 53.808533,"
                     " 71.604264 53.808533, 71.604264 17.258977))')")

    res2.createOrReplaceTempView("res2")
    res2 = spark.sql("select * from res2 where point != 'POINT (nan nan)' ")

    vega2 = vega_weighted_pointmap(1024, 896, [71.604264, 17.258977, 137.319408, 53.808533],
                                   "blue_to_red", [2, 1000], [6], 1.0, "EPSG:4326")

    res_png2 = weighted_pointmap(res2, vega2)
    save_png(res_png2, './COVID_china_weighted_point_map2.png')

    # 3
    res3 = spark.sql("select ST_Point(longitude, latitude) as point, provinceConfirmedCount as c, "
                     "provinceConfirmedCount as s from COVID_china "
                     "where ST_Within(ST_Point(longitude, latitude), "
                     "'POLYGON ((71.604264 17.258977, 137.319408 17.258977, 137.319408 53.808533,"
                     " 71.604264 53.808533, 71.604264 17.258977))')")
    res3.createOrReplaceTempView("res3")
    res3 = spark.sql("select * from res3 where point != 'POINT (nan nan)' ")

    vega3 = vega_weighted_pointmap(3000, 2000, [71.604264, 17.258977, 137.319408, 53.808533],
                                   "blue_to_red", [2, 1000], [5, 1000], 1.0, "EPSG:4326")

    res_png3 = weighted_pointmap(res3, vega3)
    save_png(res_png3, './COVID_china_weighted_point_map3.png')
    spark.catalog.dropGlobalTempView("COVID_china")


def draw_world_weighted_point_map(spark):
    df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
        "continent string, country string, locationId string, longitude double, latitude double,"
        "currentConfirmedCount int, confirmedCount int, suspectedCount int, curedCount int, deadCount int, "
        "updateTime timestamp").load(country_csv).cache()

    df.createOrReplaceTempView("COVID_country")

    register_funcs(spark)

    # 1
    res1 = spark.sql("select ST_Point(longitude, latitude) as point from COVID_country ")
    res1.createOrReplaceTempView("res1")
    res1 = spark.sql("select * from res1 where point != 'POINT (nan nan)' ")
    res1.show(20, False)
    vega1 = vega_weighted_pointmap(3000, 2000, [-289.095983, -73.863121, 289.095983, 73.863121],
                                   "#EEEEEE", [2, 60], [6], 1.0, "EPSG:4326")
    res_png1 = weighted_pointmap(res1, vega1)
    save_png(res_png1, './COVID_country_weighted_point_map1.png')

    spark.catalog.dropGlobalTempView("COVID_country")


def draw_world_include_province_weighted_point_map(spark):
    # 1
    df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
        "Province string, Country string, Longitude double, Latitude double, ConfirmedCount int,"
        "DeadCount int, CuredCount int, LastUpdateTime string").load(country_with_province_csv).cache()

    df.createOrReplaceTempView("COVID_country_province")

    register_funcs(spark)

    res2 = spark.sql("select ST_Point(Longitude, Latitude) as point, ConfirmedCount as s from COVID_country_province "
                     "where LastUpdateTime like '%03-29%'")
    res2.createOrReplaceTempView("res2")
    res2 = spark.sql("select * from res2 where point != 'POINT (nan nan)' ")
    vega2 = vega_weighted_pointmap(3000, 2000, [-289.095983, -73.863121, 289.095983, 73.863121],
                                   "#F0356D", [2, 60], [6, 60], 1.0, "EPSG:4326")
    res_png2 = weighted_pointmap(res2, vega2)
    save_png(res_png2, './COVID_country_weighted_point_map2.png')

    spark.catalog.dropGlobalTempView("COVID_country_province")


if __name__ == "__main__":
    spark_session = SparkSession \
            .builder \
            .appName("Python TestCOVID") \
            .getOrCreate()

    spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    draw_china_weighted_point_map(spark_session)
    draw_world_weighted_point_map(spark_session)
    draw_world_include_province_weighted_point_map(spark_session)

    spark_session.stop()

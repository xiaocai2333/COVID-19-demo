import datetime
from arctern.util import save_png
from arctern.util.vega import vega_pointmap, vega_heatmap, vega_choroplethmap, vega_weighted_pointmap

from arctern_pyspark import register_funcs
from arctern_pyspark import heatmap
from arctern_pyspark import pointmap
from arctern_pyspark import choroplethmap
from arctern_pyspark import weighted_pointmap

from pyspark.sql import SparkSession

country_csv = 'COVID-country-' + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + '.csv'
china_csv = 'COVID-china-' + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + '.csv'

def draw_weighted_point_map(spark):
    df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
        "continent string, country string, province string, provinceLocationId string, "
        "provinceCurrentConfirmedCount int , provinceConfirmedCount int, provinceSuspectedCount int,"
        "provinceCuredCount int, provinceDeadCount int, cityName string, longitude double, latitude double,"
        "cityLocationId string, cityCurrentConfirmedCount int, cityConfirmedCount int, citySuspectedCount int,"
        "cityCuredCount int, cityDeadCount int, updateTime timestamp").load(
        china_csv).cache()

    df.createOrReplaceTempView("COVID_china")
    df.show()

    register_funcs(spark)

    res = spark.sql("select ST_Point(longitude, latitude) as point from COVID_china "
                    "where ST_Within(ST_Point(longitude, latitude), "
                    "'POLYGON ((71.604264 17.258977, 137.319408 17.258977, 137.319408 53.808533,"
                    " 71.604264 53.808533, 71.604264 17.258977))')")
    res.show(200, False)
    vega = vega_weighted_pointmap(1024, 896, [71.604264, 17.258977, 137.319408, 53.808533],
                                  "#EEEEEE", [2, 60], [6], 1.0, "EPSG:4326")

    res = weighted_pointmap(res, vega)
    save_png(res, './weighted_pointmap_1_0.png')


if __name__ == "__main__":
    spark_session = SparkSession \
            .builder \
            .appName("Python Testmap") \
            .getOrCreate()

    spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    draw_weighted_point_map(spark_session)

    spark_session.stop()

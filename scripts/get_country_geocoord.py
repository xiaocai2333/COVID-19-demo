import json

from pyspark.sql import SparkSession


def convert_csv_to_json(spark):
    df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
        "country string, latitude double, longitude double, name string"
    ).load("../geo_data/country_geo_coord.csv").cache()

    df.createOrReplaceTempView("geo_data")
    df.show()
    rows = df.collect()

    result = {}
    for row in rows:
        result[row["name"]] = [row["longitude"], row["latitude"]]

    with open("country_geo_coord.json", "w") as f:
        json.dump(result, f, indent=4, sort_keys=True)


if __name__ == "__main__":
    spark_session = SparkSession \
        .builder \
        .appName("Python GetCountryGeo") \
        .getOrCreate()

    spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    convert_csv_to_json(spark_session)

    spark_session.stop()

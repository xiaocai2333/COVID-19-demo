import pandas as pd


def drop_duplicates(file):
    df = pd.read_csv(file)
    new_df = df.drop_duplicates()
    new_df.to_csv(file, header=False, index=False)


if __name__ == "__main__":
    null_geo_coord_china_file = '../geo_coord/null_geo_coord_china_city.csv'
    drop_duplicates(null_geo_coord_china_file)

    null_geo_coord_country_file = '../geo_coord/null_geo_coord_country.csv'
    drop_duplicates(null_geo_coord_country_file)

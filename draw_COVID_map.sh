rm *.png
python get_COVID_data.py
python convert_json_to_csv.py
spark-submit draw_point_map.py
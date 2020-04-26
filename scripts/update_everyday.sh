cd /home/zc/work/COVID-19
git pull
cd /home/zc/work/COVID-19-demo/scripts
python3 get_COVID_data.py
python3 collect_DingXiang_data.py -d
python3 collect_country_data.py -d

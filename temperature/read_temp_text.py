import os
import sys

cwd = os.getcwd()
splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)

from sql.temperature_db import TemperatureDBUtil


def split_temperature_data(pair: str, util: TemperatureDBUtil):
    split_list = pair.split('*')
    temperature = split_list[0].split('=')[1]
    humidity = split_list[1].split('=')[1].replace('%', '')
    timestamp = split_list[2]
    # print(temperature)
    # print(humidity)
    # print(timestamp)
    util.insert_temperature(int(timestamp), float(temperature), float(humidity))


def read_temp_text():
    file = open('./temp.txt', 'r')
    line_index = 0
    data = file.readline()
    database_util = TemperatureDBUtil()
    database_util.start_connect()
    while data:
        time = file.readline()
        data = data.replace('\n', '')
        # if line_index < 10:
        split_temperature_data(data + time, util=database_util)

        line_index += 1
        data = file.readline()

    print('line count = {0}'.format(str(line_index)))
    file.close()
    database_util.close_connection()


read_temp_text()

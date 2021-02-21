import os
import sys
import time
import math
import getopt

cwd = os.getcwd()
splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)

from sql.temperature_db import TemperatureDBUtil


def main(argv):
    temperature = 0
    timestamp = 0
    humidity = 0
    try:
        opts, args = getopt.getopt(argv, "-s:-r", ['tm=', "hu=", "tr="])

    except getopt.GetoptError as e:
        print(str(e))
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--tm':
            # print('timestamp = {}'.format(arg))
            timestamp = int(arg)
        elif opt in ("--tr", "--ttt"):
            # print('temperature = {}'.format(arg))
            temperature = float(arg)
        elif opt in ("--hu", "--huhuhu"):
            # print('humidity = {}'.format(arg))
            humidity = float(arg)
    # print('timestamp = {}'.format(timestamp))
    # print('temperature = {}'.format(temperature))
    # print('humidity = {}'.format(humidity))
    temperature_db_tool = TemperatureDBUtil('./testDB.db')
    temperature_db_tool.start_connect()
    insert_result = temperature_db_tool.insert_temperature(timestamp, temperature, humidity)
    if insert_result is True:
        print('temperature 更新成功！')
    temperature_db_tool.close_connection()


if __name__ == "__main__":
    main(sys.argv[1:])

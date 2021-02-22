import time
import sched
from datetime import datetime
import os
import sys


cwd = os.getcwd()
splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)

from sql.temperature_db import TemperatureDBUtil
from temperature import DHT22


def record_temperature_task(util: TemperatureDBUtil, schedule: sched.scheduler, duration):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('start record')
    data = DHT22.read_dht22()
    humidity = float(data['humidity'])
    temperature = float(data['temperature'])
    timestamp = time.time()
    util.insert_temperature(timestamp, temperature, humidity)
    schedule.enter(duration, 0, record_temperature_task, (util, schedule, duration))


def main():
    temp_database_util = TemperatureDBUtil('./temperature.db')
    temp_database_util.start_connect()
    duration = 60 * 10
    schedule = sched.scheduler(time.time, time.sleep)
    schedule.enter(0, 0, record_temperature_task, (temp_database_util, schedule, duration))
    schedule.run()


if __name__ == "__main__":
    main()

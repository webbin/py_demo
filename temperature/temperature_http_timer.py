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

from temperature import DHT22


def read_temperature_data():
    data = DHT22.read_dht22()
    humidity = float(data['humidity'])
    temperature = float(data['temperature'])
    timestamp = int(time.time())
    return {
        'temperature': temperature,
        'humidity': humidity,
        'timestamp': timestamp,
    }


def record_temperature_task(schedule: sched.scheduler, duration):
    schedule.enter(duration, 0, record_temperature_task, (schedule, duration))


def main():
    temperature_data = read_temperature_data()
    print('temperature data = ', temperature_data)
    # print('main')
    # 时间间隔 秒数
    duration = 1
    # duration = 60 * 10
    schedule = sched.scheduler(time.time, time.sleep)
    schedule.enter(0, 0, record_temperature_task, (schedule, duration))


if __name__ == '__main__':
    main()

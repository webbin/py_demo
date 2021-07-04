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
from base import base_bs, base_requests

host = '192.168.1.104'


def push_temperature_by_http(timestamp: int, temperature: float, humidity: float):
    fetch_url = 'http://{0}:8082/add_temperature_data/?timestamp={1}&temperature={2}&humidity={3}'.format(
        host,
        timestamp,
        temperature,
        humidity
    )
    result = base_requests.base_request(fetch_url)
    print('push temperature data success ', result)


def read_temperature_data():
    data = DHT22.read_dht22()
    humidity = round(float(data['humidity']), 2)
    temperature = round(float(data['temperature']), 2)
    timestamp = round(time.time() * 1000)
    push_temperature_by_http(timestamp, temperature, humidity)
    return {
        'temperature': temperature,
        'humidity': humidity,
        'timestamp': timestamp,
    }


def record_temperature_task(schedule: sched.scheduler, duration):
    temperature_data = read_temperature_data()
    print('temperature data = ', temperature_data)
    schedule.enter(duration, 0, record_temperature_task, (schedule, duration))


def main():
    # 时间间隔 秒数
    duration = 1
    # duration = 60 * 10
    schedule = sched.scheduler(time.time, time.sleep)
    schedule.enter(0, 0, record_temperature_task, (schedule, duration))
    schedule.run()


if __name__ == '__main__':
    main()

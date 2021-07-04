import requests

import os
import sys
import json
import time

cwd = os.getcwd()
splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)

from base import base_bs, base_requests


def test_http_get():
    fetch_url = 'http://localhost:8082/get_temperature_list/?count=2&offset=1'
    result = base_requests.base_request(fetch_url)
    temp_list = json.loads(result)
    print(temp_list)
    print(len(temp_list))


def push_temperature_by_http(timestamp: int, temperature: float, humidity: float):
    fetch_url = 'http://localhost:8082/add_temperature_data/?timestamp={0}&temperature={1}&humidity={2}'.format(
        timestamp, temperature, humidity)
    result = base_requests.base_request(fetch_url)
    print('push temperature data success ', result)


if __name__ == '__main__':
    timestamp = round(time.time() * 1000)
    push_temperature_by_http(timestamp, 31.2, 58.22)
    # test_http_get()

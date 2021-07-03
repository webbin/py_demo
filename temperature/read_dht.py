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


def main():
    data = DHT22.read_dht22()
    humidity = float(data['humidity'])
    temperature = float(data['temperature'])
    timestamp = int(time.time())
    print('temperature data = ', data)


if __name__ == '__main__':
    main()

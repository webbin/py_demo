import sys

import Adafruit_DHT


def read_dht22():
    sensor = Adafruit_DHT.DHT22
    pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    print('humidity =', humidity)
    print('temperature = ', temperature)
    return {'humidity': humidity, 'temperature': temperature}


if __name__ == "__main__":
    read_dht22()

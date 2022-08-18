import hmac
import hashlib
import base64
import json
import math
import requests
import time


def get_timestamp():
    return math.floor(time.time() * 1000)


def generate_sign(secret):
    timestamp = '1660814299696'
    # timestamp = str(get_timestamp())
    app_secret = secret
    app_secret_enc = app_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, app_secret)
    string_to_sign_enc = (string_to_sign).encode('utf-8')
    key = app_secret_enc
    msg = string_to_sign_enc

    print('key = ', (key))
    print('key utf8 bytes = ', list(key))
    print('msg = ', list(string_to_sign_enc))
    hmac_code = hmac.new(key, msg, digestmod=hashlib.sha256).digest()

    print('hmac code byte length = ', len(hmac_code))
    # print('hmac code bytes = ', (hmac_code))
    print('hmac code bytes = ', list(hmac_code))
    print('hmac code hex = ', hmac_code.hex())
    sign = base64.b64encode(hmac_code).decode('utf-8')
    print('sign = ', sign)
    return sign


def msg_test():
    # token = 'a189f6edcbad0f2a802f40e88b44126b07d6af49b98763346b34b0f9ef73aedb'
    secret = 'SEC3817419f1dde72c96a09f7874d5984c9d192e93fc6825ec1063955b23b7df753'
    sign = generate_sign(secret)
    print('sign = ', sign)


if __name__ == '__main__':
    msg_test()

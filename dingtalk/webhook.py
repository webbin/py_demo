# python 2.7
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
    timestamp = str(get_timestamp())
    # app_secret = 'SEC3817419f1dde72c96a09f7874d5984c9d192e93fc6825ec1063955b23b7df753'
    app_secret = secret
    app_secret_enc = app_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, app_secret)
    string_to_sign_enc = (string_to_sign).encode('utf-8')
    hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    print('sign = ', sign)
    return sign


def send_msg(token: str, secret: str, body):
    sign = generate_sign(secret)
    timestamp = get_timestamp()
    url = 'https://oapi.dingtalk.com/robot/send?access_token={0}&timestamp={1}&sign={2}'.format(token, timestamp, sign)
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(url, data=json.dumps(body), headers=headers)
    print('response = ', response.json())


def generate_action_card_body(msg_title, pic_url, content_title, content, page_url):
    body = {
        'actionCard': {
            'title': msg_title,
            'text': '![screenshot]({0}) \n\n ### {1} \n\n {2}'.format(pic_url, content_title, content),
            'btnOrientation': '0',
            'singleTitle': '阅读全文',
            'singleURL': page_url,
        },
        'msgtype': 'actionCard',
    }
    return body


def generate_text_msg(content, mobiles=[], user_ids=[]):
    body = {
        "at": {
            "atMobiles": mobiles,
            "atUserIds": user_ids,
            "isAtAll": False
        },
        "text": {
            "content": content
        },
        "msgtype": "text"
    }
    return body


# def send_action_card_msg(token, secret):

def send_msg_use_test(body):
    token = 'a189f6edcbad0f2a802f40e88b44126b07d6af49b98763346b34b0f9ef73aedb'
    secret = 'SEC3817419f1dde72c96a09f7874d5984c9d192e93fc6825ec1063955b23b7df753'
    send_msg(token, secret, body)


def send_msg_use_bot(body):
    picUrl = ''
    # picUrl = 'http://tva3.sinaimg.cn/bmiddle/006APoFYly1gowe676h5zg307g07itc1.gif'
    content_title = '翔fucking仔要的喷蛤'
    # content = '吃饭不积极 脑子有问题'
    content = ''
    page_url = 'https://pornhub.com'

    msg_title = '[动画表情]'
    token = '9d1a3da69a8796aac8c25ef57762d705506bfbe0584788881d8d73f12e3bbb04'
    secret = 'SECf62a0f322c49ee1c5e60421090d8ede39ec05447639406a79fddc3ea0cba1b54'
    send_msg(token=token, secret=secret, body=body)

def test_text():
    body = generate_text_msg('Hello')
    send_msg_use_test(body)

def at_xiang():
    # 13533803509
    msg = '@13533803509 Missile'
    mobiles = ['13533803509']
    user_ids = ['']
    body = generate_text_msg(msg, mobiles=mobiles, user_ids=user_ids)
    send_msg_use_bot(body)


if __name__ == '__main__':
    print('main')
    # at_xiang()
    # send_msg_use_bot()
    test_text()

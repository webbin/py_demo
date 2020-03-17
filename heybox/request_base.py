# Filename: request_base.py

import requests
import math
import time
from requests.exceptions import SSLError, HTTPError as ReqHttpError
import json

Cookie = 'Hm_lvt_16e641db29b184261dffedec98f2570b=1576739191,1578896877,1578896888; ' \
         'user_pkey=MTU4MzcxOTI5Ni4zM181MTUzNDkxZ3hocmZ0bmtyeHloeHZ1bw____; user_heybox_id=5153491; ' \
         'avatar=https%3A//cdn.max-c.com/heybox/avatar/805e87ec65a43cd3191fa7d0bf5599a6%3FimageMogr2/thumbnail' \
         '/%21100p/format/jpg; nickname=webbin; heybox_id=5153491; level=13; wiki_power=0; wa=0; wr=0; ws=%5B%5D; ' \
         'wj=%5B%5D; wc=1; Hm_lvt_dfc8b88f31d0ba1cef80180022f4b3df=1583718774,1584427297; ' \
         'Hm_lpvt_dfc8b88f31d0ba1cef80180022f4b3df=1584430769 '

User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/80.0.3987.132 Safari/537.36'

header = {'Cookie': Cookie, 'User-Agent': User_Agent}

hey_box_host = 'https://api.xiaoheihe.cn'
# user_profile_path = '/bbs/web/profile/post/links'

MY_ID = '5153491'
HEY_KEY = 'd2c12b57e8bb358a1a0bc569519e40dd'


def generate_url(path, params_str: str):
    res_url = hey_box_host + path + '?' + params_str
    return res_url


def generate_param(heybox_id, userid, limit=20, offset=0):
    params = {
        'heybox_id': heybox_id,
        'userid': userid,
        'limit': limit,
        'offset': offset,
        'os_type': 'web',
        'version': '999.0.0',
        'hkey': HEY_KEY,
    }
    ts = math.floor(time.time())
    # print()
    params['_time'] = ts
    return params


def generate_param_string(obj: dict):
    keys = obj.keys()
    result = ''
    key_list = list(keys)
    list_len = len(key_list)
    ranges = range(list_len)
    for index in ranges:
        k = key_list[index]
        v = str(obj.get(k))
        # print(k, v)
        result += k + '=' + v
        if index < list_len - 1:
            result += '&'
    # print(result)
    return result


def send_request(fetch_url: str):
    session = requests.Session()
    session.headers = header

    # print('fetch url = ', fetch_url)
    try:
        res = session.get(fetch_url)
    except (ReqHttpError, SSLError) as e:
        print('error', str(e))
        return None
    else:
        return res


def get_json_result_from_response(res: requests.Response):
    try:
        data = res.json()
    except json.JSONDecodeError as e:
        print('json error', str(e))
        return None
    else:
        return data


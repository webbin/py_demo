
import json as Json
from datetime import datetime
import math
import time
import requests
from requests.exceptions import SSLError, HTTPError as ReqHttpError

hey_box_host = 'https://api.xiaoheihe.cn'
user_profile_path = '/bbs/app/profile/user/link/list'
# heybox_url = 'https://api.xiaoheihe.cn/bbs/app/profile/user/link/list?heybox_id=5153491&userid=13533929&limit=1&offset=0&os_type=web&version=999.0.0&hkey=a69b4261132622ebef74639d46da7d56&_time=1583720100'

Cookie = 'Hm_lvt_16e641db29b184261dffedec98f2570b=1576739191,1578896877,1578896888; ' \
         'Hm_lvt_dfc8b88f31d0ba1cef80180022f4b3df=1583718774; ' \
         'user_pkey=MTU4MzcxOTI5Ni4zM181MTUzNDkxZ3hocmZ0bmtyeHloeHZ1bw____; user_heybox_id=5153491; ' \
         'avatar=https%3A//cdn.max-c.com/heybox/avatar/805e87ec65a43cd3191fa7d0bf5599a6%3FimageMogr2/thumbnail' \
         '/%21100p/format/jpg; nickname=webbin; heybox_id=5153491; level=13; wiki_power=0; wa=0; wr=0; ws=%5B%5D; ' \
         'wj=%5B%5D; wc=1; Hm_lpvt_dfc8b88f31d0ba1cef80180022f4b3df=1583720100 '
User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/80.0.3987.132 Safari/537.36'

header = {'Cookie': Cookie, 'User-Agent': User_Agent}


def generate_url(params_str: str):
    res_url = hey_box_host + user_profile_path + '?' + params_str
    return res_url


def generate_param(heybox_id, userid, limit, offset):
    params = {
        'heybox_id': heybox_id,
        'userid': userid,
        'limit': limit,
        'offset': offset,
        'os_type': 'web',
        'version': '999.0.0',
        'hkey': 'a69b4261132622ebef74639d46da7d56'
    }
    ts = math.floor(time.time())
    # print()
    params['_time'] = ts
    return params


def convert_params(obj: dict):
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


def send_request():
    session = requests.Session()
    session.headers = header

    hey_id = '5153491'
    user_id = '13533929'
    param = generate_param(hey_id, user_id)
    param_str = convert_params(param)
    fetch_url = generate_url(param_str)

    try:
        res = session.get(fetch_url)
    except (ReqHttpError, SSLError) as e:
        print('error', str(e))
        return None
    else:
        return res


def handle_response(res: requests.Response):
    try:
        data = res.json()
        post_list = data['post_links']
        total_page = data['total_page']
    except Json.JSONDecodeError as e:
        print('json error', str(e))
        return None
    else:
        return {post_list: post_list, total_page: total_page}


divider = 100000

# data = res.json()
resp = send_request()
result_data: dict = resp.json()
# result = handle_response(resp)
# print(result_data.keys())
print(Json.dumps(result_data))
# convert_params(header)

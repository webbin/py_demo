import request_base
import math
import time
import json

#  https://api.xiaoheihe.cn/bbs/app/link/tree?
#  link_id=37254944&heybox_id=5153491
#  &limit=20&offset=20
#  &owner_only=0&sort_filter=hot&os_type=web&version=999.0.0&hkey=691cff770b248479aafa863cc0ba4a78
#  &_time=1584437395

from base import base_requests

link_tree_path = '/bbs/app/link/tree'


def get_header_param(link_id, limit=20, offset=0):
    params = {
        'heybox_id': request_base.MY_ID,
        'limit': limit,
        'offset': offset,
        'os_type': 'web',
        'version': '999.0.0',
        'hkey': request_base.HEY_KEY,
        'owner_only': 0,
        'link_id': link_id,
    }
    ts = math.floor(time.time())
    # print()
    params['_time'] = ts
    return params


def get_user_id_list_from_result(result: dict):
    comments = result['result']['comments']
    user_ids = []
    for item in comments:
        comment_array = item['comment']
        for com in comment_array:
            user_ids.append(com['user']['userid'])
    # print(user_ids)
    return user_ids


def get_user_id_list_by_post_id(post_id, limit=20, offset=0):
    param = get_header_param(post_id, limit, offset)
    param_str = request_base.generate_param_string(param)
    fetch_url = request_base.generate_url(link_tree_path, param_str)
    resp = request_base.send_request(fetch_url)
    data = request_base.get_json_result_from_response(resp)
    # print(json.dumps(data))
    if data is None:
        print('get user ids response is none')
        return []
    else:
        return get_user_id_list_from_result(data)

# print('fetch url = ', fetch_url)

import json as Json
import requests
import box_user
import post_tree
# https://api.xiaoheihe.cn/bbs/web/profile/post/links?heybox_id=5153491&userid=5153491&limit=20&offset=0&os_type=web&version=999.0.0&hkey=d2c12b57e8bb358a1a0bc569519e40dd&_time=1584430768
# heybox_url = 'https://api.xiaoheihe.cn/bbs/app/profile/user/link/list?heybox_id=5153491&userid=13533929&limit=1
# &offset=0&os_type=web&version=999.0.0&hkey=a69b4261132622ebef74639d46da7d56&_time=1583720100'


def get_json_result_from_response(res: requests.Response):
    try:
        data = res.json()
    except Json.JSONDecodeError as e:
        print('json error', str(e))
        return None
    else:
        return data


# data = res.json()
# resp = get_user_profile('6125174')
# info = box_user.get_user_info_by_uid('6125174')
# links = box_user.get_post_id_list_by_uid('6125174')
# for link_id in links:
#     uids = post_tree.get_user_ids_from_post_comments(link_id)
#     # print('uids = ', uids)
#     if uids is None:
#         print('uid list  is none, post id = ', link_id)
#     else:
#         for uid in uids:
#             u_info = box_user.get_user_info_by_uid(uid)

# result_data: dict = get_json_result_from_response(resp)
# if result_data is None:
#     print('response = none')
# else:
#     user_info = get_user_info_from_result(result_data)
#     print(user_info)
#     post_links = result_data['post_links']
#     for link in post_links:
#         link_id = link['linkid']
#         print('link id = ', link_id)
# print(result_data.keys())
# print(Json.dumps(result_data))

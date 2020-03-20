import request_base

user_profile_path = '/bbs/web/profile/post/links'


def get_user_profile(user_id, post_limit=10, post_offset=0):
    param = request_base.generate_param(request_base.MY_ID, user_id, limit=post_limit, offset=post_offset)
    param_str = request_base.generate_param_string(param)
    fetch_url = request_base.generate_url(user_profile_path, param_str)
    return request_base.send_request(fetch_url)


def get_user_info_from_result(data: dict):
    t_user = data['user']
    t_achieve = t_user['achieve']

    follow_count = 0
    fans_count = 0
    like_count = 0
    img_url = t_user['avartar']
    user_id = t_user['userid']
    user_name = t_user['username']

    for item in t_achieve:
        ac_key = item['key']
        ac_value = item['value']
        if ac_key == 'follow':
            follow_count = ac_value
        elif ac_key == 'fan':
            fans_count = ac_value
        elif ac_key == 'award':
            like_count = ac_value
    return {
        'follow_count': follow_count,
        'fans_count': fans_count,
        'like_count': like_count,
        'img_url': img_url,
        'id': user_id,
        'name': user_name,
    }


def get_user_info_by_uid(uid):
    resp = get_user_profile(uid)
    data = request_base.get_json_result_from_response(resp)
    if data is None:
        print('get user profile failed ')
        return None
    else:
        try:
            info = get_user_info_from_result(data)
            return info
        except Exception as e:
            print('get user info failed, uid = {1} , exception {0}'.format(str(e), uid))
            return None


def get_post_id_list_by_uid(uid, post_limit=10, post_offset=0):
    resp = get_user_profile(uid, post_limit, post_offset)
    data = request_base.get_json_result_from_response(resp)

    link_ids = []

    if data is None:
        print('get user profile failed ')
        return []
    else:
        try:
            post_links = data['post_links']
            for link in post_links:
                link_id = link['linkid']
                link_ids.append(link_id)
                # print('link id = ', link_id)
            return link_ids
        except Exception as e:
            print('get user profile failed, uid = {1} , exception {0}'.format(str(e), uid))
            return []

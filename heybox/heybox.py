import json as Json
import requests
import box_user
import post_tree
import os
import sys
import time

cwd = os.getcwd()
# print(cwd)
splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)

from sql.sqllite_test import UserTableTool
import sys


# https://api.xiaoheihe.cn/bbs/web/profile/post/links?heybox_id=5153491&userid=5153491&limit=20&offset=0&os_type=web&version=999.0.0&hkey=d2c12b57e8bb358a1a0bc569519e40dd&_time=1584430768
# heybox_url = 'https://api.xiaoheihe.cn/bbs/app/profile/user/link/list?heybox_id=5153491&userid=13533929&limit=1
# &offset=0&os_type=web&version=999.0.0&hkey=a69b4261132622ebef74639d46da7d56&_time=1583720100'

# sys.path.append(r"/home/webbin/py_project/py_demo")
# sys.path.append("..")


def insert_user_by_user_info(table_tool: UserTableTool, user_info):
    table_tool.insert_user_info(
        user_info['name'],
        user_info['id'],
        user_info['img_url'],
        user_info['fans_count'],
        user_info['follow_count'],
        user_info['like_count'],
    )


def start_crawler(table_tool: UserTableTool):
    start_uid = '6125174'
    post_list = box_user.get_post_id_list_by_uid(start_uid)
    for post_id in post_list:
        uid_list = post_tree.get_user_id_list_by_post_id(post_id)
        if uid_list is None:
            print(' post id {0}, uid list is empty '.format(post_id))
        else:
            for uid in uid_list:
                uid_in_base = table_tool.check_uid_in_user_base(uid)
                if uid_in_base:
                    print('uid {0} is in database'.format(uid))
                else:
                    u_info = box_user.get_user_info_by_uid(uid)
                    insert_user_by_user_info(table_tool, u_info)


visit_user_set = set()
MAX_VISIT_COUNT = 20
insert_count = 0
time_data = {'count': 0}


def insert_user_list_by_user_post(uid, table_tool: UserTableTool):
    limit_count = 20
    list_to_end = False
    request_offset = 0

    # 访问过这个uid的主页，跳过
    if uid in visit_user_set:
        print('You have visit uid ', uid)
        return

    has_visited = user_table_tool.check_uid_has_visit(uid)
    if has_visited:
        print('You have visit uid record in database ', uid)
        return

    if len(visit_user_set) >= MAX_VISIT_COUNT:
        print('You have visit over {} users, end '.format(MAX_VISIT_COUNT))
        return
    else:
        print('You have visit {} users'.format(len(visit_user_set)))

    visit_user_set.add(uid)
    user_table_tool.insert_visit_user(uid)

    while not list_to_end:
        id_list = box_user.get_post_id_list_by_uid(uid, limit_count, request_offset)
        # print('post id list = ', id_list)
        result_length = len(id_list)
        request_offset += result_length
        if request_offset > 100:
            print('This user has more than 100 posts')
        elif request_offset > 500:
            print('This user has more than 500 posts')
        elif request_offset > 1000:
            print('This user has more than 1000 posts')
        for post_id in id_list:
            user_ids = post_tree.get_user_id_list_by_post_id(post_id)
            for user_id in user_ids:
                is_in = table_tool.check_uid_in_user_base(user_id)
                # 已在数据库中保存过，忽略
                if is_in:
                    break
                u_info = box_user.get_user_info_by_uid(user_id)
                if u_info is not None:
                    insert_user_by_user_info(table_tool, u_info)
                    time_data['count'] += 1

        if result_length == 0:
            list_to_end = True
    print('退出循环')


user_table_tool = UserTableTool('../sql/testDB.db')
user_table_tool.start_connect()

start_time = time.time()

insert_user_list_by_user_post(table_tool=user_table_tool, uid='9156139')
# user_table_tool.insert_user_info('abd===aaa', '1001100290202', 'http', 19, 11, 222)
# user_table_tool.insert_visit_user('15491083')

end_time = time.time()
print('End , time = {0} s, insert count = {1}'.format(end_time-start_time, time_data['count']))

user_table_tool.close_connection()

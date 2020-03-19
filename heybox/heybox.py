import json as Json
import requests
import box_user
import post_tree
import os
import sys

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


def insert_user_list_by_user_post(uid, table_tool: UserTableTool):
    id_list = box_user.get_post_id_list_by_uid(uid)
    for post_id in id_list:
        user_ids = post_tree.get_user_id_list_by_post_id(post_id)
        for user_id in user_ids:
            is_in = table_tool.check_uid_in_user_base(user_id)
            # 已在数据库中保存过，忽略
            if is_in:
                break
            u_info = box_user.get_user_info_by_uid(user_id)
            insert_user_by_user_info(table_tool, u_info)


user_table_tool = UserTableTool('../sql/testDB.db')
user_table_tool.start_connect()

insert_user_list_by_user_post('6125174', user_table_tool)

user_table_tool.close_connection()

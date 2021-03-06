import sqlite3
import time
import math
import os
import sys
import BaseTableTool


# cwd = os.getcwd()
#
# splits = cwd.split(os.sep)
# splits.pop()
# parent_path = '/'.join(splits)
# sys.path.append(parent_path)


class UserTableTool(BaseTableTool):

    def select(self, table: str, cols='*', where=''):
        """
            查询
            :param table: 表名
            :param cols: 查询列
            :param where: 查询条件
            :return: 查询结果
        """
        if self.cursor is None:
            return
        cursor = self.cursor
        try:
            where = 'WHERE ' + where if where else ''
            sql_select = '''SELECT {1} FROM {0} {2}'''.format(table, cols, where)
            # print(sql_select)
            cursor.execute(sql_select)
            values = cursor.fetchall()
            return values
        except Exception as e:
            print('select failed, where = {1} , exception {0}'.format(str(e), where))
            return []

    def select_user_by_offset(self, limit, offset):
        sql_str = '''
            select * from user_test1 order by id limit {0} offset {1}
        '''.format(limit, offset)
        try:
            self.cursor.execute(sql_str)
            values = self.cursor.fetchall()
            return values
        except Exception as e:
            print('select failed, limit = {1} , offset = {2}, exception {0}'.format(str(e), limit, offset))
            return []

    def check_uid_in_user_base(self, uid):
        result = self.select('user_test1', '*', 'id=' + uid)
        # print('check uid, ', result)
        length = len(result)
        return length > 0

    def check_uid_has_visit(self, uid):
        result = self.select('visit_user_1', '*', 'user_id=' + uid)
        # print('check uid, ', result)
        length = len(result)
        return length > 0

    def get_user_list_by_offset(self, limit=10, offset=0):
        # offset代表从第几条记录“之后“开始查询，limit表明查询多少条结果
        sql_str = '''
            select * from user_test1 order by id limit {0} offset {1}
        '''.format(limit, offset)
        try:
            self.cursor.execute(sql_str)
            values = self.cursor.fetchall()
            return values
        except Exception as e:
            print('get user list offset , exception {0}'.format(str(e)))
            return []

    def insert_visit_user(self, uid):
        sql_str = '''insert into visit_user_1
                (user_id, visit_time)
                values
                (:st_id, :st_insert_time)
                '''
        ts = math.floor(time.time())
        try:
            self.cursor.execute(sql_str, {
                'st_id': uid,
                'st_insert_time': ts,
            })
            self.connection.commit()
        except Exception as e:
            print('insert visit failed, uid = {1} , exception {0}'.format(str(e), uid))

    def insert_user_info(self, name, user_id, img_url, fans_count, follow_count, like_count):
        sql_str = '''insert into user_test1
        (name, id, img_url, fans_count, follow_count, like_count, insert_time)
        values
        (:st_name, :st_id, :st_img_url, :st_fans_count, :st_follow_count, :st_like_count, :st_insert_time)
        '''
        ts = math.floor(time.time())
        try:
            self.cursor.execute(sql_str, {
                'st_name': name,
                'st_id': user_id,
                'st_img_url': img_url,
                'st_fans_count': fans_count,
                'st_follow_count': follow_count,
                'st_like_count': like_count,
                'st_insert_time': ts,
            })
            self.connection.commit()
        except Exception as e:
            print('insert user failed, id = {1} , exception {0}'.format(str(e), user_id))


import sqlite3
import sys
import time
import math


class UserTableTool:
    def __init__(self, file_path):
        self.file_path = file_path
        self.connection = None
        self.cursor = None

    def start_connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.file_path)
            self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

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


# table_tool = UserTableTool('./testDB.db')
# table_tool.start_connect()
# cur = conn.cursor()
# c.execute('''CREATE TABLE COMPANY
#        (ID INT PRIMARY KEY     NOT NULL,
#        NAME           TEXT    NOT NULL,
#        AGE            INT     NOT NULL,
#        ADDRESS        CHAR(50),
#        SALARY         REAL);''')
# print('table create')
# conn.commit()
# conn.close()

# print('insert ')
# print(sys.path)
# table_tool.insert_user_info('abd', '1001100290202', 'http', 19, 11, 222)
# table_tool.close_connection()
# select_user_by_id('100202')

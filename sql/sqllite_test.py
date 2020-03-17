
import sqlite3
import sys


conn = sqlite3.connect('./testDB.db')
cur = conn.cursor()
# c.execute('''CREATE TABLE COMPANY
#        (ID INT PRIMARY KEY     NOT NULL,
#        NAME           TEXT    NOT NULL,
#        AGE            INT     NOT NULL,
#        ADDRESS        CHAR(50),
#        SALARY         REAL);''')
# print('table create')
# conn.commit()
# conn.close()


def select(cursor, table: str, cols='*', where=''):
    '''
    查询
    :param table: 表名
    :param cols: 查询列
    :param where: 查询条件
    :return: 查询结果
    '''
    values = None
    try:
        where = 'WHERE ' + where if where else ''
        sql_select = '''SELECT {1} FROM {0} {2}'''.format(table, cols, where)
        print(sql_select)
        cursor.execute(sql_select)
        values = cursor.fetchall()
    except Exception as e:
        print(e)
    return values


def insert_user_info(name, user_id, img_url, fans_count, follow_count, like_count):
    sql_str = '''insert into user_test1
    (name, id, img_url, fans_count, follow_count, like_count)
    values
    (:st_name, :st_id, :st_img_url, :st_fans_count, :st_follow_count, :st_like_count)
    '''
    cur.execute(sql_str, {
        'st_name': name,
        'st_id': user_id,
        'st_img_url': img_url,
        'st_fans_count': fans_count,
        'st_follow_count': follow_count,
        'st_like_count': like_count,
    })
    conn.commit()
    # conn.close()


def check_uid_in_user_base(uid):
    list = select(cur, 'user_test1', '*', 'id='+uid)
    # print(list)
    length = len(list)
    return length > 0


def close_connection():
    conn.close()

# print('insert ')
print(sys.path)
# insert_user_info('abd', '100290202', 'http', 19, 11, 222)
# select_user_by_id('100202')


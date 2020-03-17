
import sqlite3

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
    conn.close()


# print('insert ')
# insert_user_info('abd', '100290202', 'http', 19, 11, 222)


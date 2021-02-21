import sqlite3


class BaseTableTool:
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

    def create_table(self, table_name, data):
        # CREATE TABLE 表名称
        # (
        #     列名称1 数据类型,
        # 列名称2 数据类型,
        # 列名称3 数据类型,
        # ....
        # )
        result = False
        sql_str = '''
            CREATE TABLE {0}
            (
                {1}
            )
        '''.format(table_name, data)
        # print('sql str = {}'.format(sql_str))
        try:
            self.cursor.execute(sql_str)
            result = True
        except Exception as e:
            print('create table {0} failed, exception {0}'.format(table_name, str(e)))
        return result

    def delete_table(self, table_name):
        result = False
        sql_str = '''
                    DROP TABLE {0}
                '''.format(table_name)
        try:
            self.cursor.execute(sql_str)
            result = True
        except Exception as e:
            print('drop table {0} failed, exception {0}'.format(table_name, str(e)))
        return result

    def select(self, table: str, cols='*', where=''):
        """
            查询
            :param table: 表名
            :param cols: 查询列
            :param where: 查询条件
            :return: 查询结果
        """
        if self.cursor is None:
            return []
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

    def get_record_size(self, table):
        size = 0
        cursor = self.cursor
        if cursor is None:
            size = 0
        try:
            sql_select = '''SELECT * FROM {0}'''.format(table)
            # print(sql_select)
            cursor.execute(sql_select)
            values = cursor.fetchall()
            size = len(values)
        except Exception as e:
            print('select failed, exception {0}'.format(str(e)))

        return size

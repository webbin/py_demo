import sqlite3
import sys
import time
import math


class TemperatureDBUtil:
    def __init__(self):
        self.file_path = 'temperature.db'
        self.connection = None
        self.cursor = None

    def start_connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.file_path)
            self.cursor = self.connection.cursor()

    def close_connection(self):
        if self.connection is not None:
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

    def insert_temperature(self, timestamp, temperature, humidity):
        sql_str = '''insert into temperature
                        (timestamp, temperature, humidity)
                        values
                        (:st_time, :st_temperature, :ts_humidity)
                        '''
        # ts = math.floor(time.time())
        try:
            self.cursor.execute(sql_str, {
                'st_time': timestamp,
                'st_temperature': temperature,
                'ts_humidity': humidity,
            })
            self.connection.commit()
        except Exception as e:
            print('insert visit failed, uid = {1} , exception {0}, time = {2}'.format(str(e), temperature, timestamp))

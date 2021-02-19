import os
import sys
import time
import math

cwd = os.getcwd()
splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)

from sql.BaseTableTool import BaseTableTool


class TemperatureDBUtil(BaseTableTool):
    def insert_temperature(self, timestamp, temperature, humidity):
        result = False
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
            result = True
        except Exception as e:
            print('exception {0}, time = {2}'.format(str(e), temperature, timestamp))
        return result


def main():
    temperature_db_tool = TemperatureDBUtil('./testDB.db')
    temperature_db_tool.start_connect()
    mil_sec = int(time.time() * 1000)
    insert_result = temperature_db_tool.insert_temperature(mil_sec, 19.3, 12.2)
    if insert_result is True:
        print('更新成功！')
    temperature_db_tool.close_connection()


# if __name__ == "__main__":
#     main()

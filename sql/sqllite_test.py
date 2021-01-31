import os
import sys

cwd = os.getcwd()
splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)

from sql.BaseTableTool import BaseTableTool


def manual_table():
    print('[1] 创建表')
    print('[2] 删除表')
    table_operate = input('请输入要执行的操作: ')
    # print('您选择了 {0}'.format(table_operate))

    table_name = input('请输入table_name: ')
    table_tool = BaseTableTool('./testDB.db')
    table_tool.start_connect()
    if table_operate == '1':
        result = table_tool.create_table(table_name, '''
            timestamp int,
            temperature decimal(3,2),
            humidity decimal(3,2)
            ''')
        if result is True:
            print('创建成功！')
        else:
            print('创建失败！')
    else:
        result = table_tool.delete_table(table_name)
        if result is True:
            print('删除成功！')
        else:
            print('删除失败！')

    table_tool.close_connection()


def main():
    manual_table()


if __name__ == "__main__":
    main()

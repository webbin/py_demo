import time


def show_timestruct(t):
    print('年：', t.tm_year)
    print('月：', t.tm_mon)
    print('日：', t.tm_mday)
    print('小时：', t.tm_hour)
    print('分钟', t.tm_min)
    print('秒', t.tm_sec)
    print('星期：', t.tm_wday)
    print('一年的第 %s 天' % t.tm_yday)
    print('是否夏时令：', t.tm_isdst)


def show_time():
    mil_sec = time.time()
    t1 = time.gmtime(mil_sec)
    # print('gm time ', mil_sec, int(mil_sec))
    show_timestruct(t1)
    print('local time -----')
    local_time = time.localtime(mil_sec)
    show_timestruct(local_time)


show_time()

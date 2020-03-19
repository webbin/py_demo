
import threading

import json
import os


def ping_ip(ip_address):
    cmd = 'ping '+ip_address+' -c 1'
    file = os.popen(cmd)
    result: str = file.read()
    # i = result.find('statistics')
    splits = result.split('\n')
    length = len(splits)
    statistics = splits[length - 2]
    # print(ip_address)
    # print(statistics)
    loss_index = statistics.find('loss')
    if loss_index > 0:
        print(ip_address, 'failed')
    else:
        tips = statistics.split(' ')
        # print(tips)
        times = tips[3]
        time_splits = times.split('/')
        avg = time_splits[1]
        print(ip_address, 'avg = '+avg)


class PingThread (threading.Thread):
    def __init__(self, ip_address):
        threading.Thread.__init__(self)
        self.ip = ip_address

    def run(self):
        ping_ip(self.ip)


json_file = open('./export-ssr-0319.json', 'r')
text = json_file.read()
conf = json.loads(text)
server_list = conf['configs']

thread_list = []

for server in server_list:
    server_ip = server['server']
    th = PingThread(server_ip)
    thread_list.append(th)

for th in thread_list:
    th.start()

for th in thread_list:
    th.join()
# print(len(server_list))
# ping_ip(server_list[0]['server'])
print('--- ping servers end ---')

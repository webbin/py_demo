
from urllib import request
import requests
from io import open
import os
import sys
cwd = os.getcwd()

splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)
from base import base_requests

request_tool = base_requests.BaseRequests()

bundle_url = 'http://localhost:8081/index.js.bundle?platform=ios&dev=true&minify=false'
img_url = 'http://h1.ioliu.cn/bing/PascuaFlorida_ZH-CN7720904158_800x480.jpg?imageslim'


def download_bundle():
    data = requests.get(bundle_url)
    bundle_file = open('./bundle.txt', 'wb+')

    # print(len(texts))
    bundle_bytes = bytes(data.text, 'utf-8')
    bundle_file.write(bundle_bytes)
    print('write bundle done')
    os.popen('subl ./bundle.txt')


def download_img():
    request_tool.download_img_by_requests(img_url, download_dir=cwd)


# download_img()

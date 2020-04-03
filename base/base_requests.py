
import requests
import re
import time
import math
import os

from base import base_log

User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/80.0.3987.132 Safari/537.36'

header = {'User-Agent': User_Agent}

class BaseRequests():
    def __init__(self, log_tool:base_log.LogTool):
        if log_tool is None:
            self.log_tool = base_log.LogTool('log.txt')
        else:
            self.log_tool = log_tool

    def get_file_name_by_time(self, prefix='', suffix=''):
        name = str(math.floor(time.time() * 1000))
        return prefix + name + suffix

    def get_file_name_from_header(self, headers):
        disposition = headers['Content-Disposition']
        match = re.search(r'filename="(\S+)"', disposition)
        if match is not None:
            return match.group(1)
        return self.get_file_name_by_time('bing-', '.jpg')

    def set_proxy(self, proxy):
        self.proxy = proxy

    def download_img_by_requests(self, img_url, download_dir=None, download_file_path=None, overwrite=True):
        # overwrite 是否覆盖文件，如果不覆盖，文件存在时就不下载
        if img_url is None:
            self.log_tool.log('img url is None')
            return
        if download_file_path is not None and overwrite is False:
            file_exist = os.path.exists(download_file_path)
            if file_exist:
                self.log_tool.log('file exist')
                return
        # print('dir = {0}, file path = {1}'.format(download_dir, download_file_path))
        try:
            session = requests.Session()
            session.headers = header
            if self.proxy is not None:
                session.proxies = self.proxy

            res = session.get(img_url)
            self.log_tool.log('download img url = {}'.format(img_url))
            self.log_tool.log('headers'.format(res.headers))
            res.raise_for_status()
            op_file = {}
            if download_file_path is not None:
                op_file = open(download_file_path, 'wb')
            elif download_dir is not None:
                # print(res.headers)
                file_name = self.get_file_name_from_header(res.headers)
                file_path = download_dir + '/' + file_name
                file_exist = os.path.exists(file_path)
                if file_exist and overwrite is False:
                    self.log_tool.log('file exist {}'.format(file_name))
                    return
                op_file = open(file_path, 'wb')

            for chunk in res.iter_content(4096):
                op_file.write(chunk)
            op_file.close()
        except Exception as e:
            self.log_tool.log('download image failed, exception = {}'.format(e))
        else:
            self.log_tool.log('url %s download complete ' % img_url)


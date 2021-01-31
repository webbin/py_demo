
import requests
import os
import sys

cwd = os.getcwd()
splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)

from base import base_requests
requests_tool = base_requests.BaseRequests()
requests_tool.use_proxy(1)


def fetch_file_url(url):
    # res = requests_tool.get(url)
    # print(res.headers)
    # print(requests_tool.get_file_name_from_header(res.headers))
    requests_tool.download_img_by_requests(url, download_dir=cwd)


img_url = 'https://wallpapersite.com/images/wallpapers/anime-girl-3840x2160-night-lonely-4k-19530.jpg'
fetch_file_url(img_url)
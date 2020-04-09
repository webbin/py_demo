
from urllib import request as url_request
import requests
from requests.exceptions import SSLError, HTTPError as ReqHttpError

# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.ssl_ import create_urllib3_context

from io import open
import os
import sys

cwd = os.getcwd()
splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)

from base import base_bs, base_requests, base_log

requests_tool = base_requests.BaseRequests()


def get_img_url_from_href(href: str):
    page_url = 'https://wallpapersite.com'+href
    html = base_requests.base_request(page_url)
    if html is not None:
        bs = base_bs.get_bs_parse_result(html)
        a_list = bs.findAll('a', {'class': 'original'})
        if a_list is not None:
            node = a_list[0]
            href = node.get('href')
            # print('img url = ', href)
            # return href


def fetch_site_anime(page):
    fetch_url = 'https://wallpapersite.com/anime/?page={}'.format(page)
    result = base_requests.base_request(fetch_url)
    if result is not None:
        # print(result)
        bs = base_bs.get_bs_parse_result(result)
        img_list = bs.findAll('a', {'class': None})
        print('length = ', len(img_list))
        if img_list is not None:
            for node in img_list:
                if node.childrens is None:
                    print(node)
            # node = img_list[0]
            # href = node.get('href')
            # # img_url = get_img_url_from_href(href)
            # print('href = ', node)


fetch_site_anime(1)

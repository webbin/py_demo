
import requests
import math
import time
from requests.exceptions import SSLError, HTTPError as ReqHttpError
import json
import os
import sys

cwd = os.getcwd()
# print(cwd)
splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)
from base import base_bs


User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/80.0.3987.132 Safari/537.36'

header = {'User-Agent': User_Agent}


def bing_base_request(fetch_url):
    session = requests.Session()
    session.headers = header
    try:
        res = session.get(fetch_url)
        return res.text
    except Exception as e:
        print('fetch bing ioliu error ', e)
        return None


def fetch_bing_ioliu(index):
    url_str = 'https://bing.ioliu.cn/?p='+str(index)
    return bing_base_request(url_str)


def get_img_url_by_page_href(tag_href):
    page_url = 'https://bing.ioliu.cn'+tag_href
    # print('page url =', page_url)
    page_html = bing_base_request(page_url)
    if page_html is None:
        print(' html is none ')
        return
    result = base_bs.get_bs_parse_result(page_html)
    print('html =', page_html)
    list = result.findAll('div', {'class':'mark'})
    # print('get {} mark div'.format(len(list)))
    node = list[0]
    print(node)


def handle_ioliu_html(html):
    # print(html)
    if html is None:
        print('html is none ')
        return
    bs_result = base_bs.get_bs_parse_result(html)
    list = bs_result.findAll('a', {'class':'mark'})
    length = len(list)
    print('find {} img tags'.format(length))
    node = list[0]
    href = node.get('href')
    get_img_url_by_page_href(href)
    # for node in list:
    #     href = node.get('href')
    #     get_img_url_by_page_href(href)


text = fetch_bing_ioliu(1)
handle_ioliu_html(text)


import requests
import math
import time
from requests.exceptions import SSLError, HTTPError as ReqHttpError
import json
import os
import sys
import re

cwd = os.getcwd()
splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)
from base import base_bs, base_selenium, base_requests


User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/80.0.3987.132 Safari/537.36'

header = {'User-Agent': User_Agent}


def check_file(file_path):
    return os.path.exists(file_path)


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


def match_img_url_from_style(style:str):
    pattern = r'\("(\S+)"\)'
    result = re.search(pattern, style)
    if result is None:
        print('match image url failed, style = ', style)
        return None
    img_url = result.group(1)
    # print('match result = ', img_url)
    return img_url


def get_img_url_by_page_href(tag_href):
    page_url = 'https://bing.ioliu.cn'+tag_href
    print('page url =', page_url)
    page_html = base_selenium.get_html_by_url(page_url)
    if page_html is None:
        print(' html is none ')
        return
    result = base_bs.get_bs_parse_result(page_html)
    # print('html =', page_html)
    list = result.findAll('img')
    node = list[0]
    img_url = node.get('src')
    # print(img_url)
    return img_url
    # return match_img_url_from_style(node_style)


def handle_ioliu_html(html):
    # print(html)
    if html is None:
        print('html is none ')
        return
    bs_result = base_bs.get_bs_parse_result(html)
    list = bs_result.findAll('a', {'class':'mark'})
    length = len(list)
    print('find {} img tags'.format(length))
    # node = list[0]
    # href = node.get('href')
    # print('href = ', href)
    # print('get img url from href ', img_url)
    for node in list:
        href = node.get('href')
        img_url = get_img_url_by_page_href(href)
        base_requests.download_img_by_requests(img_url, download_dir=cwd + '/src', overwrite=False)
        time.sleep(2)


def start_download_from_bing():
    index = 2
    while index < 3:
        text = fetch_bing_ioliu(index)
        print('fetch bing text ', text)
        handle_ioliu_html(text)
        index += 1
    base_selenium.close_browser()


# match_img_url_from_style('background-image: url("http://h1.ioliu.cn/bing/ShyGuy_ZH-CN7391687938_1920x1080.jpg?imageslim"); filter: blur(0px);')
start_download_from_bing()

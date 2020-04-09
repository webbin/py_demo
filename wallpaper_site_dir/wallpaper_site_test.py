

import requests as request_lib
from requests.exceptions import SSLError, HTTPError as ReqHttpError

from io import open
import os
import sys
from bs4 import Tag

cwd = os.getcwd()
splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)

from base import base_bs, base_requests, base_log

request_tool = base_requests.BaseRequests()
request_tool.use_proxy(1)

def get_length(generator):
    if hasattr(generator,"__len__"):
        return len(generator)
    else:
        return sum(1 for _ in generator)

def if_a_has_img(a_tag):
    if a_tag is None:
        return False
    if a_tag.children is None:
        return False
    for child in a_tag.children:
        if child.name == 'img':
            return True
    return False


def get_img_href_from_tag(tag: Tag):
    if tag.children is None:
        return None
    has_img = False
    obj = {}
    for index, child in enumerate(tag.contents):
        obj[child.name] = child
        if child.name == 'img':
            has_img = True
            print(tag.contents)
    # if has_img and obj['a'] is not None:
    #     return obj['a'].get('href')
    return None


def get_anime_fetch_url(page):
    return 'https://wallpapersite.com/anime?page={}'.format(page)


def get_img_url_by_page_href(href):
    page_url = 'https://wallpapersite.com'+href
    html = request_tool.send_request(page_url)
    if html is None:
        print('page html is none')
        return None
    bs = base_bs.get_bs_parse_result(html)
    node = bs.find('a',{'class':'original'})
    if list is not None:
        # print(node)
        href = node.get('href')
        url = 'https://wallpapersite.com'+href
        print(url)
        return url
    return None


def get_img_url_list_from_html(html):
    if html is None:
        print('html is None ')
        return None
    bs = base_bs.get_bs_parse_result(html)
    list = bs.findAll('a', {'class': None})
    result = []
    for node in list:
        has_img = if_a_has_img(node)
        if has_img:
            href = node.get('href')
            # print(href)
            result.append(href)
    return result

def download_img_by_page_index(index):
    url = get_anime_fetch_url(1)
    html = request_tool.send_request(url)
    list = get_img_url_list_from_html(html)
    if list is not None:
        for url in list:
            img_url = get_img_url_by_page_href(url)
            if img_url is not None:
                request_tool.download_img_by_requests(img_url, download_dir=cwd + '/resource', overwrite=False)


def run():
    index = 1
    while index < 10:
        download_img_by_page_index(index)
        index += 1
        # href = list[0]
        # img_url = get_img_url_by_page_href(href)


run()
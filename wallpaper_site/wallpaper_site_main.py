
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
Host_Wallpaper_Site = 'https://wallpapersite.com'


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


def if_a_has_img(tag):
    if tag is None:
        return False
    if tag.contents is None:
        return False
    for child in tag.contents:
        if child.name == 'img':
            return True
    return False


def get_img_original_url(page_url):
    result = base_requests.base_request(page_url)
    if result is not None:
        bs = base_bs.get_bs_parse_result(result)
        tag = bs.find('a', {'class': 'original'})
        # print(tag)
        href = tag.get('href')
        original_url = Host_Wallpaper_Site+href
        print('get original url of {}'.format(page_url))
        return original_url


def download_img(img_url):
    print('start download img {} '.format(img_url))
    requests_tool.download_img_by_requests(img_url, overwrite=False, download_dir=cwd+'/resource')


def get_img_page_href_by_index(page):
    fetch_url = 'https://wallpapersite.com/anime/?page={}'.format(page)
    result = base_requests.base_request(fetch_url)
    if result is not None:
        # print(result)
        bs = base_bs.get_bs_parse_result(result)
        img_list = bs.findAll('a', {'class': None})
        # print('length = ', len(img_list))
        result = []
        if img_list is not None:
            for node in img_list:
                node_has_img = if_a_has_img(node)
                if node_has_img:
                    # print(node)
                    href = node.get('href')
                    result.append(Host_Wallpaper_Site+href)
            # node = img_list[0]
            # href = node.get('href')
            # # img_url = get_img_url_from_href(href)
            # print('href = ', node)
        print('find {} img href'.format(len(result)))
        return result


def download_images_by_page_index(index):
    href_list = get_img_page_href_by_index(index)
    # print('href list = ', href_list)
    for node in href_list:
        img_url = get_img_original_url(node)
        download_img(img_url)


def run():
    requests_tool.use_proxy(3)
    index = 1
    while index < 10:
        download_images_by_page_index(index)
        index += 1


run()

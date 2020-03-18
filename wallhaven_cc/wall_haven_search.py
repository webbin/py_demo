
import os
import sys
import requests as request_lib
from requests.exceptions import SSLError, HTTPError as ReqHttpError
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

cwd = os.getcwd()
# print(cwd)
splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)

from heybox import request_base

# https://wallhaven.cc/search?q=anime&categories=010&purity=100&sorting=views&order=desc

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}


def get_wall_haven_search_url(param_str):
    return 'https://wallhaven.cc/search?'+param_str


def send_request_ssr_proxy(input_url):
    proxies = {
        'http': 'socks5://127.0.0.1:1086',
        'https': 'socks5://127.0.0.1:1086',
    }
    session = request_lib.Session()
    session.proxies = proxies
    session.headers = HEADER
    data = None
    try:
        res = session.get(input_url)
        data = res.text
    except Exception as e:
        print('error', str(e))
        return data
    else:
        return data


def get_search_param(q: str, categories: str, purity: str, sorting: str, order: str = 'desc'):
    params = {
        'q': q,
        'categories': categories,
        'purity': purity,
        'sorting': sorting,
        'order': order,
    }
    param_string = request_base.generate_param_string(params)
    # print(param_string)
    return param_string


param_string_ = get_search_param('anime', '010', '100', 'views')
fetch_url = get_wall_haven_search_url(param_string_)
datas = send_request_ssr_proxy(fetch_url)
print(datas)

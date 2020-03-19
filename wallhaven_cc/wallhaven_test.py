
from urllib import request as url_request
import requests as request_lib
from requests.exceptions import SSLError, HTTPError as ReqHttpError
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from io import open
import os

Html_Parser = 'html.parser'


User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/80.0.3987.132 Safari/537.36'

HEADER = {'User-Agent': User_Agent}


def custom_proxy_open_url(url: str):
    proxy_host = '127.0.0.1:1087'  # host and port of your proxy

    req = url_request.Request('url')
    req.set_proxy(proxy_host, 'http')

    response = url_request.urlopen(req)
    print(response.read().decode('utf8'))


def get_img_file_path(file_name):
    return 'src/'+file_name


def download_img(img_url):
    file_name = get_file_name_from_url(img_url)
    # url_request.urlretrieve(img_url, get_img_file_path(file_name))
    file_n, header = url_request.urlretrieve('http://python.org/')
    print(header)


def download_img_by_requests(img_url):
    if img_url is None:
        print('img url is None')
        return
    file_name = get_file_name_from_url(img_url)
    file_path = get_img_file_path(file_name)
    if os.path.exists(file_path):
        print('url %s file exists ' % img_url)
    else:
        try:
            res = request_lib.get(img_url)
            res.raise_for_status()

            op_file = open(file_path, 'wb')
            for chunk in res.iter_content(4096):
                op_file.write(chunk)
            op_file.close()
        except Exception as e:
            print('There was a problem when download file : %s' % e)
        else:
            print('url %s download complete ' % img_url)


def get_file_name_from_url(file_url: str):
    splits = file_url.split('/')
    return splits.pop()


def send_request_by_aqara_proxy(input_url):
    proxies = {
        'http': 'socks5://proxy.aqara.com:1080',
        'https': 'socks5://proxy.aqara.com:1080',
    }
    session = request_lib.Session()
    session.proxies = proxies
    session.headers = HEADER
    try:
        res = session.get(input_url)
    except (ReqHttpError, SSLError) as e:
        print('error', str(e))
        return None
    else:
        return res


def get_img_url_from_page_detail(page_url):
    res = send_request_by_aqara_proxy(page_url)
    # write_result(res.text)
    if res is None:
        print('None, response is None ')
        return None
    bs = BeautifulSoup(res.text, Html_Parser)
    img = bs.find('img', {'id': 'wallpaper'})
    if img is None:
        print('None, cannot find image ')
        return None
    else:
        src = img.get('src')
        # print('get img url from page detail , url = ', src)
        return src


def fetch_wall_haven_anime():
    url_wallhaven = 'https://wallhaven.cc/search?q=id:1&ref=fp'
    res = send_request_by_aqara_proxy(url_wallhaven)
    if res is None:
        return
    # print(res.text)
    # write_result(res.text)
    bs = BeautifulSoup(res.text, Html_Parser)
    links = bs.findAll('a', {'class': 'preview'})
    for link in links:
        href = link.get('href')
        # print(href)
        img_url = get_img_url_from_page_detail(href)
        download_img_by_requests(img_url)


# fetch_wall_haven_anime()
# down_file_url = 'https://w.wallhaven.cc/full/8x/wallhaven-8xxjjj.jpg'
# download_img_by_requests(down_file_url)
fetch_wall_haven_anime()

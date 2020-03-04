
from urllib.request import urlopen, ProxyHandler, build_opener, Request, urlretrieve
import requests as request_lib
from requests.exceptions import SSLError, HTTPError as ReqHttpError
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from io import open
import socks
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}
url = "https://www.baidu.com"
url_google = 'https://google.com'
Html_Parser = 'html.parser'

# html = urlopen(url)
# bs = BeautifulSoup(html.read(), 'html.parser')
# print(bs.script)

#
# proxyHandler = ProxyHandler({'socks5': 'proxy.aqara.com:1080'})
# proxyOpener = build_opener(proxyHandler)
#
# google_request = Request(url_google, headers=header)
# response = proxyOpener.open(google_request)
#
# print(response.read().decode('utf-8'))


def download_file(download_url):
    try:
        session = request_lib.Session()
        session.headers = header
        res = session.get(download_url)
    except URLError as e:
        print('http error ', e.strerror)
    else:
        print(res.headers)


def get_proxy_response(input_url):
    proxies = {
        'http': 'socks5://proxy.aqara.com:1080',
        'https': 'socks5://proxy.aqara.com:1080',
    }
    session = request_lib.Session()
    session.proxies = proxies
    session.headers = header
    try:
        res = session.get(input_url)
    except (ReqHttpError, SSLError) as e:
        print('error', str(e))
        return None
    else:
        return res


def read_jd_use_requests():
    jd_url = 'https://jd.com'
    res = get_proxy_response(jd_url)
    if res is None:
        return
    # print(res.text)
    jd_bs = BeautifulSoup(res.text, 'html.parser')
    all_img = jd_bs.findAll('img')
    print(len(all_img))


def write_result(result):
    file = open('response.txt', 'w')
    file.write(str(result))
    file.close()
    print('write result done')


def handle_page_detail(page_url):
    res = get_proxy_response(page_url)
    # write_result(res.text)
    if res is None:
        return
    bs = BeautifulSoup(res.text, Html_Parser)
    img = bs.find('img', {'id': 'wallpaper'})
    if img is None:
        print('None')
    else:
        src = img.get('src')
        download_file(src)
        # print('src = ', src)


def quest_socks_proxy():
    url_wallhaven = 'https://wallhaven.cc/search?q=id:1&ref=fp'
    res = get_proxy_response(url_wallhaven)
    if res is None:
        return
    # print(res.text)
    # write_result(res.text)
    bs = BeautifulSoup(res.text, Html_Parser)
    links = bs.findAll('a', {'class': 'preview'})
    # for link in links:
    #     print(link.get('href'))
    # print(links[0].get('href'))
    handle_page_detail(links[0].get('href'))


quest_socks_proxy()
# read_jd_use_requests()
# proxies = {
#         'http': 'socks5://proxy.aqara.com:1080',
#         'https': 'socks5://proxy.aqara.com:1080',
#     }
# res = request_lib.get(url_google, proxies=proxies)

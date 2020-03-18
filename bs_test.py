
from bs4 import BeautifulSoup
from urllib import request as url_request
from urllib.request import urlopen, build_opener, ProxyHandler
from urllib.error import HTTPError, URLError
import requests as request_lib
from requests.exceptions import SSLError, HTTPError as ReqHttpError

bing_url = 'https://cn.bing.com/images/trending?form=Z9LH'

wallHavenUrl = 'https://wallhaven.cc/search?q=id:1&ref=fp'
wall_haven_anime = 'https://wallhaven.cc/search?q=id:1&ref=fp'
biao_qing_url = 'https://www.fabiaoqing.com/biaoqing'

# html = urlopen(wallHavenUrl)
# print(len(aList))


proxy_handler = ProxyHandler({'http': 'http://127.0.0.1:1087'})
opener = build_opener(proxy_handler)
# r = opener.open('http://httpbin.org/ip')
# print(str(r.read()))


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}


def get_proxy_response(input_url):
    proxies = {
        'http': 'http://127.0.0.1:1087',
        'https': 'http://127.0.0.1:1087',
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


def test_google():
    google_url = 'https://www.google.com'
    res = get_proxy_response(google_url)
    print(res.text)


def fetch_wall_haven():
    try:
        wh_html = opener.open(wallHavenUrl)
        wall_haven_bs = BeautifulSoup(wh_html.read(), 'html.parser')
        a_list = wall_haven_bs.find_all('a', {'class': 'preview'})
        print(len(a_list))
    except HTTPError as e:
        print('http error ', e.code)
    except URLError as e:
        print('url error ', e.errno)
    else:
        print('Done')


def biao_qing_fetch():
    bq_html = urlopen(biao_qing_url)
    bq_bs = BeautifulSoup(bq_html.read(), 'html.parser')
    result = bq_bs.find_all('img', {'class': 'ui image lazy'})
    print('find ', len(result), ' img tag')


# fetch_wall_haven()
def start_fetch():
    try:
        biao_qing_fetch()
    except HTTPError as e:
        print('http error ', e.code)
    except URLError as e:
        print('url error ', e.errno, e.reason)
    else:
        print('Done')


# test_google()
# start_fetch()

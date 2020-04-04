from urllib import request as url_request
import requests as request_lib
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

from base import base_bs, base_requests, base_log, base_selenium

User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/80.0.3987.132 Safari/537.36'

HEADER = {'User-Agent': User_Agent}
img_dir = cwd + '/src'

log_tool = base_log.LogTool('wall_haven_log.txt', need_print=True)
is_use_aqara = False
SSR_Proxy = {
    'http': 'http://127.0.0.1:1087',
    'https': 'http://127.0.0.1:1087',
}
AQARA_PROXY = {
    'http': 'socks5://proxy.aqara.com:1080',
    'https': 'socks5://proxy.aqara.com:1080',
}


# class DESAdapter(HTTPAdapter):
#     """
#     A TransportAdapter that re-enables 3DES support in Requests.
#     """
#     def init_poolmanager(self, *args, **kwargs):
#         self.CIPHERS = (
#             'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
#             'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
#             '!eNULL:!MD5'
#         )
#         context = create_urllib3_context(ciphers=self.CIPHERS)
#         kwargs['ssl_context'] = context
#         return super(DESAdapter, self).init_poolmanager(*args, **kwargs)
#
#     def proxy_manager_for(self, *args, **kwargs):
#         context = create_urllib3_context(ciphers=self.CIPHERS)
#         kwargs['ssl_context'] = context
#         return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)


def get_img_file_path(file_name):
    return 'src/' + file_name


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
        log_tool.log('url %s file exists ' % img_url)
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


def send_request_by_proxy(input_url):
    session = request_lib.Session()
    if is_use_aqara:
        session.proxies = AQARA_PROXY
    else:
        session.proxies = SSR_Proxy
    session.headers = HEADER
    # session.mount(input_url, DESAdapter())
    try:
        res = session.get(input_url)
    except Exception as e:
        log_tool.log('error {}'.format(e))
        return None
    else:
        return res


def get_img_url_from_page_detail(page_url):
    res = send_request_by_proxy(page_url)
    # write_result(res.text)
    if res is None:
        print('None, response is None ')
        return None
    bs = base_bs.get_bs_parse_result(res.text)
    img = bs.find('img', {'id': 'wallpaper'})
    if img is None:
        print('None, cannot find image ')
        return None
    else:
        src = img.get('src')
        # print('get img url from page detail , url = ', src)
        return src


def get_wall_haven_url(query, page):
    return 'https://wallhaven.cc/search?q={0}&page={1}&sorting=toplist&order=desc'.format(query, page)


def fetch_and_download_wall_haven_anime(fetch_url):
    res = send_request_by_proxy(fetch_url)
    if res is None:
        return
    # print(res.text)
    # write_result(res.text)
    bs = base_bs.get_bs_parse_result(res.text)
    links = bs.findAll('a', {'class': 'preview'})
    for link in links:
        href = link.get('href')
        img_url = get_img_url_from_page_detail(href)
        if img_url is None:
            return
        file_name = get_file_name_from_url(img_url)
        file_path = cwd + '/src/' + file_name
        requests_tool.download_img_by_requests(img_url, download_file_path=file_path, overwrite=False)
        log_tool.log('download completed ' + img_url)
        # download_img_by_requests(img_url)


def start_download_anime_wallpaper():
    index = 1
    # browser = base_selenium.BaseBrowser()
    while index < 2:
        log_tool.log('fetch and download, page = {}'.format(index))
        fetch_url = get_wall_haven_url('anime', index)
        fetch_and_download_wall_haven_anime(fetch_url)
        # html = browser.get_html_by_url(fetch_url)
        # print(html)
        index += 1
    # browser.close_browser()


def get_html_by_browser(fetch_url):
    browser = base_selenium.BaseBrowser()
    html = browser.get_html_by_url(fetch_url)
    print(html)


# fetch_wall_haven_anime()
requests_tool = base_requests.BaseRequests(log_tool)
if is_use_aqara:
    requests_tool.set_proxy(AQARA_PROXY)
else:
    requests_tool.set_proxy(SSR_Proxy)
# down_file_url = 'https://w.wallhaven.cc/full/8x/wallhaven-8xxjjj.jpg'
# download_img_by_requests(down_file_url)
start_download_anime_wallpaper()
# img_u = 'https://w.wallhaven.cc/full/vg/wallhaven-vglgwp.jpg'
# requests_tool.download_img_by_requests(
#     img_u,
#     download_file_path=cwd+'/src/'+get_file_name_from_url(img_u),
#     overwrite=False
# )

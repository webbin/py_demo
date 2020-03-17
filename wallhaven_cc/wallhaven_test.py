
from urllib import request as url_request


def custom_proxy_open_url(url: str):
    proxy_host = '127.0.0.1:1087'  # host and port of your proxy

    req = url_request.Request('url')
    req.set_proxy(proxy_host, 'http')

    response = url_request.urlopen(req)
    print(response.read().decode('utf8'))

    




from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# gecko_options = webdriver.FirefoxOptions()
# browser = webdriver.Firefox(options=gecko_options)

class BaseBrowser():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # 使用headless无界面浏览器模式
        # //增加无界面选项
        chrome_options.add_argument('--headless')
        # //如果不加这个选项，有时定位会出现问题
        chrome_options.add_argument('--disable-gpu')

        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        # proxy.http_proxy = "ip_addr:port"
        proxy.socks_proxy = "proxy.aqara.com:1080"
        # proxy.ssl_proxy = "ip_addr:port"

        capabilities = webdriver.DesiredCapabilities.CHROME
        proxy.add_to_capabilities(capabilities)

        # 启动浏览器，获取网页源代码
        self.browser = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)

    def get_html_by_url(self, fetch_url):
        try:
            self.browser.get(fetch_url)
            return self.browser.page_source
        except Exception as e:
            print('selenium get html error {}'.format(str(e)))
            return None

    def close_browser(self):
        self.browser.quit()

# browser.get(mainUrl)
# print(f"browser text = {browser.page_source}")
# browser.quit()

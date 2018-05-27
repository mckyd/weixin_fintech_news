import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from selenium import webdriver
import time
from scrapy.http import HtmlResponse
from weixin_fintech_news.config import CHROME_PATH

class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, agents):
        UserAgentMiddleware.__init__(self, agents)
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(agents = crawler.settings.getlist('USER_AGENTS'))  # 返回的是本类的实例cls ==RandomUserAgent

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class JavaScriptMiddleware(object):
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')
        #chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROME_PATH)

    def __del__(self):
        self.driver.close()

    def process_request(self, request, spider):
        if spider.name == 'weixin_fintech_news':
            self.driver.get(request.url)
            time.sleep(1)
            body = self.driver.page_source
            return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)
        else:
            return None
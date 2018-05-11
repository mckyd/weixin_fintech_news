import random
from scrapy.downloadermiddlewares.useragent import  UserAgentMiddleware
'''

这个类主要用于产生随机UserAgent

'''



class RandomUserAgentMiddleware(UserAgentMiddleware):



    def __init__(self,agents):
        UserAgentMiddleware.__init__(self, agents)
        self.agents = agents



    @classmethod

    def from_crawler(cls,crawler):

        return cls(crawler.settings.getlist('USER_AGENTS'))#返回的是本类的实例cls ==RandomUserAgent



    def process_request(self,request,spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))
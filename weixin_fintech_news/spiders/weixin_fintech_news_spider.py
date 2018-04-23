import scrapy
from weixin_fintech_news.items import WeixinFintechNewsItem
from scrapy.selector import Selector
from weixin_fintech_news.settings import weixin_ids

class WeixinFintechNewsSpider(scrapy.Spider):
    name = "weixin_fintech_news_spider"
    def start_requests(self):
        url_prefix = "http://weixin.sogou.com/weixin?query="
        for weixin_id in weixin_ids:
            url = url_prefix + weixin_id
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = WeixinFintechNewsItem()

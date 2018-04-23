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
        selector = Selector(response)
        profile_href = selector.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a').extract()[0]

        yield scrapy.Request(url=profile_href, callback=self.parse_profile())

    def parse_profile(self, response):
        push_lists = Selector(response).xpath('//*[@id="history"]').extract()[0]
        for push_list in push_lists:
            msg_card_bd = push_lists.xpath('//*').extract()[1]
            #for msg in msg_card_bd:

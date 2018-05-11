import scrapy
from weixin_fintech_news.items import WeixinFintechNewsItem
from scrapy.selector import Selector
from weixin_fintech_news.settings import weixin_ids
import hashlib
import time

class WeixinFintechNewsSpider(scrapy.Spider):
    name = "weixin_fintech_news"
    def start_requests(self):
        url_prefix = "http://weixin.sogou.com/weixin?query="
        for weixin_id in weixin_ids:
            url = url_prefix + weixin_id
            yield scrapy.Request(url=url, callback=self.parse, meta={'wxid': weixin_id})

    def parse(self, response):
        selector = Selector(response)
        profile_href = selector.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a/@href').extract()[0]
        wxid = response.meta['wxid']
        time.sleep(1)
        yield scrapy.Request(url=profile_href, callback=self.parse_profile, meta={'wxid': wxid})

    def parse_profile(self, response):
        itemsDict = {}
        wxid = response.meta['wxid']
        push_lists = Selector(response).xpath('//*[@id="history"]')
        print("push_lists", push_lists)
        # for push_list in push_lists:
        #     msg_card_bd = Selector(text=push_list).xpath('//*').extract()[1]
        #     print('msg_card_bd: ', msg_card_bd)
        #     title = Selector(text=msg_card_bd).xpath('//*[@class="weui_media_title"]/text()').extract()
        #     abstract = Selector(text=msg_card_bd).xpath('//*[@class="weui_media_desc"]/text()').extract()
        #     reference = Selector(text=msg_card_bd).xpath('//*[@class="weui_media_title"]/@hrefs').extract()
        #     image_url = Selector(text=msg_card_bd).xpath('//*[@class="weui_media_hd"]/@style').extract()
        #     post_date = Selector(text=msg_card_bd).xpath('//*[@class="weui_media_desc"]/text()').extract()
        #
        #     itemDict = {'title': title, 'abstract': abstract, 'reference': reference, 'image_url': image_url, 'post_date': post_date}
        #     uuid = hashlib.md5(wxid + title + abstract).hexdigest()
        #     itemsDict[uuid] = itemDict
        return itemsDict
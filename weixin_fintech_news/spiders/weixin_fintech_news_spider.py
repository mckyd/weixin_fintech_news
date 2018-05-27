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
        print('User-Agent: ', response.request.headers.get('User-Agent'), None)
        selector = Selector(response)
        profile_href = selector.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a/@href').extract()[0]
        wxid = response.meta['wxid']
        time.sleep(20)
        yield scrapy.Request(url=profile_href, callback=self.parse_profile, meta={'wxid': wxid})

    def parse_profile(self, response):
        itemsDict = {}
        wxid = response.meta['wxid']
        push_lists = response.xpath('//div[contains(@class, "weui_media_box appmsg")]')
        #print("push_lists: ", push_lists.extract())
        for index, push_list in enumerate(push_lists):
            title = push_list.xpath('.//*[@class="weui_media_title"]/text()').extract()[0].strip()
            abstract = push_list.xpath('.//*[@class="weui_media_desc"]/text()').extract()[0].strip()
            reference = push_list.xpath('.//*[@class="weui_media_title"]/@hrefs').extract()[0].strip()
            image_url = push_list.xpath('.//*[@class="weui_media_hd"]/@style').extract()[0].strip() \
                .lstrip('background-image:url(').rstrip(')')
            post_date = push_list.xpath('.//*[@class="weui_media_extra_info"]/text()').extract()[0].strip()
            itemDict = {'title': title, 'abstract': abstract, 'reference': reference, 'image_url': image_url, 'post_date': post_date}
            uuid = hashlib.md5((wxid + title + abstract).encode('utf-8')).hexdigest()
            itemsDict[uuid] = itemDict
        return itemsDict
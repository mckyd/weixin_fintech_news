# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeixinFintechNewsItem(scrapy.Item):
    # define the fields for your item here like:
    #title = scrapy.Field()
    #abstract = scrapy.Field()
    #reference = scrapy.Field()
    #post_time = scrapy.Field()
    itemsDict = scrapy.Field()

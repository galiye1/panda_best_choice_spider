# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PandaBestChoiceItem(scrapy.Item):
    #商品标题
    title = scrapy.Field()
    #原价
    original_price = scrapy.Field()
    #券后价
    last_price = scrapy.Field()
    #券
    coupon = scrapy.Field()
    #销售量
    sale_num = scrapy.Field()
    #优惠券过期时间
    expire_date = scrapy.Field()

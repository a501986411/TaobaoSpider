# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 商品标题
    title = scrapy.Field()
    # 商品id
    goods_id = scrapy.Field()
    #月销量
    monthly_sales = scrapy.Field()
    pass

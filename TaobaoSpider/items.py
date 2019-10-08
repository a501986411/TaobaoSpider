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
    # 月销量（30天内销量）
    monthly_sales = scrapy.Field()
    # 商品所属 1;自己店铺的数据；2：关注店铺的数据
    owner = scrapy.Field()
    # 自己店铺商品与关注店铺商品的关联id
    relation_id = scrapy.Field()
    pass

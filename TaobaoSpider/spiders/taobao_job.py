# -*- coding: utf-8 -*-
import scrapy
from TaobaoSpider.items import TaobaospiderItem

class TaobaoJobSpider(scrapy.Spider):
    # 定义爬虫名称
    name = 'taobao_job'
    #定义此爬虫允许爬取域名
    allowed_domains = ['taobao.com']
    # 定义该爬虫爬取得首页列表
    start_urls = ['http://taobao.com/']
    def parse(self, response):
        item = TaobaospiderItem()
        item['title'] = ''

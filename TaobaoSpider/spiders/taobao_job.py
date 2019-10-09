# -*- coding: utf-8 -*-
import scrapy
import pymysql
from TaobaoSpider.items import TaobaospiderItem

class TaobaoJobSpider(scrapy.Spider):
    # 定义爬虫名称
    name = 'taobao_job'
    #定义此爬虫允许爬取域名
    allowed_domains = ['taobao.com','tmall.com']
    # 定义该爬虫爬取得首页列表
    start_urls = ''
    def __init__(self):
        self.start_urls = [
            'https://item.taobao.com/item.htm?spm=a2oq0.12575281.0.0.25911debe483LR&ft=t&id=604075431419',
            'https://detail.tmall.com/item.htm?spm=a230r.1.14.39.4f6b3547vNtrST&id=601289609578&ns=1&abbucket=6',
        ]
        super().__init__(scrapy.Spider)


    def parse(self, response):
        item = TaobaospiderItem()
        item['title'] = response.xpath('//title/text()').extract_first()
        yield item



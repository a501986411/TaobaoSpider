# -*- coding: utf-8 -*-
import scrapy
from TaobaoSpider.items import TaobaospiderItem

class TaobaoJobSpider(scrapy.Spider):
    # 定义爬虫名称
    name = 'taobao_job'
    #定义此爬虫允许爬取域名
    allowed_domains = ['taobao.com','tmall.com']
    # 定义该爬虫爬取得首页列表
    start_urls = ['https://detail.tmall.com/item.htm?id=584590068195&spm=a1z0k.7385961.1997985097.d4918997.11bb6b925mRbxO&_u=t2dmg8j26111']
    def parse(self, response):
        item = TaobaospiderItem()
        item['title'] = response.xpath('//title/text()').extract_first()
        yield item



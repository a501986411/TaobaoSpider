# -*- coding: utf-8 -*-
import scrapy
import pymysql
from langconv import *
import sys
from TaobaoSpider.items import TaobaospiderItem

class TaobaoJobSpider(scrapy.Spider):
    # 定义爬虫名称
    name = 'taobao_job'
    #定义此爬虫允许爬取域名
    allowed_domains = ['taobao.com','tmall.com']
    # 定义该爬虫爬取得首页列表
    start_urls = ''
    goods_id = []
    db = ''
    cursor = ''
    goods_id_url = {}
    def __init__(self):
        super().__init__(scrapy.Spider)
        self.db = pymysql.connect('localhost', 'root', 'root', 'easy_taobao')
        self.cursor = self.db.cursor(cursor = pymysql.cursors.DictCursor)
        self.goods_id = self.getGoodsId()
        # url = "https://www.taobao.com/list/item-amp/"+self.goods_id[0]+".htm"
        url = "https://www.taobao.com/list/item-amp/601289609578.htm"
        self.start_urls = [url]
        self.goods_id_url[url] = self.goods_id[0]
        self.goods_id.pop()


    def parse(self, response):
        item = TaobaospiderItem()
        item['title'] = self.cht_to_chs(response.xpath('//h1/text()').extract_first())
        item['goods_id'] = self.goods_id_url[response.url]
        monthly_sales = response.xpath('//span[@class="salesNum"]/text()').extract_first().split('：')
        item['monthly_sales'] = monthly_sales[1]
        if len(self.goods_id) > 0:
            next_url = "https://www.taobao.com/list/item-amp/"+self.goods_id[0]+".htm"
            self.goods_id_url[next_url] = self.goods_id[0]
            self.goods_id.pop()
            yield scrapy.Request(next_url, callback=self.parse)
        yield item


    def getGoodsId(self):
        """
        获取需要爬去的url
        :return: url list
        """
        self.cursor.execute('select goods_id from etb_goods')
        goods_id_list = []
        for row in self.cursor.fetchall():
            goods_id_list.append(row['goods_id'])
            goods_id_list.reverse()
        return goods_id_list

    def cht_to_chs(str):
        """
        中文繁体转简体
        :return:
        """
        str = Converter('zh-hans').convert(str)
        str.encode('utf-8')
        return str




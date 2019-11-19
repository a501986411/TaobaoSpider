# -*- coding: utf-8 -*-
import scrapy
import pymysql
from TaobaoSpider.items import TaobaospiderItem
from langconv import *
import json
from random import choice
import html
import logging
class TaobaoJobSpider(scrapy.Spider):
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    url_prefix = [
        # "https://world.taobao.com/item/%s.htm",
        "https://www.taobao.com/list/item-amp/%s.htm"
    ]
    handle_httpstatus_list = [404]
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
        self.db = pymysql.connect('127.0.0.1', 'root', 'chen19920328', 'easy_taobao')
        self.cursor = self.db.cursor(cursor = pymysql.cursors.DictCursor)
        self.goods_id = self.getGoodsId() #设置所有需要爬去的商品ID
        self.start_urls = [self.get_url()] #设置入口url



    def parse(self, response):
        try:
            # item = self.get_item_for_list_amp(response)
            item = self.get_item_for_word(response)
            next_url = self.get_url()
            if next_url:
                yield scrapy.Request(next_url,
                 headers={
                    "user-agent":choice(self.user_agent_list),
                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }, callback=self.parse)
            yield item
        except:
            next_url = self.get_url()
            if next_url:
                yield scrapy.Request(next_url,headers={
                    "user-agent":choice(self.user_agent_list),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }, callback=self.parse)



    def getGoodsId(self):
        """
        获取需要爬去的url
        :return: url list
        """
        self.cursor.execute('select goods_id,detail_url from etb_goods where goods_id <> "" AND goods_id in (607415124550, 607251861603, 607451390712)')
        goods_id_list = []
        for row in self.cursor.fetchall():
            goods_id_list.append(row['goods_id'])
        goods_id_list.reverse()
        return goods_id_list

    def tradition2simple(self,line):
        # 将繁体转换成简体
        line = Converter('zh-hans').convert(line)
        return line

    def get_url(self):
        """
        获取需要爬去的url
        :return: url
        """
        next_url = ''
        if len(self.goods_id) > 0:
            next_goods_id = self.goods_id.pop()
            next_url = choice(self.url_prefix) % (str(next_goods_id))
            self.goods_id_url[next_url] = next_goods_id
        return next_url

    def get_cover_img(self, response):
        res = response.xpath("//script/text()").extract()
        for item in res:
            try:
                item = json.loads(item)
                if isinstance(item, dict):
                    if '@type' in item:
                        if item['@type'] == 'Product':
                            return item['image'][0]
            except:
                continue
        return ''

    def get_item_for_word(self, response):
        item = TaobaospiderItem()
        item['title'] = self.tradition2simple(response.xpath('//h1/text()').extract_first())
        item['goods_id'] = self.goods_id_url[response.url]
        monthly_sales = response.xpath('//div[@class="sub-title"]/span/text()').extract()[1]
        item['monthly_sales'] = monthly_sales
        item['cover_img'] = self.get_cover_img(response)
        logging.debug(item)
        return item

    def get_item_for_list_amp(self, response):
        item = TaobaospiderItem()
        item['goods_id'] = self.goods_id_url[response.url]
        item['title'] = self.tradition2simple(html.unescape(response.xpath('//h1/text()').extract_first()))
        monthly_sales = response.xpath('//span[@class="salesNum"]/text()').extract_first().split('：')[1]
        item['monthly_sales'] = monthly_sales
        item['cover_img'] = self.get_cover_img(response)
        logging.debug(item)
        return item

    def get_tb_item(self, response):
        item = TaobaospiderItem()
        item['goods_id'] = self.goods_id_url[response.url]
        item['title'] = self.tradition2simple(html.unescape(response.xpath('//title/text()').extract_first()))
        monthly_sales = 0
        item['monthly_sales'] = monthly_sales
        item['cover_img'] = ''
        logging.debug(item)
        return item


# -*- coding: utf-8 -*-
import scrapy
import pymysql
from TaobaoSpider.items import TaobaospiderItem
from langconv import *
from random import choice
import html
import logging
import json
import time
from urllib import parse
import configparser
import conf
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
    type_tb = 1
    type_tm = 2
    type_now = 0
    url_prefix = [
        # "https://world.taobao.com/item/%s.htm",
        "https://www.taobao.com/list/item-amp/%s.htm"
    ]
    tb_url = {
        "title": "https://item.taobao.com/item.htm?spm=a1z10.1-c.w4004-21346271448.4.7d3f3f48rFn2t2&%s",
        'monthly_sales': "https://www.taobao.com/list/item-amp/%s.htm",
        "cover_img": "https://www.taobao.com/list/item-amp/%s.htm",
    }

    tm_url = {
        'title': "https://www.taobao.com/list/item-amp/%s.htm",
        'monthly_sales': "https://www.taobao.com/list/item-amp/%s.htm",
        "cover_img": "https://www.taobao.com/list/item-amp/%s.htm",
    }

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
    goods_type = {}
    cf = ''
    db_cnf = ''
    def __init__(self):
        super().__init__(scrapy.Spider)
        self.db_cnf = configparser.ConfigParser()
        self.cf = conf.conf()
        self.db_cnf.read(self.cf.get_db_conf(), encoding="utf-8")
        self.db = pymysql.connect(self.db_cnf.get('db','db_host'), self.db_cnf.get('db','db_user'),self.db_cnf.get('db','db_pwd'), self.db_cnf.get('db','db_database'))
        self.cursor = self.db.cursor(cursor = pymysql.cursors.DictCursor)
        # 设置所有需要爬去的商品ID
        # self.start_urls = self.get_start_urls() #设置入口url
        self.goods_id = self.getGoodsId()
        self.start_urls = [self.get_url()] #设置入口url

    def parse(self, response):
        try:
            # item = self.get_item_info(response)
            item = self.parse_tb_title_two(response)
            next_url = self.get_url()
            if next_url:
                yield scrapy.Request(next_url,
                 headers={
                    "user-agent": choice(self.user_agent_list),
                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }, callback=self.parse)
            yield item
        except:
            next_url = self.get_url()
            if next_url:
                yield scrapy.Request(next_url, headers={
                    "user-agent": choice(self.user_agent_list),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }, callback=self.parse)

    def get_start_urls(self):
        """
        获取入口url列表
        :return: list
        """
        all_goods_id = self.getGoodsId()
        start_urls = []
        for g_id in all_goods_id:
            start_urls.append(choice(self.url_prefix) % (str(g_id)))
        return  start_urls

    def get_item_info(self, response):
        item = TaobaospiderItem()
        item['goods_id'] = self.goods_id_url[response.url]
        monthly_sales = response.xpath('//span[@class="salesNum"]/text()').extract_first().split('：')[1]
        item['monthly_sales'] = monthly_sales
        if self.type_now == self.type_tb:
            param = {
                "jsv": "2.5.1",
                "appKey": 12574478,
                "t": int(time.time() * 1000),
                # "sign": "08ca47d1bf4ac9d0a8c297fe0980c9b6",
                "api": "mtop.taobao.detail.getdetail",
                "v": "6.0",
                "ttid": "2017@htao_h5_1.0.0",
                "type": "jsonp",
                "dataType": "jsonp",
                "callback": "mtopjsonp1",
                "data": json.dumps({"exParams": "{\"countryCode\":\"CN\"}", "itemNumId": str(item['goods_id'])})
            }

            url = "https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?" + parse.urlencode(param).replace('+', '')
            item = scrapy.Request(url, meta={'item': item}, headers={
                "user-agent": choice(self.user_agent_list),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }, callback=self.parse_tb_title_two)
        elif self.type_now == self.type_tm:
            param = {
                "jsv": "2.5.1",
                "appKey": 12574478,
                "t": int(time.time() * 1000),
                # "sign": "08ca47d1bf4ac9d0a8c297fe0980c9b6",
                "api": "mtop.taobao.detail.getdetail",
                "v": "6.0",
                "ttid": "2017@htao_h5_1.0.0",
                "type": "jsonp",
                "dataType": "jsonp",
                "callback": "mtopjsonp1",
                "data": json.dumps({"exParams": "{\"countryCode\":\"CN\"}", "itemNumId": str(item['goods_id'])})
            }

            url = "https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?" + parse.urlencode(param).replace(
                '+', '')
            item = scrapy.Request(url, meta={'item': item}, headers={
                "user-agent": choice(self.user_agent_list),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }, callback=self.parse_tb_title_two)
        else:
            pass
        return item

    def parse_tb_title_one(self, response):
        # 接收上级已爬取的数据
        item = response.meta['item']
        param = {
            "jsv":"2.5.1",
            "appKey":12574478,
            "t": int(time.time() * 1000),
            #"sign": "08ca47d1bf4ac9d0a8c297fe0980c9b6",
            "api": "mtop.taobao.detail.getdetail",
            "v": "6.0",
            "ttid": "2017@htao_h5_1.0.0",
            "type": "jsonp",
            "dataType": "jsonp",
            "callback": "mtopjsonp1",
            "data" : json.dumps({"exParams":"{\"countryCode\":\"CN\"}","itemNumId":str(item['goods_id'])})
        }

        url = "https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?"+parse.urlencode(param).replace('+','')
        item = scrapy.Request(url, meta={'item': item}, headers={
            "user-agent": choice(self.user_agent_list),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }, callback=self.parse_tb_title_two)
        return item

    def parse_tb_title_two(self, response):
        item = TaobaospiderItem()
        item['goods_id'] = self.goods_id_url[response.url]
        # item = response.meta['item']
        try:
            text = response.xpath("//text()").extract_first().replace("mtopjsonp1(","").replace(")","")
            json_text = json.loads(text)
            if 'item' not in json_text['data']:
                item['title'] = '商品不存在'
                item['cover_img'] = ''
                item['monthly_sales'] = 0
                return item
            else:
                item['title'] = json_text['data']['item']['title']
                item['cover_img'] = json_text['data']['item']['images'][0]
                goods_item = json.loads(json_text['data']['apiStack'][0]['value'])
                if 'sellCount' in goods_item['item']:
                    item['monthly_sales'] = goods_item['item']['sellCount']
                else:
                    item['monthly_sales'] = goods_item['item']['vagueSellCount']
        except Exception as e:
            item['title'] = "获取出错"
            item['cover_img'] = ''
            item['monthly_sales'] = 0
            self.goods_id.append(item['goods_id'])
            logging.error(e)
        return item

    def getGoodsId(self):
        """
        获取需要爬去的url
        :return: url list
        """
        self.cursor.execute('select goods_id,detail_url from etb_goods where goods_id <> ""')
        goods_id_list = []
        for row in self.cursor.fetchall():
            goods_id_list.append(row['goods_id'])
            if "tmall" in row['detail_url']:
                self.goods_type[row['goods_id']] = self.type_tm
            else:
                self.goods_type[row['goods_id']] = self.type_tb
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
            # next_url = choice(self.url_prefix) % (str(next_goods_id))
            param = {
                "jsv": "2.5.1",
                "appKey": 12574478,
                "t": int(time.time() * 1000),
                # "sign": "08ca47d1bf4ac9d0a8c297fe0980c9b6",
                "api": "mtop.taobao.detail.getdetail",
                "v": "6.0",
                "ttid": "2017@htao_h5_1.0.0",
                "type": "jsonp",
                "dataType": "jsonp",
                "callback": "mtopjsonp1",
                "data": json.dumps({"exParams": "{\"countryCode\":\"CN\"}", "itemNumId": str(next_goods_id)})
            }
            next_url = "https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?" + parse.urlencode(param).replace(
                '+', '')
            self.goods_id_url[next_url] = next_goods_id
            # 设置当前爬取的商品的类型
            self.type_now = self.goods_type[next_goods_id]
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


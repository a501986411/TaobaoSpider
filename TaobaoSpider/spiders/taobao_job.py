# -*- coding: utf-8 -*-
import scrapy
import pymysql
from TaobaoSpider.items import TaobaospiderItem
from langconv import *
import json
from random import choice
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
            item = TaobaospiderItem()
            item['title'] = self.tradition2simple(response.xpath('//h1/text()').extract_first())
            item['goods_id'] = self.goods_id_url[response.url]
            # monthly_sales = response.xpath('//span[@class="salesNum"]/text()').extract_first().split('：')
            monthly_sales = response.xpath('//div[@class="sub-title"]/span/text()').extract()[1]
            item['monthly_sales'] = monthly_sales
            item['cover_img'] = self.get_cover_img(response)
            next_url = self.get_url()
            if next_url:
                yield scrapy.Request(next_url, meta={
                 'dont_redirect': True,
                 'handle_httpstatus_list': [302]
                },
                 headers={
                    "authority": "world.taobao.com",
                    "method": "GET",
                    "path": "/item/537493777173.htm",
                    "scheme": "https",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                    "accept-encoding":"gzip, deflate, br",
                    "accept-language":"zh-CN,zh;q=0.9",
                    "cache-control":"max-age=0",
                    "cookie":"thw=cn; t=c2e8b7acdacb20ae46d289e041bb78e8; ali_ab=113.66.108.236.1568125226322.0; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; everywhere_service_strategy=cco_busi:ads_crmwx_wanxiang_guard_crowd:20191007@1; cna=A5/+FQupT2gCAdoTZXW8xTLd; lgc=q7601086; tracknick=q7601086; tg=0; enc=lTBoFEEtynkBcT6ftC8mD7dZmnuFb1TpsSAWsKfd3J0%2Fu%2Fy9aUDP6Tpu7ZoSGPQgLEEGXqqyS8cheOg2yJ5c9Q%3D%3D; cookie2=1c0420fdcc8184bbffebd5a0c45fb1c2; _tb_token_=738beee13b357; v=0; _m_h5_tk=588cec1822ae35a104383acb771e28ab_1573927407905; _m_h5_tk_enc=0b490a55254afefd3f3ee5944f83afe5; unb=890883777; cookie17=W8CN4aYihwvL; dnk=q7601086; _l_g_=Ug%3D%3D; sg=678; _nk_=q7601086; cookie1=ACzhCrlgLybrjbDxXunwXZW%2FtM989GOO%2BOlhaItgeXQ%3D; mt=ci=20_1; uc3=vt3=F8dByuWi4LRGyx2Hgbo%3D&nk2=EqLIKlQ5ROM%3D&lg2=VT5L2FSpMGV7TQ%3D%3D&id2=W8CN4aYihwvL; csg=244b8d63; skt=2578c1cb8c3a507d; existShop=MTU3MzkyMTEzNg%3D%3D; uc4=nk4=0%40EN0Di5EJ%2FxSwpTx8ChGdjr05IA%3D%3D&id4=0%40WeNXGMCJNk5pqDCo%2FgVe%2BKPjGXo%3D; _cc_=WqG3DMC9EA%3D%3D; uc1=cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie21=URm48syIZJfmZ9wVCtpzEQ%3D%3D&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&existShop=true&pas=0&cookie14=UoTbnrFqlHLZtg%3D%3D&tag=8&lng=zh_CN; l=dBE85h6eqwe32LcbKOCanurza77OSIRYYuPzaNbMi_5BT6T6eqbOkKL2yF96VjW5TsYB47_ypV99-etkZ8IZm1pCOGJ7xUvb4bLe4; isg=BMXFMcxTNJQRnxDvhthRMiOm1AE_Knh8-8XmfscqhfwLXuXQj9ZQ5LU8bMINHpHM",
                    "if-none-match":'W/"1355c-+P/4Qa6zZf6pyESXPOmUAW4zfEw"',
                    "sec-fetch-mode":"navigate",
                    "sec-fetch-site":"none",
                    "sec-fetch-user":"?1",
                    "upgrade-insecure-requests":"1",
                    "user-agent":choice(self.user_agent_list)
                }, callback=self.parse)
            yield item
        except:
            next_url = self.get_url()
            if next_url:
                yield scrapy.Request(next_url,meta={
                 'dont_redirect': True,
                 'handle_httpstatus_list': [302]
                },  headers={
                    "authority": "world.taobao.com",
                    "method": "GET",
                    "path": "/item/537493777173.htm",
                    "scheme": "https",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                    "accept-encoding":"gzip, deflate, br",
                    "accept-language":"zh-CN,zh;q=0.9",
                    "cache-control":"max-age=0",
                    "cookie":"thw=cn; t=c2e8b7acdacb20ae46d289e041bb78e8; ali_ab=113.66.108.236.1568125226322.0; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; everywhere_service_strategy=cco_busi:ads_crmwx_wanxiang_guard_crowd:20191007@1; cna=A5/+FQupT2gCAdoTZXW8xTLd; lgc=q7601086; tracknick=q7601086; tg=0; enc=lTBoFEEtynkBcT6ftC8mD7dZmnuFb1TpsSAWsKfd3J0%2Fu%2Fy9aUDP6Tpu7ZoSGPQgLEEGXqqyS8cheOg2yJ5c9Q%3D%3D; cookie2=1c0420fdcc8184bbffebd5a0c45fb1c2; _tb_token_=738beee13b357; v=0; _m_h5_tk=588cec1822ae35a104383acb771e28ab_1573927407905; _m_h5_tk_enc=0b490a55254afefd3f3ee5944f83afe5; unb=890883777; cookie17=W8CN4aYihwvL; dnk=q7601086; _l_g_=Ug%3D%3D; sg=678; _nk_=q7601086; cookie1=ACzhCrlgLybrjbDxXunwXZW%2FtM989GOO%2BOlhaItgeXQ%3D; mt=ci=20_1; uc3=vt3=F8dByuWi4LRGyx2Hgbo%3D&nk2=EqLIKlQ5ROM%3D&lg2=VT5L2FSpMGV7TQ%3D%3D&id2=W8CN4aYihwvL; csg=244b8d63; skt=2578c1cb8c3a507d; existShop=MTU3MzkyMTEzNg%3D%3D; uc4=nk4=0%40EN0Di5EJ%2FxSwpTx8ChGdjr05IA%3D%3D&id4=0%40WeNXGMCJNk5pqDCo%2FgVe%2BKPjGXo%3D; _cc_=WqG3DMC9EA%3D%3D; uc1=cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie21=URm48syIZJfmZ9wVCtpzEQ%3D%3D&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&existShop=true&pas=0&cookie14=UoTbnrFqlHLZtg%3D%3D&tag=8&lng=zh_CN; l=dBE85h6eqwe32LcbKOCanurza77OSIRYYuPzaNbMi_5BT6T6eqbOkKL2yF96VjW5TsYB47_ypV99-etkZ8IZm1pCOGJ7xUvb4bLe4; isg=BMXFMcxTNJQRnxDvhthRMiOm1AE_Knh8-8XmfscqhfwLXuXQj9ZQ5LU8bMINHpHM",
                    "if-none-match":'W/"1355c-+P/4Qa6zZf6pyESXPOmUAW4zfEw"',
                    "sec-fetch-mode":"navigate",
                    "sec-fetch-site":"none",
                    "sec-fetch-user":"?1",
                    "upgrade-insecure-requests":"1",
                    "user-agent":choice(self.user_agent_list)
                }, callback=self.parse)



    def getGoodsId(self):
        """
        获取需要爬去的url
        :return: url list
        """
        self.cursor.execute('select goods_id from etb_goods where goods_id <> ""')
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
            next_url = "https://world.taobao.com/item/"+next_goods_id+".htm"
            self.goods_id_url[next_url] = next_goods_id
            print(next_url)
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




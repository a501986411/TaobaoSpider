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
        self.getPorxy()
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
                    "cookie":"_uab_collina=157395373893266439568875; thw=cn; t=f173acf32e8c8051f0f3114d1d207a13; ali_ab=219.137.59.177.1569119521068.2; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; UM_distinctid=16d96dc01f35b5-0296e398c3bde1-3c604504-1fa400-16d96dc01f458f; everywhere_service_strategy=cco_busi:ads_crmwx_wanxiang_guard_crowd:20191007@1; enc=MMABM%2B3umk16zBJvFLwR8svHsElahQ7lvR71vj8mN8Dx3Lfv3MbjBHjTc8g60%2BV3TuVnwPRnlQqcYxb1Dg1whQ%3D%3D; cna=ocoNFujWMywCAduJO7Cbas0m; v=0; _m_h5_tk=1d6545b1eb3d67b3a93827209387bc3f_1573964048129; _m_h5_tk_enc=1861c5571b300f384633c1d30ee113bb; mt=ci=-1_0; cookie2=19b07e1b62c126daec71009cc1816edc; _tb_token_=e83bfe063f3e5; unb=1771243310; lgc=ydyxfc; cookie17=UoYZawW1ovMJXA%3D%3D; dnk=ydyxfc; tracknick=ydyxfc; tg=0; _l_g_=Ug%3D%3D; sg=c00; _nk_=ydyxfc; cookie1=BYfqCqUpHiQ9EPnuPNCSoJx3LbqiSi%2FQH8rowBp88Do%3D; x5sec=7b22617365727665723b32223a223365333435326630613465373635303236326264323861373938663736363930434d724277753446454b76722b4e69666f4b575970674561444445334e7a45794e444d7a4d5441374d773d3d227d; uc1=cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&pas=0&cookie21=VT5L2FSpdeCjwGS%2FFqZpWg%3D%3D&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&cookie14=UoTbnrFtSEAoaQ%3D%3D&tag=8&existShop=true&lng=zh_CN; uc3=lg2=U%2BGCWk%2F75gdr5Q%3D%3D&vt3=F8dByuWi5VDN1z%2BxyBQ%3D&nk2=Gg9RfyAC&id2=UoYZawW1ovMJXA%3D%3D; csg=f8426f03; skt=c33100e07dfeccd3; existShop=MTU3Mzk1Mzc0OA%3D%3D; uc4=id4=0%40UO6QoO1NXNuDPAcMqXFSXiIjQb9O&nk4=0%40GINykxWkHKzDS3E4KTk6Tp0%3D; _cc_=VFC%2FuZ9ajQ%3D%3D; isg=BFVVgGdepETjYoBumzWYLpCzZFHP-ggMbof0Pdf6EUwbLnUgn6IZNGPs-HI9NSEc; l=dBLdxc8gqXpzTufDBOCanurza77OSIRYYuPzaNbMi_5QK6TsIZ7OkKUYCF96VjWf9lYB4IFj7TJ9-etkZtStWiIpXUJ_GMc.",
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
                    "cookie":"_uab_collina=157395373893266439568875; thw=cn; t=f173acf32e8c8051f0f3114d1d207a13; ali_ab=219.137.59.177.1569119521068.2; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; UM_distinctid=16d96dc01f35b5-0296e398c3bde1-3c604504-1fa400-16d96dc01f458f; everywhere_service_strategy=cco_busi:ads_crmwx_wanxiang_guard_crowd:20191007@1; enc=MMABM%2B3umk16zBJvFLwR8svHsElahQ7lvR71vj8mN8Dx3Lfv3MbjBHjTc8g60%2BV3TuVnwPRnlQqcYxb1Dg1whQ%3D%3D; cna=ocoNFujWMywCAduJO7Cbas0m; v=0; _m_h5_tk=1d6545b1eb3d67b3a93827209387bc3f_1573964048129; _m_h5_tk_enc=1861c5571b300f384633c1d30ee113bb; mt=ci=-1_0; cookie2=19b07e1b62c126daec71009cc1816edc; _tb_token_=e83bfe063f3e5; unb=1771243310; lgc=ydyxfc; cookie17=UoYZawW1ovMJXA%3D%3D; dnk=ydyxfc; tracknick=ydyxfc; tg=0; _l_g_=Ug%3D%3D; sg=c00; _nk_=ydyxfc; cookie1=BYfqCqUpHiQ9EPnuPNCSoJx3LbqiSi%2FQH8rowBp88Do%3D; x5sec=7b22617365727665723b32223a223365333435326630613465373635303236326264323861373938663736363930434d724277753446454b76722b4e69666f4b575970674561444445334e7a45794e444d7a4d5441374d773d3d227d; uc1=cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&pas=0&cookie21=VT5L2FSpdeCjwGS%2FFqZpWg%3D%3D&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&cookie14=UoTbnrFtSEAoaQ%3D%3D&tag=8&existShop=true&lng=zh_CN; uc3=lg2=U%2BGCWk%2F75gdr5Q%3D%3D&vt3=F8dByuWi5VDN1z%2BxyBQ%3D&nk2=Gg9RfyAC&id2=UoYZawW1ovMJXA%3D%3D; csg=f8426f03; skt=c33100e07dfeccd3; existShop=MTU3Mzk1Mzc0OA%3D%3D; uc4=id4=0%40UO6QoO1NXNuDPAcMqXFSXiIjQb9O&nk4=0%40GINykxWkHKzDS3E4KTk6Tp0%3D; _cc_=VFC%2FuZ9ajQ%3D%3D; isg=BFVVgGdepETjYoBumzWYLpCzZFHP-ggMbof0Pdf6EUwbLnUgn6IZNGPs-HI9NSEc; l=dBLdxc8gqXpzTufDBOCanurza77OSIRYYuPzaNbMi_5QK6TsIZ7OkKUYCF96VjWf9lYB4IFj7TJ9-etkZtStWiIpXUJ_GMc.",
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

    def getPorxy(self):
        url = "http://http.tiqu.alicdns.com/getip3?num=20&type=2&pro=&city=0&yys=0&port=1&pack=72703&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=2&regions=";
        res = scrapy.Request(url)
        print(res)



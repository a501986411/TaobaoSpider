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
                    #"cookie":"_uab_collina=157395181210035995436112; thw=cn; t=f173acf32e8c8051f0f3114d1d207a13; ali_ab=219.137.59.177.1569119521068.2; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; UM_distinctid=16d96dc01f35b5-0296e398c3bde1-3c604504-1fa400-16d96dc01f458f; everywhere_service_strategy=cco_busi:ads_crmwx_wanxiang_guard_crowd:20191007@1; enc=MMABM%2B3umk16zBJvFLwR8svHsElahQ7lvR71vj8mN8Dx3Lfv3MbjBHjTc8g60%2BV3TuVnwPRnlQqcYxb1Dg1whQ%3D%3D; cookie2=189bc53494d9a5f0c0532f72fe8307f1; _tb_token_=737615be75370; _m_h5_tk=a256dc17440ea3487c3a23f653135f39_1573959221342; _m_h5_tk_enc=1ad56373a2d0a107a93a9b3fe5019e8b; cna=ocoNFujWMywCAduJO7Cbas0m; v=0; unb=1771243310; uc3=vt3=F8dByuWi5VDKMGe7P6w%3D&id2=UoYZawW1ovMJXA%3D%3D&lg2=VT5L2FSpMGV7TQ%3D%3D&nk2=Gg9RfyAC; csg=53437c38; lgc=ydyxfc; cookie17=UoYZawW1ovMJXA%3D%3D; dnk=ydyxfc; skt=33c4b602dcd3812e; existShop=MTU3Mzk1MzA0Ng%3D%3D; uc4=nk4=0%40GINykxWkHKzDS3E4KTk9Mnk%3D&id4=0%40UO6QoO1NXNuDPAcMqXFSXiIjRtla; tracknick=ydyxfc; _cc_=U%2BGCWk%2F7og%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=c00; _nk_=ydyxfc; cookie1=BYfqCqUpHiQ9EPnuPNCSoJx3LbqiSi%2FQH8rowBp88Do%3D; mt=ci=16_1; l=dBLdxc8gqXpzTkckBOCgCuI8Ls7tSIRAguPRwC0Xi_5aE1Y6GZ_OkKFFDev6cjWf9BLB4IFj7TJ9-etkZJRgTBpCOGJWhxDc.; isg=BPn5kq7KgDjZh1z6V0H8AhQ_CGUTruzQansIyRsufSCfohk0Y1WiiMrwIObxGoXw; uc1=cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie21=UtASsssmfavZrexPkAwn7A%3D%3D&cookie15=W5iHLLyFOGW7aA%3D%3D&existShop=true&pas=0&cookie14=UoTbnrFtSEc8RQ%3D%3D&tag=8&lng=zh_CN",
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
                    #"cookie":"_uab_collina=157395181210035995436112; thw=cn; t=f173acf32e8c8051f0f3114d1d207a13; ali_ab=219.137.59.177.1569119521068.2; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; UM_distinctid=16d96dc01f35b5-0296e398c3bde1-3c604504-1fa400-16d96dc01f458f; everywhere_service_strategy=cco_busi:ads_crmwx_wanxiang_guard_crowd:20191007@1; enc=MMABM%2B3umk16zBJvFLwR8svHsElahQ7lvR71vj8mN8Dx3Lfv3MbjBHjTc8g60%2BV3TuVnwPRnlQqcYxb1Dg1whQ%3D%3D; cookie2=189bc53494d9a5f0c0532f72fe8307f1; _tb_token_=737615be75370; _m_h5_tk=a256dc17440ea3487c3a23f653135f39_1573959221342; _m_h5_tk_enc=1ad56373a2d0a107a93a9b3fe5019e8b; cna=ocoNFujWMywCAduJO7Cbas0m; v=0; unb=1771243310; uc3=vt3=F8dByuWi5VDKMGe7P6w%3D&id2=UoYZawW1ovMJXA%3D%3D&lg2=VT5L2FSpMGV7TQ%3D%3D&nk2=Gg9RfyAC; csg=53437c38; lgc=ydyxfc; cookie17=UoYZawW1ovMJXA%3D%3D; dnk=ydyxfc; skt=33c4b602dcd3812e; existShop=MTU3Mzk1MzA0Ng%3D%3D; uc4=nk4=0%40GINykxWkHKzDS3E4KTk9Mnk%3D&id4=0%40UO6QoO1NXNuDPAcMqXFSXiIjRtla; tracknick=ydyxfc; _cc_=U%2BGCWk%2F7og%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=c00; _nk_=ydyxfc; cookie1=BYfqCqUpHiQ9EPnuPNCSoJx3LbqiSi%2FQH8rowBp88Do%3D; mt=ci=16_1; l=dBLdxc8gqXpzTkckBOCgCuI8Ls7tSIRAguPRwC0Xi_5aE1Y6GZ_OkKFFDev6cjWf9BLB4IFj7TJ9-etkZJRgTBpCOGJWhxDc.; isg=BPn5kq7KgDjZh1z6V0H8AhQ_CGUTruzQansIyRsufSCfohk0Y1WiiMrwIObxGoXw; uc1=cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie21=UtASsssmfavZrexPkAwn7A%3D%3D&cookie15=W5iHLLyFOGW7aA%3D%3D&existShop=true&pas=0&cookie14=UoTbnrFtSEc8RQ%3D%3D&tag=8&lng=zh_CN",
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




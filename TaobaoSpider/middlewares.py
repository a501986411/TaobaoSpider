# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from random import choice
import requests
class TaobaospiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TaobaospiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class ProxyMiddleware(object):
    proxys = [
        "112.114.89.246:4532",
        "58.252.201.126:4525",
        "180.116.168.57:4576",
        "140.237.162.184:4554",
        "182.111.93.100:4573",
        "182.244.169.106:4565",
        "117.60.45.20:4521",
        "220.165.155.71:4532",
        "113.76.63.107:4572",
        "183.166.161.14:4526",
        "113.100.85.150:4583",
        "220.176.65.169:4543",
        "117.90.191.207:4507",
        "117.90.74.73:4507",
        "122.237.182.130:4575",
        "163.179.205.134:4561",
        "112.114.131.7:4528",
        "117.63.26.239:4575",
        "117.91.131.32:4545",
        "106.35.35.74:4554"
    ]

    def get_proxy_ip(self, proxy):
        proxies = {"http": proxy}
        response = requests.get('http://www.baidu.com', proxies=proxies, timeout=2)
        if response.status_code != 200:
            return proxy
        return False




    def process_request(self,request,spider):
        proxy = self.get_proxy_ip(choice(self.proxys))
        if proxy == False:
            proxy = self.get_proxy_ip(choice(self.proxys))
        print("使用的IP:", proxy)
        if request.url.startswith("http://"):
            request.meta['proxy']="http://"+ str(proxy)
        elif request.url.startswith("https://"):
            request.meta['proxy']="https://"+ str(proxy)
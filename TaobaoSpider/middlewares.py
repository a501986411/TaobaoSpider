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

    def valVer(self):
        proxys = [
            {"ip":"58.218.200.253", "port":7031, "outip":"183.252.126.66"},
            {"ip":"58.218.200.253", "port":6288, "outip":"103.40.223.204"},
            {"ip":"58.218.201.114", "port":6523, "outip":"223.64.7.107"},
            {"ip":"58.218.200.253", "port":8474, "outip":"122.226.158.132"},
            {"ip":"58.218.200.253","port":7759,"outip":"112.0.15.220"},
            {"ip":"58.218.201.74","port":8432,"outip":"120.83.116.190"},
            {"ip":"58.218.200.253","port":8243,"outip":"111.41.245.236"},
            {"ip":"58.218.201.114","port":4855,"outip":"120.239.50.255"},
            {"ip":"58.218.200.253","port":3101,"outip":"183.251.186.73"},
            {"ip":"58.218.200.214","port":8411,"outip":"117.27.20.43"},
            {"ip":"58.218.201.114","port":5593,"outip":"111.0.181.24"},
            {"ip":"58.218.201.122","port":6600,"outip":"110.52.94.255"},
            {"ip":"58.218.201.114","port":9056,"outip":"111.41.22.138"},
            {"ip":"58.218.201.74","port":7840,"outip":"101.17.140.15"},
            {"ip":"58.218.201.74","port":3707,"outip":"60.9.218.144"},
            {"ip":"58.218.200.253","port":6426,"outip":"112.10.70.235"},
            {"ip":"58.218.201.74","port":3631,"outip":"175.44.8.43"},
            {"ip":"58.218.201.114","port":8843,"outip":"183.251.120.43"},
            {"ip":"58.218.200.214","port":8349,"outip":"223.247.86.228"},
            {"ip":"58.218.200.214","port":5603,"outip":"115.203.83.5"}
        ]
        badNum = 0
        goodNum = 0
        good = []
        for proxy in proxys:
            try:
                proxy_host = proxy
                protocol = 'https' if 'https' in proxy_host else 'http'
                proxies = {protocol: proxy_host}
                response = requests.get('http://www.baidu.com', proxies=proxies, timeout=2)
                if response.status_code != 200:
                    badNum += 1
                    print(proxy_host, 'bad proxy')
                else:
                    goodNum += 1
                    good.append(proxies)
                    print(proxy_host, 'success proxy')
            except Exception as e:
                print(e)
                # print proxy_host, 'bad proxy'
                badNum += 1
                continue
        print('success proxy num : ', goodNum)
        print('bad proxy num : ', badNum)
        return good


    def process_request(self,request,spider):
        proxys = self.valVer()
        
        proxy = choice(proxys)
        if request.url.startswith("http://"):
            request.meta['proxy']="http://"+ proxy['ip'] + ":" + str(proxy['port'])
        elif request.url.startswith("https://"):
            request.meta['proxy']="https://"+ proxy['ip'] + ":" + str(proxy['port'])
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from random import choice
import requests
import sys
import logging
import configparser
import time
import conf
import json
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
    proxy_cf = ''
    cf =''
    db = ''
    cursor = ''
    get_proxy_url = ""
    def __init__(self):
        self.proxy_cf = configparser.ConfigParser()
        self.cf = conf.conf()
        self.proxy_cf.read(self.cf.get_proxy_conf(), encoding="utf-8")

    def get_proxy_ip(self):
        proxy_ip = self.proxy_cf.get('proxy', 'ip')
        if proxy_ip == '':
            proxy_ip = self.get_ip_by_url()

        # 检查代理是否失效
        try:
            proxies = {"http": proxy_ip}
            response = requests.get('http://www.baidu.com', proxies=proxies)
            if response.status_code != 200:
                logging.debug('代理'+proxy_ip+'失效,重新获取')
                proxy_ip = self.get_ip_by_url()
        except Exception as e:
            logging.error(e)
            proxy_ip = self.get_ip_by_url()
        return proxy_ip

    def get_ip_by_url(self):
        url = self.proxy_cf.get('proxy', 'url')
        try:
            response = requests.get(url)
            if response.status_code == 200:
                if "code" in response.text:
                    logging.error(response.text)
                    sys.exit(0)
                else:
                    if "code" in response.text:
                        proxy_ip = self.get_ip_by_url()
                    else:
                        proxy_ip = response.text.strip()
                        self.proxy_cf.set('proxy', 'ip', proxy_ip)
                        self.proxy_cf.set('proxy', 'get_ip_time', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                        with open(self.cf.get_proxy_conf(), "w+") as f:
                                self.proxy_cf.write(f)
            else:
                proxy_ip = ''
                logging.error('代理IP获取失败1')
        except Exception as e:
            logging.error('代理IP获取失败2；'+e)
            proxy_ip = ''
        return proxy_ip

    def process_request(self, request, spider):
        proxy_ip = self.get_proxy_ip()
        if proxy_ip:
            if request.url.startswith("http://"):
                request.meta['proxy'] = "http://" + str(proxy_ip)
            elif request.url.startswith("https://"):
                request.meta['proxy'] = "https://" + str(proxy_ip)
        else:
            logging.debug("未设置代理IP")
            sys.exit(0)
        logging.info('使用的代理:'+proxy_ip)

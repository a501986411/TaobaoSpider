# -*- coding: utf-8 -*-

# Scrapy settings for TaobaoSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'TaobaoSpider'

SPIDER_MODULES = ['TaobaoSpider.spiders']
NEWSPIDER_MODULE = 'TaobaoSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'TaobaoSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'TaobaoSpider.middlewares.TaobaospiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#   'TaobaoSpider.middlewares.TaobaospiderDownloaderMiddleware': 543,
    'TaobaoSpider.middlewares.ProxyMiddleware': 400,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'TaobaoSpider.pipelines.TaobaospiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
DEFAULT_REQUEST_HEADERS = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    "cookie": "thw=cn; t=c2e8b7acdacb20ae46d289e041bb78e8; ali_ab=113.66.108.236.1568125226322.0; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; everywhere_service_strategy=cco_busi:ads_crmwx_wanxiang_guard_crowd:20191007@1; cna=A5/+FQupT2gCAdoTZXW8xTLd; lgc=q7601086; tracknick=q7601086; tg=0; enc=lTBoFEEtynkBcT6ftC8mD7dZmnuFb1TpsSAWsKfd3J0%2Fu%2Fy9aUDP6Tpu7ZoSGPQgLEEGXqqyS8cheOg2yJ5c9Q%3D%3D; cookie2=1c0420fdcc8184bbffebd5a0c45fb1c2; _tb_token_=738beee13b357; v=0; _m_h5_tk=588cec1822ae35a104383acb771e28ab_1573927407905; _m_h5_tk_enc=0b490a55254afefd3f3ee5944f83afe5; unb=890883777; cookie17=W8CN4aYihwvL; dnk=q7601086; _l_g_=Ug%3D%3D; sg=678; _nk_=q7601086; cookie1=ACzhCrlgLybrjbDxXunwXZW%2FtM989GOO%2BOlhaItgeXQ%3D; mt=ci=20_1; uc3=vt3=F8dByuWi4LRGyx2Hgbo%3D&nk2=EqLIKlQ5ROM%3D&lg2=VT5L2FSpMGV7TQ%3D%3D&id2=W8CN4aYihwvL; csg=244b8d63; skt=2578c1cb8c3a507d; existShop=MTU3MzkyMTEzNg%3D%3D; uc4=nk4=0%40EN0Di5EJ%2FxSwpTx8ChGdjr05IA%3D%3D&id4=0%40WeNXGMCJNk5pqDCo%2FgVe%2BKPjGXo%3D; _cc_=WqG3DMC9EA%3D%3D; uc1=cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=U%2BGCWk%2F7owY3j65jYmjW9Q%3D%3D&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&existShop=true&pas=0&cookie14=UoTbnrFqlHdt1w%3D%3D&tag=8&lng=zh_CN; l=dBE85h6eqwe32d09KOCanurza77OSIRYYuPzaNbMi_5a-6T6iF7OkKLXJF96VjWftRYB47_ypV99-etkZd42YOPvlXVjIDc.; isg=BFFRjSH36LD-kwQDEpQd1v8iYF0rFsRYV8HSUjPmT5g32nEsew2AAiQ4eO6ZUl1o",
}

#database config
MYSQL_HOST = '127.0.0.1'
MYSQL_DATABASE = 'easy_taobao'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_CHARSET = 'utf8mb4'
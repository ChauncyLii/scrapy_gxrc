# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import requests
import random
import logging

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class GxrcSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        # spider.logger.info('Spider opened: %s' % spider.name)
        pass


class GxrcDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.logger = logging.getLogger('INFO')
        self.ip_list = []

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    # 获取芝麻代理的ip
    def get_ip(self):
        url = "http://http.tiqu.letecs.com/getip3?num=13&type=2&pro=0&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=&gm=4"
        # url选择json
        body = {
        }
        headers = {
        }
        response = requests.post(url, json=body, headers=headers)
        # print(response.text)
        ip_data = response.json()
        if ip_data['code'] == 0:
            print("获取成功");
        # 获取ip 端口 生成 http://ip:端口 url
        result = []
        for ip_dic in ip_data['data']:
            url = 'http://{0}:{1}'.format(ip_dic['ip'], ip_dic['port'])
            result.append(url)
        self.ip_list = result

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        ua = UserAgent()
        request.headers['User-Agent'] = ua.random

        # 判断ip_list的长度如果长度<20,则调用get_ip获取ip
        if len(self.ip_list) < 5:
            self.get_ip()
        request.meta['proxy'] = random.choice(self.ip_list)
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        # 检测是否响应正常，如果返回不正常则清除此ip，并且返回request重新进行请求
        if response.status != 200:
            i = 0
            while i < len(self.ip_list):
                if self.ip_list[i] == request.meta['proxy']:
                    del self.ip_list[i]
                    self.logger.info('\033[0:31mDelete an Porxy {0}\033[m'.format(self.ip_list[i])) # 输出带有颜色的自定义的INFO信息
                    break
                i+= 1
            return request
        self.logger.info('\033[0:32m Use Proxy "{0}" get URL "{1}"\033[m'.format(request.meta['proxy'],response.url)) # 输出带有颜色的自定义的INFO信息
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
        # spider.logger.info('Spider opened: %s' % spider.name)
        pass

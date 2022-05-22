import scrapy
import js2py
from gxrc.items import GxrcItem
import logging

class GxrcSpider(scrapy.spiders.Spider):
    # https://www.gxrc.com/
    name = "gxrc"

    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('scrapy.spidermiddlewares.httperror')
        logger.setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)

    def start_requests(self):
        # 执行javascript代码
        list = []
        data = open('./gxrc/gxrc.js', 'r', encoding='utf-8').read()
        list = js2py.eval_js(data)  # [['一级目录', '二级目录', '职位', 'URL'], ['一级目录', '二级目录', '职位类型', 'URL']]
        i = 0
        while(i<len(list)):
            url = list[i][3]
            yield scrapy.Request(url=url,meta={'list_4':list[i]},callback=self.parse)
            i+=1


    # 获取到 一层目录 二层目录 三层目录 工资 更新日期 职位的详情页的URL
    def parse(self,response):
        list_4 = response.meta['list_4'] # 第四个值用不着
        for i in response.xpath("//div[@class='posDetailWrap']/div[@class='rlOne']"): # 获取这一页的全部项
            item = GxrcItem()
            item['level_1'] = list_4[0] # 一层目录
            item['level_2'] = list_4[1] # 二层目录
            item['level_3'] = list_4[2] # 三层目录
            item['salary'] = i.xpath("ul[@class='posDetailUL clearfix']/li[@class='w3']/text()").get() # 薪资
            item['release_date'] = i.xpath("ul[@class='posDetailUL clearfix']/li[@class='w5']/text()").get() # 发布日期
            item['detail_url'] = i.xpath("ul/li[@class='w1']/h3/a[@class='posName']/@href").get() # 详细页的URL
            yield scrapy.Request(item['detail_url'],meta={'item':item},callback=self.detail)



    # 获取 公司名称 职位名称 详细工作地点 学习要求 工作经验 职位描述 薪资福利
    def detail(self,response):
        item = response.meta['item']
        item['company_name'] = response.xpath("//div[@class='ent-name']/a[@class='a']/text()").get() # 公司名称
        item['target_post'] = response.xpath("//div[@id='header']//h1/@title").get() # 职位名称
        place = response.xpath("//div[@class='BMap_bubble_content']/div[@class='iw_poi_content']/text()").get()
        if place != None:  # 详细工作地点
            item['place'] = place
        else:
            item['place'] = response.xpath("//p[@class='detail']/text()[1]").get()
        item['edu_requirements'] = response.xpath("//p[@class='detail']/text()[2]").get() # 学历要求
        item['exp_requirements'] = response.xpath("//p[@class='detail']/text()[3]").get() # 工作经验要求
        # item['weal'] = response.xpath().get("") # 福利
        item['job_requirements'] = response.xpath("//pre[@id='examineSensitiveWordsContent']/text()").get() # 职位描述
        yield item
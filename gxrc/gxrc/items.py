# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GxrcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 获取到 工资 更新日期 职位的详情页的URL
    # 获取 公司名称 职位名称 详细工作地点 学历要求 工作经验 职位描述 薪资福利
    # 公司名称 职位名称 详细工作地点 学历要求 工作经验 工资 薪资福利 职位描述 职位的详细页的URL 更新日期

    level_1 = scrapy.Field() # 一层目录
    level_2 = scrapy.Field() # 二层目录
    level_3 = scrapy.Field() # 三层目录
    company_name = scrapy.Field()  # 公司名称
    target_post = scrapy.Field() # 职位名称
    place = scrapy.Field()  # 详细工作地点
    edu_requirements = scrapy.Field()  # 学历要求
    exp_requirements = scrapy.Field()  # 工作经验要求
    salary = scrapy.Field() # 薪资
    job_requirements = scrapy.Field()  # 职位描述
    detail_url = scrapy.Field()  # 详细页URL
    release_date = scrapy.Field()  # 发布日期

    # weal = scrapy.Field()  # 福利
    # p_tag = scrapy.Field() # 岗位标签
    # post_type = scrapy.Field() # 行业
    # company_profile = scrapy.Field() # 公司简介

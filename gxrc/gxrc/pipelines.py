# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class GxrcPipeline(object):
    def __init__(self):
        try:
            self.db = pymysql.connect(
                host="127.0.0.1", # ip地址
                user="root", # 用户名
                password="xxxxxxxxxx", # 数据库密码
                database="info") # 数据库
            self.mycursor = self.db.cursor()
        except:
            print("数据库连接失败")

    def process_item(self, item, spider):
        sql = f'INSERT INTO `gxrc`(`level_1`,`level_2`,`level_3`,`company_name`,`target_post`,`place`,`edu_requirements`,`exp_requirements`,`salary`,`job_requirements`,`detail_url`,`release_date`,`city`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self.mycursor.execute(sql,(item['level_1'],item['level_2'],item['level_3'],item['company_name'],item['target_post'],item['place'],item['edu_requirements'],item['exp_requirements'],item['salary'],item['job_requirements'],item['detail_url'],item['release_date'],"南宁"))
            self.db.commit()
        except Exception as e:
            print("Error:数据写入失败： %s" %e)
        return item

    def close_spider(self,spider):
        self.db.close()

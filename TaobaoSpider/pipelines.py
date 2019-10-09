# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class TaobaospiderPipeline(object):
    """
    保存爬虫数据到数据库
    """
    db = ''
    cursor = ''
    def __init__(self):
        self.db = pymysql.connect('localhost', 'root', 'root', 'easy_taobao')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        print(item)
        # self.saveData(item)

    def saveData(self, item):
        sql = "INSERT INTO etb_goods_log (goods_id, title) \
               VALUES (%s, '%s')" % \
              (item['goods_id'], item['title'])
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()


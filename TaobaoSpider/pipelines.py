# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import logging
class TaobaospiderPipeline(object):
    """
    保存爬虫数据到数据库
    """
    db = ''
    cursor = ''
    def __init__(self):
        self.db = pymysql.connect('47.240.39.15', 'etb', 'chen19920328', 'easy_taobao')
        # self.db = pymysql.connect('localhost', 'root', 'chen19920328', 'easy_taobao')
        self.cursor = self.db.cursor(cursor = pymysql.cursors.DictCursor)

    def reConnect(self):
        try:
            self.db.connection.ping()
        except:
            self.db.connection()

    def process_item(self, item, spider):
        self.save_data(item)

    def save_data(self, item):
        sql = "INSERT INTO etb_goods_log (goods_id, title, monthly_sales, cover_img) \
               VALUES (%s, '%s', %s, '%s')" % \
              (item['goods_id'], item['title'], item['monthly_sales'], item['cover_img'])
        u_sql = "update etb_goods set title='%s',monthly_sales=%s, cover_img='%s' where goods_id=%s" % \
                (item['title'], item['monthly_sales'], item['cover_img'], item['goods_id'])
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 执行更新语句
            self.cursor.execute(u_sql)

            self.db.commit()
        except Exception as e:
            logging.error(e)
            self.db.rollback()





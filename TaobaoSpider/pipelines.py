# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import logging
import configparser
import conf
class TaobaospiderPipeline(object):
    """
    保存爬虫数据到数据库
    """
    db = ''
    cursor = ''
    db_cnf = ''
    cf = ''
    def __init__(self):
        self.db_cnf = configparser.ConfigParser()
        self.cf = conf.conf()
        self.db_cnf.read(self.cf.get_db_conf(), encoding="utf-8")
        self.db = pymysql.connect(self.db_cnf.get('db', 'db_host'), self.db_cnf.get('db', 'db_user'), self.db_cnf.get('db', 'db_pwd'), self.db_cnf.get('db', 'db_database'))
        self.cursor = self.db.cursor(cursor = pymysql.cursors.DictCursor)

    def reConnect(self):
        try:
            self.db.connection.ping()
        except:
            self.db.connection()

    def process_item(self, item, spider):
        if item['result'] != False:
            self.save_data(item)
        else:
            pass

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





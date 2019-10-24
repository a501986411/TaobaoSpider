# -*- coding: utf-8 -*-
import pymysql
from scrapy.utils.project import get_project_settings

class Db:
    db_host = ''
    db_database = ''
    db_user = ''
    db_port = ''
    db_pwd = ''
    db_charset = 'utf8'
    db = ''
    def __init__(self):
        setting = get_project_settings()
        self.db_host = setting.get('MYSQL_HOST')
        self.db_database = setting.get('MYSQL_DATABASE')
        self.db_user = setting.get('MYSQL_USER')
        self.db_port = setting.get('MYSQL_PORT')
        self.db_pwd = setting.get('MYSQL_PASSWORD')
        self.db_charset = setting.get('MYSQL_CHARSET')

    def get_db(self):
        if type(self.db) != pymysql:
            self.db = pymysql.connect(self.db_host, self.db_port, self.db_user, self.db_pwd, self.db_database, self.db_charset)
        return self.db

    def __repr__(self):
        return 'User[name=%s]' % self.name

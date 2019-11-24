# -*- coding: utf-8 -*-

class conf :
    # conf_dir = "G:\\project\\TaobaoSpider\\config\\"
    conf_dir = "/www/TaobaoSpider/config/"
    def get_db_conf(self):
        return self.conf_dir+"db.ini"

    def get_proxy_conf(self):
        return self.conf_dir + "proxy.ini"

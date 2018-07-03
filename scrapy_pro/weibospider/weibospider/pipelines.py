# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import pymongo
from scrapy.conf import settings

from weibospider.items import WeibospiderItem


class UserCreateTimePipeline(object):
    def process_item(self, item, spider):
        item['create_time'] = datetime.now().strftime('%Y-%m-%d %H-%M')
        return item


class WeibospiderPipeline(object):
    def process_item(self, item, spider):
        return item


class WeibospiderPymongoPipeline(object):
    # 用于保存数据
    def __init__(self):
        self.conn = pymongo.MongoClient(host=settings['MONGODB_HOST'],
                                        port=settings['MONGODB_PORT'])
        self.db = self.conn[settings['MONGODB_DB']]
        self.collections = self.db[WeibospiderItem.Collections]

    def process_item(self, item, spider):
        # self.collections.insert(dict(item))
        self.collections.update({'id': dict(item)['id']}, {'$set': dict(item)}, upsert=True)
        return item
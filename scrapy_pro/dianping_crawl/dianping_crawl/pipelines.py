# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

from dianping_crawl.items import DianpingCrawlItem


class DianpingCrawlPipeline(object):

    def __init__(self):
        self.conn = pymongo.MongoClient(host=settings['MONGODB_HOST'],
                                        port=settings['MONGODB_PORT'])
        self.db = self.conn[settings['MONGODB_DB']]
        self.collections = self.db[DianpingCrawlItem.Collections]

    def process_item(self, item, spider):
        self.collections.update({'id': item['id']}, {'$set': item}, upsert=True)
        return item
